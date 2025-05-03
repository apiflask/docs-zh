# 从 Flask 迁移

由于 APIFlask 是基于 Flask 的一个轻量级封装，你只需要修改很少的代码即可将你的应用迁移到 APIFlask（通常少于十行代码）。


## `Flask` 类 -> `APIFlask` 类

这是创建 Flask 应用的方式：

```python
from flask import Flask

app = Flask(__name__)
```

现在改为 APIFlask：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
```


## `Blueprint` 类 -> `APIBlueprint` 类

这是创建 Flask 蓝图的方式：

```python
from flask import Blueprint

bp = Blueprint('foo', __name__)
```

现在改为 APIFlask：

```python
from apiflask import APIBlueprint

bp = APIBlueprint('foo', __name__)
```

!!! 提示

    你可以将一个 `Blueprint` 对象注册到 `APIFlask` 实例，但不能将一个 `APIBlueprint` 对象注册到 `Flask` 实例。


## 使用路由快捷方式（可选）

APIFlask 提供了一些路由快捷方式，你可以将一个视图函数更新为：

```python
@app.route('/pets', methods=['POST'])
def create_pet():
    return {'message': 'created'}
```

改为：

```python
@app.post('/pets')
def create_pet():
    return {'message': 'created'}
```

!!! 提示

    你可以混合使用 `app.route()` 和路由快捷方式。Flask 2.0 将包含这些路由快捷方式。


## 基于类的视图（MethodView）

!!! 警告 "版本 >= 0.5.0"

    此功能在 [版本 0.5.0](/changelog/#version-050) 中添加。

APIFlask 支持使用基于 `MethodView` 的视图类，例如：

```python
from apiflask import APIFlask, Schema
from flask.views import MethodView

# ...

class Pet(MethodView):

    decorators = [doc(responses=[404])]

    @app.output(PetOut)
    def get(self, pet_id):
        pass

    @app.output({}, status_code=204)
    def delete(self, pet_id):
        pass

    @app.input(PetIn)
    @app.output(PetOut)
    def put(self, pet_id, json_data):
        pass

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, json_data):
        pass

app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

基于 `View` 的视图类不受支持，你仍然可以使用它，但目前 APIFlask 无法为其生成 OpenAPI 规范（和 API 文档）。


## 其他行为变化和注意事项


### 导入语句

你只需要从 `apiflask` 包中导入 `APIFlask`、`APIBlueprint` 和其他 APIFlask 提供的工具。对于其他内容，仍然从 `flask` 包中导入：

```python
from apiflask import APIFlask, APIBlueprint
from flask import request, render_template, g, session, url_for
```


### APIFlask 的 `abort()` 与 Flask 的 `abort()`

APIFlask 的 `abort()` 函数将返回一个 JSON 错误响应，而 Flask 的 `abort()` 返回一个 HTML 错误页面：

```python
from apiflask import APIFlask, abort

app = APIFlask(__name__)

@app.get('/foo')
def foo():
    abort(404)
```

在上述示例中，当用户访问 `/foo` 时，响应体将是：

```json
{
    "detail": {},
    "message": "Not Found",
    "status_code": 404
}
```

你可以使用 `message` 和 `detail` 参数在 `abort()` 函数中传递错误信息和详细信息。

!!! 警告

    函数 `abort_json()` 在 [版本 0.4.0](/changelog/#version-040) 中被重命名为 `abort()`。


### JSON 错误和混合使用 `flask.abort()` 和 `apiflask.abort()`

当你将基础应用类更改为 `APIFlask` 时，即使使用 Flask 的 `abort()` 函数，所有的错误响应也会自动转换为 JSON 格式：

```python
from apiflask import APIFlask
from flask import abort

app = APIFlask(__name__)

@app.get('/foo')
def foo():
    abort(404)
```

如果你想禁用此行为，只需将 `json_errors` 参数设置为 `False`：

```python
from apiflask import APIFlask

app = APIFlask(__name__, json_errors=False)
```

现在你仍然可以使用来自 `apiflask` 包的 `abort` 返回 JSON 错误响应。要混合使用 `flask.abort` 和 `apiflask.abort`，需要为其中一个导入指定不同的名称：

```python
from apiflask import abort as abort_json
```

以下是一个完整示例：

```python hl_lines="1 14"
from apiflask import APIFlask, abort as abort_json
from flask import abort

app = APIFlask(__name__, json_errors=False)


@app.get('/html-error')
def foo():
    abort(404)


@app.get('/json-error')
def bar():
    abort_json(404)
```


### 将位置参数传递给视图函数

在 APIFlask 1.x 中，为了确保将参数按自然顺序传递给视图函数，它会将路径参数作为位置参数传递给视图函数。

假设一个视图如下：

```python
@app.get('/<category>/articles/<int:article_id>')  # category, article_id
@app.input(ArticleQuery, location='query')  # query
@app.input(ArticleIn)  # data
def get_article(category, article_id, query, data):
    pass
```

使用 APIFlask，你可以以自然的方式在视图函数中接受参数（从左到右，从上到下）：

```python
def get_article(category, article_id, query, data)
```

当你使用自定义装饰器访问参数时，这可能会导致问题。因此在 APIFlask 2.x 中，所有传递给视图函数的参数都将是关键字参数。

通过 `app.input()` 装饰器传递的参数将命名为 `{location}_data`，可以通过 `arg_name` 参数设置自定义参数名称。更多详情请参见 [基本用法](/usage)。


### 视图函数的返回值

对于没有 `@app.output` 装饰器的简单视图函数，你可以返回一个字典或列表作为 JSON 响应。返回的字典和列表将自动转换为 JSON 响应（通过调用 [`jsonify()`](https://flask.palletsprojects.com/api/#flask.json.jsonify) 实现）。

!!! 提示

    尽管列表看起来像元组，但只有列表返回值会被序列化为 JSON 响应。元组有 [特殊含义](https://flask.palletsprojects.com/quickstart/#about-responses)。

    从 Flask 2.2 开始，列表返回值已被原生支持。

```python
@app.get('/foo')
def foo():
    return {'message': 'foo'}


@app.get('/bar')
def bar():
    return ['foo', 'bar', 'baz']
```

当你为视图函数添加了 `@app.output` 装饰器时，APIFlask 期望你返回一个 ORM/ODM 模型对象或一个与 `@app.output` 装饰器中传递的模式匹配的字典/列表。如果你返回一个 `Response` 对象，APIFlask 将直接返回它而不做任何处理。


## 下一步

现在你的应用已迁移到 APIFlask。查看 [基本用法](/usage) 章节以了解更多关于 APIFlask 的内容。享受吧！
