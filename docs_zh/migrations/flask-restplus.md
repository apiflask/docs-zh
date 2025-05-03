# 从 Flask-RESTPlus 或 Flask-RESTX 迁移

Flask-RESTPlus 是一个为 Flask 提供快速构建 REST API 支持的扩展。它已不再维护，并被 Flask-RESTX 取代。

APIFlask 和 Flask-RESTPlus/Flask-RESTX 具有类似的目标和功能，但实现方式不同。本指南将帮助你从 Flask-RESTPlus/Flask-RESTX 迁移到 APIFlask。

## 初始化

=== "Flask-RESTPlus"

    ```python
    from flask import Flask
    from flask_restx import Api

    app = Flask(__name__)
    api = Api(app)
    ```

    或：

    ```python
    from flask import Flask
    from flask_restx import Api

    api = Api()

    app = Flask(__name__)
    api.init_app(app)
    ```

=== "APIFlask"

    ```python
    from apiflask import APIFlask

    app = APIFlask(__name__)
    ```

## 路由

=== "Flask-RESTPlus"

    ```python
    from flask import Flask
    from flask_restx import Resource, Api

    app = Flask(__name__)
    api = Api(app)

    @api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return {'message': 'Hello world'}
    ```

=== "APIFlask"

    ```python
    from apiflask import APIFlask

    app = APIFlask(__name__)

    @app.get('/hello')
    def hello_world():
        return {'message': 'Hello world!'}
    ```

    或：

    ```python
    from apiflask import APIFlask
    from flask.views import MethodView

    app = APIFlask(__name__)

    class HelloWorld(MethodView):
        def get(self):
            return {'message': 'Hello world!'}

    app.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))
    ```

## 响应格式化/序列化

=== "Flask-RESTPlus"

    Flask-RESTPlus 使用 `api.model` 创建模型，并使用 `marshal_with` 装饰器进行响应格式化。

    ```python
    from flask_restplus import fields, marshal_with

    user_fields = api.model('User', {
        'name': fields.String,
        'age': fields.Integer
    })

    @api.route('/users')
    class User(Resource):
        @marshal_with(user_fields)
        def get(self):
            return {'name': 'John', 'age': 30}
    ```

