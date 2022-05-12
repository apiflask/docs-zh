
![](https://apiflask.com/_assets/apiflask-logo.png)

# APIFlask 中文文档

[![Build status](https://github.com/apiflask/apiflask/workflows/build/badge.svg)](https://github.com/apiflask/apiflask/actions) [![codecov](https://codecov.io/gh/apiflask/apiflask/branch/main/graph/badge.svg?token=2CFPCZ1DMY)](https://codecov.io/gh/apiflask/apiflask)


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
- Swagger UI and Redoc (api-docs.md)
- Configuration (configuration.md)
- Error Handling (error-handling.md)
- Examples (examples.md)
- Comparison and Motivations (comparison.md)
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


## APIFlask 介绍

APIFlask is a lightweight Python web API framework based on [Flask](https://github.com/pallets/flask) and [marshmallow-code](https://github.com/marshmallow-code) projects. It's easy to use, highly customizable, ORM/ODM-agnostic, and 100% compatible with the Flask ecosystem.

With APIFlask, you will have:

- More sugars for view function (`@app.input()`, `@app.output()`, `@app.get()`, `@app.post()` and more)
- Automatic request validation and deserialization (with [webargs](https://github.com/marshmallow-code/webargs))
- Automatic response formatting and serialization (with [marshmallow](https://github.com/marshmallow-code/marshmallow))
- Automatic [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) (OAS, formerly Swagger Specification) document generation (with [apispec](https://github.com/marshmallow-code/apispec))
- Automatic interactive API documentation (with [Swagger UI](https://github.com/swagger-api/swagger-ui) and [Redoc](https://github.com/Redocly/redoc))
- API authentication support (with [Flask-HTTPAuth](https://github.com/miguelgrinberg/flask-httpauth))
- Automatic JSON response for HTTP errors


## Requirements

- Python 3.7+
- Flask 1.1.0+


## Installation

For Linux and macOS:

```bash
$ pip3 install apiflask
```

For Windows:

```bash
> pip install apiflask
```


## Links

- Website: <https://apiflask.com>
- Documentation: <https://apiflask.com/docs>
- PyPI Releases: <https://pypi.python.org/pypi/APIFlask>
- Change Log: <https://apiflask.com/changelog>
- Source Code: <https://github.com/apiflask/apiflask>
- Issue Tracker: <https://github.com/apiflask/apiflask/issues>
- Discussion: <https://github.com/apiflask/apiflask/discussions>
- Twitter: <https://twitter.com/apiflask>


## Example

```python
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get('/')
def say_hello():
    # returning a dict equals to use jsonify()
    return {'message': 'Hello!'}


@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    if pet_id > len(pets) - 1:
        abort(404)
    # you can also return an ORM/ODM model class instance directly
    # APIFlask will serialize the object into JSON format
    return pets[pet_id]


@app.patch('/pets/<int:pet_id>')
@app.input(PetInSchema(partial=True))
@app.output(PetOutSchema)
def update_pet(pet_id, data):
    # the validated and parsed input data will
    # be injected into the view function as a dict
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]
```

Notice: The `input`, `output`, `doc`, and `auth_required` decorators are now bound
to application/blueprint instances, use standalone decorators if you are still using
APIFlask < 0.12, see [here](https://apiflask.com/usage/#move-to-new-api-decorators)
for more details.

<details>
<summary>You can also use class-based views with <code>MethodView</code></summary>

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


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


# use the "route" decorator to decorate the view class
@app.route('/')
class Hello(MethodView):

    # use HTTP method name as class method name
    def get(self):
        return {'message': 'Hello!'}


@app.route('/pets/<int:pet_id>')
class Pet(MethodView):

    @app.output(PetOutSchema)
    def get(self, pet_id):
        """Get a pet"""
        if pet_id > len(pets) - 1:
            abort(404)
        return pets[pet_id]

    @app.input(PetInSchema(partial=True))
    @app.output(PetOutSchema)
    def patch(self, pet_id, data):
        """Update a pet"""
        if pet_id > len(pets) - 1:
            abort(404)
        for attr, value in data.items():
            pets[pet_id][attr] = value
        return pets[pet_id]
```
</details>

<details>
<summary>Or use <code>async def</code> with Flask 2.0</summary>

```bash
$ pip install -U flask[async]
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

See <em><a href="https://flask.palletsprojects.com/async-await">Using async and await</a></em> for the details of the async support in Flask 2.0.

</details>

Save this as `app.py`, then run it with :

```bash
$ flask run --reload
```

Now visit the interactive API documentation (Swagger UI) at <http://localhost:5000/docs>:

![](https://apiflask.com/_assets/swagger-ui.png)

Or you can visit the alternative API documentation (Redoc) at <http://localhost:5000/redoc>:

![](https://apiflask.com/_assets/redoc.png)

The auto-generated OpenAPI spec file is available at <http://localhost:5000/openapi.json>. You can also get the spec with [the `flask spec` command](https://apiflask.com/openapi/#the-flask-spec-command):

```bash
$ flask spec
```

For some complete examples, see [/examples](https://github.com/apiflask/apiflask/tree/main/examples).


## Relationship with Flask

APIFlask is a thin wrapper on top of Flask. You only need to remember four differences (see *[Migrating from Flask](https://apiflask.com/migrating)* for more details):

- When creating an application instance, use `APIFlask` instead of `Flask`.
- When creating a blueprint instance, use `APIBlueprint` instead of `Blueprint`.
- The `abort()` function from APIFlask (`apiflask.abort`) returns JSON error response.
- The view class should be registered with the `route` decorator.

For a minimal Flask application:

```python
from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'Human')
    return f'Hello, {escape(name)}'
```

Now change to APIFlask:

```python
from apiflask import APIFlask  # step one
from flask import request, escape

app = APIFlask(__name__)  # step two

@app.route('/')
def hello():
    name = request.args.get('name', 'Human')
    return f'Hello, {escape(name)}'
```

In a word, to make Web API development in Flask more easily, APIFlask provides `APIFlask` and `APIBlueprint` to extend Flask's `Flask` and `Blueprint` objects and it also ships with some helpful utilities. Other than that, you are actually using Flask.


## Relationship with marshmallow

APIFlask accepts marshmallow schema as data schema, uses webargs to validate the request data against the schema, and uses apispec to generate the OpenAPI representation from the schema.

You can build marshmallow schemas just like before, but APIFlask also exposes some marshmallow APIs for convenience (it's optional, you can still import everything from marshamallow directly):

- `apiflask.Schema`: The base marshmallow schema class.
- `apiflask.fields`: The marshmallow fields, contain the fields from both marshmallow and Flask-Marshmallow. Beware that the aliases (`Url`, `Str`, `Int`, `Bool`, etc.) were removed (vote in [marshmallow #1828](https://github.com/marshmallow-code/marshmallow/issues/1828) to remove these aliases from marshmallow).
- `apiflask.validators`: The marshmallow validators (vote in [marshmallow #1829](https://github.com/marshmallow-code/marshmallow/issues/1829) for better names for validate-related APIs in marshmallow).

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from marshmallow import pre_load, post_dump, ValidationError
```

## Credits

APIFlask starts as a fork of [APIFairy](https://github.com/miguelgrinberg/APIFairy) and is inspired by [flask-smorest](https://github.com/marshmallow-code/flask-smorest) and [FastAPI](https://github.com/tiangolo/fastapi) (see *[Comparison and Motivations](https://apiflask.com/comparison)* for the comparison between these projects).
