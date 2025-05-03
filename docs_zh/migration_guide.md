# 迁移指南

## 迁移到 APIFlask 2.x

### 为 `input` 数据使用关键字参数

在 APIFlask 2.x 中，通过 `input` 装饰器传递的数据更改为名为 `{location}_data` 的关键字参数。例如，JSON 输入的名称将是 `json_data`：

```py
@app.post('/pets')
@app.input(PetQuery, location='query')
@app.input(PetIn)  # 等同于 app.input(PetIn, location='json')
def create_pet(query_data, json_data):
    pass
```

你可以使用 `arg_name` 设置自定义参数名称：

```py
@app.post('/pets')
@app.input(PetQuery, location='query')
@app.input(PetIn, arg_name='pet')
def create_pet(query_data, pet):
    pass
```


### 替换 `/redoc` 和 `redoc_path` 参数

从 APIFlask 2.x 开始，所有的 OpenAPI 文档都可以通过 `/docs` 访问。你可以使用 `docs_ui` 参数将文档界面更改为 ReDoc，并使用 `docs_path` 参数更改文档路径：

```py
from apiflask import APIFlask

app = APIFlask(__name__, docs_ui='redoc', docs_path='/redoc')
```


### 在 `@app.doc` 中将 `tag` 参数替换为 `tags`

`tag` 参数已被移除，应该使用 `tags`。始终为 `tags` 传递一个列表。

```py
@app.doc(tags=['foo'])
```


### 在 `@app.auth_required` 中将 `role` 参数替换为 `roles`

`role` 参数已被移除，应该使用 `roles`。始终为 `roles` 传递一个列表。

```py
@app.doc(auth_required=['admin'])
```


### 对于 204 响应始终设置 `output(status_code=204)`

在 APIFlask 2.x 中，空模式（schema）有了不同的含义，并且不会将状态码设置为 204。

要返回 204 响应，你必须设置状态码：

```py
@app.get('/nothing')
@app.output({}, status_code=204)
def nothing():
    return ''
```
