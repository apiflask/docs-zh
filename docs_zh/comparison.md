# 对比与动机

APIFlask 是基于 APIFairy（和 flask-smorest 一样，提供类似的 API）的一个分支开发，并且受到 flask-smorest 和 FastAPI 的启发。 那么， APIFlask 与 APIFairy/flask-smorest/FastAPI 之间有什么区别呢？

总之，我试图提供一个优雅的（作为框架，不需要实例化额外的扩展对象）和简单的（对 OpenAPI / API 提供更多自动化支持）解决方案，来创建基于 Flask 的 Web API。以下是 APIFlask 和相似项目差异的摘要。

## APIFlask vs FastAPI

- 对于 Web 部分，FastAPI 基于 Starlette 构建，而 APIFlask 基于 Flask 构建。
- 对于数据部分（序列化/反序列化，OpenAPI 支持），FastAPI 依赖于 Pydantic，而 APIFlask 使用 marshmallow-code 项目（marshmallow，webargs，apispec）。
- APIFlask 基于 Flask 开发，因此它与 Flask 扩展兼容。
- FastAPI 支持异步。APIFLASK 基于 Flask 2.0 将支持基本的异步。
- APIFlask 提供了更多的装饰器来帮助更好地组织代码。
- FastAPI 将输入数据作为对象注入，而 APIFlask 则使用字典传递。
- APIFlask 具有基于 Flask's `MethodView` 的内置类视图支持。

## APIFlask vs APIFairy/flask-smorest

### 这是一个框架（为什么？）

虽然 APIFlask 是 Flask 上层的一个薄包装器，但它实际上是一个框架。因此，无需实例化其他扩展对象：

```python
from flask import Flask
from flask_api_extension import APIExtension

app = Flask(__name__)
api = APIExtension(app)
```

你只需使用 `APIFlask` 类来替换 `Flask` 类：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
```

APIFlask 能成为框架而不是一个 Flask 扩展的关键原因在于：

- 我必须重写 `Flask` 类，以确保注入到视图函数中参数的自然顺序。
- 我必须重写 `Flask` 类和 `Blueprint` 类来添加快捷路由。
- 可以添加更多高级功能，例如支持返回列表作为 JSON 响应。

有关更多详细信息，请参阅以下两个部分。


### 视图参数的自然顺序

作为 Flask 上层框架，APIFlask 可以重写 Flask 由关键字参数到位置参数传递到视图函数的方式。

假设这样一个视图：

```python
@app.get('/<category>/articles/<int:article_id>')  # category, article_id
@app.input(ArticleQuerySchema, location='query')  # query
@app.input(ArticleInSchema)  # data
def get_article(category, article_id, query, data):
    pass
```

使用 APIFlask，你可以很自然地接受视图函数中的参数（从左到右，从上到下）：

```python
def get_article(category, article_id, query, data)
```

但是，对于 APIFairy、Flask-Smorest 或 webargs，需要在输入数据之后声明路径变量（ `category` 和 `article_id`）：

```python
def get_article(query, data, category, article_id)
```

### 快捷路由

APIFlask 为 `app.route(..., methods=['GET/POST...'])` 添加了一些快捷路由（`app.get()`, `app.post()` , 等）

不需要这样做：

```python
@app.route('/pets', methods=['POST'])
def create_pet():
    pass
```

可以仅使用 `@app.post()`：

```python
@app.post('/pets')
def create_pet():
    pass
```

!!! 提示

    Flask 将在 2.0 版本中对这些快捷路由提供原始支持。

### OpenAPI 更加自动化地生成

- 根据视图函数的名称为视图函数添加自动摘要。
- 为仅使用路由修饰符的裸视图函数添加成功响应 （200）。
- 为使用 `input` 装饰器的视图函数添加验证错误响应 （400）。
- 为使用 `auth_required` 装饰器的视图函数添加身份验证错误响应 （401）。
- 为包含 URL 变量的视图函数添加 404 响应。
- 为使用 `doc` 装饰器的视图函数的潜在错误响应添加响应 schema。例如 `doc(responses=[404, 405])`。
- 等等.

!!! 提示

    可以使用相关的[配置变量](/configuration)更改这些自动化行为。


### 比 APIFairy 具有更多特性

- 添加 `doc` 装饰器来允许以显式方式为视图函数设置 OpenAPI 规范。
- 支持更多 OpenAPI 字段（所有字段来自 `info`, `servers`，响应/请求体/参数 `example`，路径 `deprecated`， 等）。
- 支持自定义 API 文档配置和 CDN 网址。
- 将所有 HTTP 错误和身份验证错误的 JSON 响应作为默认值返回。
- 支持类视图。
- 等等
