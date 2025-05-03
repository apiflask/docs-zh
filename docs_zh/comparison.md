# 对比与动机

APIFlask 基于 APIFairy（它和 flask-smorest 提供类似的 API）的一个 fork 实现，并受到 flask-smorest 和 FastAPI 的启发。那么，APIFlask 与 APIFairy/flask-smorest/FastAPI 之间有什么区别呢？

简而言之，对于使用 Flask 开发 Web API，我试图提供一个优雅（作为框架，不需要实例化额外的扩展对象）和简单的（对 OpenAPI/API 提供更多自动化支持）解决方案。以下是 APIFlask 和相似项目差异的总结。


## APIFlask vs FastAPI

- 对于 Web 部分，FastAPI 基于 Starlette 构建，而 APIFlask 基于 Flask 构建。
- 对于数据处理部分（序列化/反序列化，OpenAPI 支持），FastAPI 依赖于 Pydantic，而 APIFlask 使用 marshmallow-code 项目（marshmallow、webargs、apispec）。
- APIFlask 基于 Flask 开发，因此它与 Flask 扩展相兼容。
- FastAPI 支持异步。APIFlask 基于 Flask 2.0+ 可以实现基本的异步支持。
- APIFlask 提供了更多的装饰器来帮助更好地组织代码。
- FastAPI 将输入数据作为对象注入，而 APIFlask 则使用字典传递。
- APIFlask 基于 Flask 的 `MethodView` 实现了内置的类视图支持。
- 除了 Swagger UI 和 Redoc，APIFlask 还支持更多的 API 文档工具：Elements、RapiDoc 和 RapiPDF。


## APIFlask vs APIFairy/flask-smorest


### APIFlask 是一个框架

虽然 APIFlask 是 Flask 之上的一层薄薄的包装，但它实际上是一个框架。因此，无需实例化其他扩展对象：

```python
from flask import Flask
from flask_api_extension import APIExtension

app = Flask(__name__)
api = APIExtension(app)
```

只需使用 `APIFlask` 类来替换 `Flask` 类：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
```

将 APIFlask 设计为框架而不是 Flask 扩展的关键原因在于，这使得覆盖和更改 Flask 的内部行为成为可能。例如：

- 重写 `Flask.dispatch_request` 以确保注入到视图函数中的参数的自然顺序（APIFlask 1.x）。
- 为 `Flask` 和 `Blueprint` 类添加路由快捷方式（在 Flask 2.0 中添加）。
- 重写 `Flask.make_response` 以支持将列表作为 JSON 响应返回（在 Flask 2.2 中添加）。
- 重写 `Flask.add_url_rule` 以支持为基于类的视图生成 OpenAPI 规范。

### OpenAPI 生成更加自动化

- 根据视图函数的名称为视图函数添加自动摘要（summary）。
- 为仅使用路由修饰符的裸视图函数添加成功响应（200）。
- 为使用 `input` 装饰器的视图函数添加验证错误响应（422）。
- 为使用 `auth_required` 装饰器的视图函数添加认证错误响应（401）。
- 为包含 URL 变量的视图函数添加 404 响应。
- 为使用 `doc` 装饰器的视图函数的潜在错误响应添加响应 schema，例如 `doc(responses=[404, 405])`。
- ……

!!! tip

    你可以使用相关的[配置变量](/configuration)更改这些自动化行为。


### 功能更丰富和完善

- 添加 `doc` 装饰器来允许以显式方式为视图函数设置 OpenAPI spec。
- 支持设置更多 OpenAPI 字段（`info` 的所有子字段、`servers`、响应/请求体/参数的 `example`、路径 `deprecated` 等）。
- 支持自定义 API 文档的配置和 CDN 网址。
- 默认为所有 HTTP 错误和认证错误返回 JSON 响应。
- 支持类视图。
- ……
