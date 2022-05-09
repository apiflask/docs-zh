# 从Flask迁移

因为 APIFlask 是 Flask 之上的一层包装，你应该能不费吹灰之力就将你的 Flask 应用迁移到 APIFlask（通常不会改动超过十行代码）。


## `Flask` 类 -> `APIFlask` 类

你一般这样创建一个 Flask 应用：

```python
from flask import Flask

app = Flask(__name__)
```

现在，将它改写为 APIFlask 应用：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
```


## `Blueprint` 类 -> `APIBlueprint` 类

你一般这样创建一个 Flask 蓝本：

```python
from flask import Blueprint

bp = Blueprint(__name__, 'foo')
```

现在，将它改写为 APIFlask 蓝本只需：

```python
from apiflask import APIBlueprint

bp = APIBlueprint(__name__, 'foo')
```

!!! tip "提示"

    你可以把一个 `Blueprint` 对象注册到一个 `APIFlask` 实例，但是你不能把一个
	`APIBlueprint` 对象注册到一个 `Flask` 实例。


## （可选的）使用快捷路径方法

APIFlask 提供了一些快捷路径方法，你可以将一个视图函数：

```python hl_lines="1"
@app.route('/pets', methods=['POST'])
def create_pet():
    return {'message': 'created'}
```

改写为:

```python hl_lines="1"
@app.post('/pets')
def create_pet():
    return {'message': 'created'}
```

!!! tip "提示"

	你可以将 `app.route()` 与快捷路径方法混用。需要注意的是，
	Flask 2.0 版本已经内置了这些方法。

## 基于 MethodView 的视图类

!!! warning "使用0.5.0及以上的版本"

    这个特性在[0.5.0版本](/changelog/#version-050)添加。

APIFlask 支持基于 `MethodView` 的视图类，例如：

```python
from apiflask import APIFlask, Schema, input, output
from flask.views import MethodView

# ...

@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):

    decorators = [doc(responses=[404])]

    @app.output(PetOutSchema)
    def get(self, pet_id):
        pass

    @app.output({}, 204)
    def delete(self, pet_id):
        pass

    @app.input(PetInSchema)
    @app.output(PetOutSchema)
    def put(self, pet_id, data):
        pass

    @app.input(PetInSchema(partial=True))
    @app.output(PetOutSchema)
    def patch(self, pet_id, data):
        pass
```

APIFlask 支持对一个基于 `MethodView` 的视图类添加 `route` 装饰器，但是你也可以使用
`add_url_rule` 方法来灵活注册这个视图类。

虽然基于 `View` 的类视图不被支持，你依然可以使用它，尽管目前 APIFlask 还无法为它生成
OpenAPI spec 以及 API 文档。


## 其他改动以及一些提示

### 引入语句

你只需要引入 `APIFlask`、`APIBlueprint` 以及其他 `apiflask` 包提供的其他有用的组件。
对于其他需要的对象或函数，你依然需要从 `flask` 包中引入它们：

```python
from apiflask import APIFlask, APIBlueprint
from flask import request, escape, render_template, g, session, url_for
```


### 对比 APIFlask 与 Flask 中的 `abort()`

APIFlask 中的 `abort()` 函数会返回一个JSON错误响应，但 Flask 中的 `abort()`
会返回一个HTML错误页面：

```python
from apiflask import APIFlask, abort

app = APIFlask(__name__)

@app.get('/foo')
def foo():
    abort(404)
```

在上面的例子中，当用户访问 `/foo` 时，返回的响应体将会是：

```json
{
    "detail": {},
    "message": "Not Found",
    "status_code": 404
}
```

你可以在 `abort()` 函数中使用 `message` 和 `detail` 两个参数来传递错误消息以及详细的信息

!!! warning "警告"

    `abort_json()` 函数在 [0.4.0 版本](/changelog/#version-040) 中被重命名为 `abort()`。


### JSON 错误和对 `flask.abort()` 和 `apiflask.abort()` 的混用

当你将应用基类改为 `APIFlask` 时，所有的错误响应将会自动转换为 JSON 格式，即使你在使用
Flask 提供的 `abort()` 函数：

```python
from apiflask import APIFlask
from flask import abort

app = APIFlask(__name__)

@app.get('/foo')
def foo():
    abort(404)
```

如果你希望禁用这种自动转换，仅需设置 `json_errors` 参数为 `False`：

```python hl_lines="3"
from apiflask import APIFlask

app = APIFlask(__name__, json_errors=False)
```

现在，你仍可以使用 `apiflask` 包提供的 `abort()` 来返回一个 JSON 错误响应。
如果你想混用 `flask.abort` 和 `apiflask.abort`，引入其中的一个时你需要使用一个不同的名字：

```python
from apiflask import abort as abort_json
```

这里是一个完整的例子：

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


### 视图函数的返回值

当你为你的视图函数添加 `@app.output` 装饰器时，APIFlask 将会认为你返回的 ORM/ODM 模型或是字典
符合你向 `@app.output` 传递的 Schema。如果你返回一个 `Response` 对象，APIFlask 直接返回它，不会
进行任何处理。

## 接下来的路

现在，你的应用应该已经迁移到了 APIFlask，你可以访问 [基本用法](/usage) 一章来学习更多关于
APIFlask 的内容。乐在其中吧！