=== "APIFlask"

    APIFlask 使用 [marshmallow](https://marshmallow.readthedocs.io/en/stable/) 定义数据模式，并使用 `app.output` 进行响应格式化。

    ```python
    from apiflask import Schema
    from apiflask.fields import Integer, String

    class User(Schema):
        name = String()
        age = Integer()

    @app.get('/users')
    @app.output(User)
    def get_user():
        return {'name': 'John', 'age': 30}
    ```

    你也可以直接从 `marshmallow` 导入 `Schema`、`Integer` 和 `String`。

## 请求解析/参数解析

=== "Flask-RESTPlus"

    Flask-RESTPlus 使用内置的 `reqparse` 模块进行请求解析。

    ```python
    from flask_restplus import reqparse

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('age', type=int, required=True)
    args = parser.parse_args()
    ```

    但 `reqparse` 模块已被弃用，并将在未来版本中移除。

    此外，你还可以使用 `api.expect` 和 API 模型进行请求解析。

    ```python
    from flask_restplus import fields, marshal_with

    user_fields = api.model('User', {
        'name': fields.String,
        'age': fields.Integer
    })

    @api.route('/users')
    class User(Resource):
        @api.expect(user_fields)
        def post(self):
            pass
    ```

=== "APIFlask"

    APIFlask 使用 [marshmallow](https://marshmallow.readthedocs.io/en/stable/) 定义数据模式，并使用 `api.input` 进行请求解析。

    ```python
    from apiflask import Schema
    from apiflask.fields import Integer, String

    class User(Schema):
        name = String(required=True)
        age = Integer(required=True)

    @app.get('/')
    @app.input(User, location='json')
    def create_user(json_data):  # 参数名默认为 `<location_name>_data`
        pass
    ```

    你也可以直接从 `marshmallow` 导入 `Schema`、`Integer` 和 `String`。

## 错误处理

=== "Flask-RESTPlus"

    Flask-RESTPlus 会自动处理错误并返回包含错误信息的 JSON 响应。

    ```json
    {
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }
    ```

    要添加自定义错误数据，可以向异常添加 `data` 属性或使用 `flask_restplus.abort` 方法。

    ```python
    from flask_restplus import abort
    abort(400, custom='value')
    ```

    输出：

    ```json
    {
        "message": "The browser (or proxy) sent a request that this server could not understand.",
        "custom": "value"
    }
    ```

    要记录错误响应，可以在文档字符串中使用 `:raises` 注释。

    ```python
    @api.route('/test/')
    class TestResource(Resource):
        def get(self):
            '''
            执行某些操作

            :raises CustomException: 在某些情况下
            '''
            pass
    ```

=== "APIFlask"

    APIFlask 也会自动处理错误并返回包含错误信息的 JSON 响应。

    ```json
    {
        "message": "The browser (or proxy) sent a request that this server could not understand.",
        "detail": {}
    }
    ```

    要添加自定义字段，可以定义一个继承自 `HTTPException` 的自定义异常类：

    ```python
    from apiflask import HTTPError

    class PetNotFound(HTTPError):
        status_code = 404
        message = 'This pet is missing.'
        extra_data = {
            'error_code': '2323',
            'error_docs': 'https://example.com/docs/missing'
        }
    ```

    或使用 `apiflask.abort` 和 `extra_data` 参数：

    ```python
    abort(
        400,
        message='Something is wrong...',
        extra_data={
            'docs': 'http://example.com',
            'error_code': 1234
        }
    )
    ```

    输出：

    ```json
    {
        "message": "Something is wrong...",
        "detail": {},
        "docs": "http://example.com",
        "error_code": 1234
    }
    ```

    要记录错误响应，可以使用 `app.doc` 装饰器：

    ```python
    @app.get('/')
    @app.doc(responses=[400])
    def hello():
        return 'Hello'
    ```

## OpenAPI（以前称为 Swagger）文档

对于 Flask-RESTPlus/Flask-RESTX，默认的 OpenAPI 规范可通过 `/swagger.json` 获取，Swagger UI 可通过 API 根路径 `/` 访问。

对于 APIFlask，默认的 OpenAPI 规范可通过 `/openapi.json` 获取，Swagger UI 或其他替代 UI 可通过 `/docs` 访问。

要收集 API 文档，它们提供了类似的 API，详情见下表：

| Flask-RESTPlus/Flask-RESTX | APIFlask |
| --- | --- |
| `@api.doc()` | `@app.doc()` |
| `@api.marshal_with()` | `@app.output()` |
| `@api.expect()` | `@app.input()` |
| `@api.responses()` | `@app.doc(responses=...)` |
| `@api.deprecated` | `@app.doc(deprecated=True)` |
| `@api.hide` | `@app.doc(hide=True)` |

它们还以类似的方式定义 API 文档的基本设置：

Flask-RESTPlus/Flask-RESTX:

```python
from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', description='A sample API')
```

APIFlask:

```python
app = APIFlask(__name__, version='1.0', title='Sample API', description='A sample API')
```

但 APIFlask 提供了 [广泛的配置选项](/configuration) 用于 API 文档。

## Postman 支持和字段掩码

=== "Flask-RESTPlus"

    Flask-RESTPlus 提供了生成 Postman 集合的内置功能：

    ```python
    from flask import json

    from myapp import api

    urlvars = False  # 在 URL 中构建查询字符串
    swagger = True  # 导出 Swagger 规范
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    print(json.dumps(data))
    ```

    它还支持通过请求中提供自定义头部来获取部分对象（即字段掩码）。

=== "APIFlask"

    APIFlask 尚未提供这些功能。
    如果需要，请[创建功能请求](https://github.com/apiflask/apiflask/issues/new?assignees=&labels=feature&projects=&template=feature-request.md&title=)。
