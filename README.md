
![](https://apiflask.com/_assets/apiflask-logo.png)

# APIFlask 中文文档

[![Build status](https://github.com/apiflask/apiflask/actions/workflows/tests.yml/badge.svg)](https://github.com/apiflask/apiflask/actions) [![codecov](https://codecov.io/gh/apiflask/apiflask/branch/main/graph/badge.svg?token=2CFPCZ1DMY)](https://codecov.io/gh/apiflask/apiflask) [![Netlify Status](https://api.netlify.com/api/v1/badges/456180b4-55f0-417c-9c4e-88e407a24011/deploy-status)](https://app.netlify.com/sites/zh-apiflask/deploys)


## 翻译流程

欢迎参与翻译，仓库地址为：

<https://github.com/apiflask/docs-zh>

参与翻译的基本流程如下：

- 创建 PR 在下面列表里你想翻译的章节后添加你的名字，一次一章
- Fork 本仓库（[apiflask/docs-zh](https://github.com/apiflask/docs-zh)），然后克隆你的 fork 到本地（将下面的 `{username}` 替换为你的用户名）：

```
$ git clone https://github.com/{username}/docs-zh
$ cd docs-zh
$ git remote add upstream https://github.com/apiflask/docs-zh
```

- 参考[贡献指南](/contributing)搭建开发环境（跳过 fork 部分）
- 阅读《[翻译指南](https://github.com/apiflask/docs-zh/wiki/Translation-Guide)》了解翻译要求
- 创建 branch 翻译 docs_zh/ 目录下对应的文件
- 执行 `mkdocs serve` 预览文档并修正错误
- 提交 PR 等待审核


## 翻译章节列表

- Home (index.md) [@greyli](https://github.com/greyli)
- Documentation Index (docs.md) [@rice0208](https://github.com/rice0208)
- Migrating from Flask (migrating.md) [@z-t-y](https://github.com/z-t-y)
- Basic Usage (usage.md) [@Farmer](https://github.com/FarmerChillax)
- Request Handling (request.md) [@rice0208](https://github.com/rice0208)
- Response Formatting (response.md) [@Tridagger](https://github.com/Tridagger)
- Data Schema (schema.md) [@rice0208](https://github.com/rice0208)
- Authentication (authentication.md) [@z-t-y](https://github.com/z-t-y)
- OpenAPI Generating (openapi.md) [@rice0208](https://github.com/rice0208)
- Swagger UI and Redoc (api-docs.md) [@Tridagger](https://github.com/Tridagger)
- Configuration (configuration.md) [@z-t-y](https://github.com/z-t-y)
- Error Handling (error-handling.md) [@yangfan9702](https://github.com/yangfan9702)
- Examples (examples.md) [@Tridagger](https://github.com/Tridagger)
- Comparison and Motivations (comparison.md) [@Tridagger](https://github.com/Tridagger)
- Authors (authors.md)
- Changelog (changelog.md)
- Contributing Guide (contributing.md)
- API Reference:
    - APIFlask (api/app.md)
    - APIBlueprint (api/blueprint.md)
    - Exceptions (api/exceptions.md)
    - OpenAPI (api/openapi.md)
    - Schemas (api/schemas.md)
    - Fields (api/fields.md)
    - Validators (api/validators.md)
    - Route (api/route.md)
    - Security (api/security.md)
    - Helpers (api/helpers.md)
    - Commands (api/commands.md)


## 介绍

APIFlask 是一个轻量的 Python web API 框架，基于 [Flask](https://github.com/pallets/flask) 和 [marshmallow-code](https://github.com/marshmallow-code) 项目实现。它易于使用，高度可定制，可搭配任意 ORM/ODM 框架，并且和 Flask 生态 100% 兼容。

APIFlask 提供了下面这些主要特性：

- 为视图函数实现了更多的语法糖（`@app.input()`、`@app.output()`、`@app.get()`、`@app.post()` 等）
- 自动化请求验证和反序列化（基于 [webargs](https://github.com/marshmallow-code/webargs)）
- 自动化响应格式化和序列化（基于 [marshmallow](https://github.com/marshmallow-code/marshmallow)）
- 自动生成 [OpenAPI 规范](https://github.com/OAI/OpenAPI-Specification) （OAS，原 Swagger 规范）文档（基于 [apispec](https://github.com/marshmallow-code/apispec)）
- 自动生成交互式 API 文档（基于 [Swagger UI](https://github.com/swagger-api/swagger-ui) 和 [Redoc](https://github.com/Redocly/redoc)）
- API 认证支持（基于 [Flask-HTTPAuth](https://github.com/miguelgrinberg/flask-httpauth)）
- 自动为 HTTP 错误生成 JSON 响应


## 要求

- Python 3.8+
- Flask 2.0+


## 安装

Linux 和 macOS：

```bash
$ pip3 install apiflask
```

Windows：

```bash
> pip install apiflask
```


## 链接

- 网站：<https://apiflask.com>
- 文档：<https://apiflask.com/docs>
- PyPI：<https://pypi.python.org/pypi/APIFlask>
- 变更日志：<https://apiflask.com/changelog>
- 源代码：<https://github.com/apiflask/apiflask>
- Issue 追踪：<https://github.com/apiflask/apiflask/issues>
- 论坛（英文）：<https://github.com/apiflask/apiflask/discussions>
- 论坛（中文）：<https://discuss.helloflask.com/>
- Twitter：<https://twitter.com/apiflask>


## 示例

```python
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get('/')
def say_hello():
    # 返回字典或列表等同于使用 jsonify()
    return {'message': 'Hello!'}


@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    if pet_id > len(pets) - 1:
        abort(404)
    # 你也可以直接返回一个 ORM/ODM 模型类实例
    # APIFlask 会将其序列化为 JSON 格式
    return pets[pet_id]


@app.patch('/pets/<int:pet_id>')
@app.input(PetIn(partial=True))  # -> json_data
@app.output(PetOut)
def update_pet(pet_id, data):
    # 验证且解析后的请求输入数据会
    # 作为一个字典传递给视图函数
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in json_data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]
```

注意：`input`、`output`、`doc` 和 `auth_required` 装饰器现在移动到了程序/蓝本实例上，
如果你使用 APIFlask 0.12 及以下版本，则需要使用独立的装饰器具体参考
[这里](https://apiflask.com/usage/#move-to-new-api-decorators)。

<details>
<summary>你也可以通过 <code>MethodView</code> 编写基于类的视图（class-based views）</summary>

```python
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from flask.views import MethodView

app = APIFlask(__name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()


class Hello(MethodView):

    # 使用 HTTP 方法名作为类方法名
    def get(self):
        return {'message': 'Hello!'}


class Pet(MethodView):

    @app.output(PetOut)
    def get(self, pet_id):
        """Get a pet"""
        if pet_id > len(pets) - 1:
            abort(404)
        return pets[pet_id]

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, json_data):
        """Update a pet"""
        if pet_id > len(pets) - 1:
            abort(404)
        for attr, value in json_data.items():
            pets[pet_id][attr] = value
        return pets[pet_id]


app.add_url_rule('/', view_func=Hello.as_view('hello'))
app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```
</details>

<details>
<summary>或使用 <code>async def</code>（Flask 2.0）</summary>

```bash
$ pip install -U "apiflask[async]"
```

```python
import asyncio

from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
async def say_hello():
    await asyncio.sleep(1)
    return {'message': 'Hello!'}
```

参考 <a href="https://flask.palletsprojects.com/async-await">Using async and await</a> 了解 Flask 2.0 的异步支持。

</details>

把代码保存到 `app.py`，然后使用下面的命令运行：

```bash
$ flask run --reload
```

现在访问 <http://localhost:5000/docs> 查看交互式 API 文档（Swagger UI）：

![](https://apiflask.com/_assets/swagger-ui.png)

或者你可以在创建 APIFlask 实例时通过 `docs_ui` 参数来设置 API 文档 UI
([APIFlask 1.1+](https://apiflask.com/changelog/#version-110)):

```py
app = APIFlask(__name__, docs_ui='redoc')
```

现在 <http://localhost:5000/docs> 将会使用 Redoc 渲染 API 文档：

![](https://apiflask.com/_assets/redoc.png)

支持的 `docs_ui` 选项（API 文档库）包括：

- `swagger-ui`（默认值）：[Swagger UI](https://github.com/swagger-api/swagger-ui)
- `redoc`：[Redoc](https://github.com/Redocly/redoc)
- `elements`：[Elements](https://github.com/stoplightio/elements)
- `rapidoc`：[RapiDoc](https://github.com/rapi-doc/RapiDoc)
- `rapipdf`：[RapiPDF](https://github.com/mrin9/RapiPdf)

注意：如果 API 文档页面加载不出来，大概率是因为 API 文档资源文件对应的 CDN 提供商被政府封锁，可以尝试
[更换其他 CDN 提供商](https://apiflask.com/api-docs/#use-different-cdn-server-for-swagger-uiredoc-resources)，
或是 [使用本地资源](https://apiflask.com/api-docs/#serve-swagger-uiredoc-from-local-resources)。下面是设置自定义资源 URL 的示例（可直接复制使用）：

```py
# 放到程序实例定义下
app.config['SWAGGER_UI_BUNDLE_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.min.js'
app.config['SWAGGER_UI_CSS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css'
app.config['SWAGGER_UI_STANDALONE_PRESET_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-standalone-preset.min.js'
app.config['REDOC_STANDALONE_JS'] = 'https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js'
```

自动生成的 OpenAPI 规范文件可以在 <http://localhost:5000/openapi.json> 访问到。你也可以通过 [`flask spec` 命令](https://apiflask.com/openapi/#the-flask-spec-command) 获取：

```bash
$ flask spec
```

更多完整的示例程序见 [/examples](https://github.com/apiflask/apiflask/tree/main/examples)。


## 和 Flask 的关系

APIFlsak 是 Flask 之上的一层包装。你只需要记住下面几点区别（阅读 [从 Flask 迁移](https://apiflask.com/migrating) 了解更多细节）：

- 当创建程序实例时，使用 `APIFlask` 而不是 `Flask`。
- 当创建蓝本实例时，使用 `APIBlueprint` 而不是 `Blueprint`。
- 当创建类视图时，使用 `apiflask.views.MethodView` 而不是 `flask.views.MethodView`。
- APIFlask 提供的 `abort()` 函数（`apiflask.abort`）返回 JSON 错误响应。

下面的 Flask 程序：

```python
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'Human')
    return f'Hello, {escape(name)}'
```

转换到 APIFlask 只需要两步：

```python
from apiflask import APIFlask  # step one
from flask import request
from markupsafe import escape

app = APIFlask(__name__)  # step two

@app.route('/')
def hello():
    name = request.args.get('name', 'Human')
    return f'Hello, {escape(name)}'
```

简单来说，为了让使用 Flask 开发 Web API 更容易，APIFlask 提供了 `APIFlask` 和 `APIBlueprint` 来扩展 Flask 的 `Flask` 和 `Blueprint` 对象，并且添加了一些有用的功能函数。除了这些，你实际上是在使用 Flask。


## 和 marshmallow 的关系


APIFlask 接受 marshmallow schema 作为数据 schema，它使用 webargs 验证请求数据是否符合 schema 定义，并且使用 apispec 生成 schema 对应的 OpenAPI 表示。

你可以像以前那样构建 marshmallow schema。对于一些常用的 marshmallow 函数和类，你可以从 APIFlask 导入：

- `apiflask.Schema`：schema 基类。
- `apiflask.fields`：marshmallow 字段，包含来自 marshmallow、Flask-Marshmallow 和 webargs 的字段类。注意，别名字段（`Url`、`Str`、`Int`、`Bool` 等）已被移除。
- `apiflask.validators`：marshmallow 验证器投票为验证器相关的 API 使用更好的命名）。

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from marshmallow import pre_load, post_dump, ValidationError
```

## 致谢

APIFlask 基于 [APIFairy](https://github.com/miguelgrinberg/APIFairy) 改写，并且受到 [flask-smorest](https://github.com/marshmallow-code/flask-smorest) 和 [FastAPI](https://github.com/tiangolo/fastapi) 的启发（阅读 [对比和动机](https://apiflask.com/comparison) 了解这些项目之间的区别）。
