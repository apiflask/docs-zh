# OpenAPI 支持

[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（起初被称作 Swagger 规范）是 REST API 的一个热门的描述规范。
APIFlask 对它有内置的支持。这个章节将会介绍在 APIFlask 中生成 OpenAPI 的基本用法。

!!! note "代码优先还是设计优先"

    使用 OpenAPI 的方法有两种：代码优先和设计优先。APIFlask 目前只支持第一种。在你写完代码之后，APIFlask
    会为你生成 OpenAPI spec。我们将会在 1.0 版本之后尝试支持设计优先的方法。


## OpenAPI 支持概览

APIFlask 先收集来自配置、注册的路径，还有你在装饰器中传递的信息，然后基于这些信息生成 OpenAPI spec。

字段名称 | APIFlask 如何生成  | 如何自定义
------- |------------------|------------------
openapi    | - | 使用配置变量 [`OPENAPI_VERSION`](/configuration/#openapi_version)
info | - | 请阅读 [元信息](#meta-information)
servers | - | 使用配置变量 [`SERVERS`](/configuration/#servers)
paths | 基于路径与装饰器生成 | 使用 `input`, `output`, `doc` 装饰器，以及文档字符串
components | 从数据 schema 生成 | -
security | 从安全验证对象生成安全信息 | 使用 `auth_required` 装饰器
tags | 从蓝图名称生成 | 见 [标签](#tags)
externalDocs | - | 使用配置变量 [`EXTERNAL_DOCS`](/configuration/#external_docs)

APIFlask 提供三种获得 spec 文档文件的方法：

- 一个返回字典 spec 的 `app.spec` 属性。
- 一个为 spec 提供服务的端点。
- 一个将 spec 输出到文件或标准输出的 `flask spec` 命令。

另外，APIFlask 也提供了一个你可以注册在返回值前更新 spec 的 spec 处理器的 `app.spec_processor` 装饰器，
要了解更多信息，请移步 [注册一个 spec 处理器](#register-a-spec-processor)。


### spec 格式

默认的 OpenAPI spec 格式是 JSON，但 YAML 也有提供支持。如果你希望启用 YAML 支持，请
安装 APIFlask 的时候一并安装 `yaml` 额外依赖包：

```
$ pip install apiflask[yaml]
```

现在，你可以通过配置变量 `SPEC_FORMAT` 来更改格式：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['SPEC_FORMAT'] = 'yaml'
```

spec 端点的默认 URL 路径是 `/openapi.json`，你可能还希望在使用 YAML 格式时更新路径：

```python hl_lines="3"
from apiflask import APIFlask

app = APIFlask(__name__, spec_path='/openapi.yaml')
app.config['SPEC_FORMAT'] = 'yaml'
```

`SPEC_FORMAT` 配置变量还会控制 `flask spec` 命令中的 spec 格式输出。


### JSON spec 的缩进

当你从浏览器通过 `/openapi.json` 查看 spec 的时候，假如你启用了调试模式，或者将
配置变量 `JSONIFY_PRETTYPRINT_REGULAR` 设置为 `True`，缩进空格将会设置为 `2`。
否则，JSON spec 会以无缩进，无空格的形式被输出，以节省带宽和加快请求速度。

本地 spec 文件的缩进默认启用。默认的缩进就是变量 `LOCAL_SPEC_JSON_INDENT`
 的默认值，也就是 `2`。当你使用 `flask spec` 命令时，你可以用 `--indent`
 或 `-i` 选项来改变缩进的空格数。

YAML spec 的缩进始终是 `2`，而且目前不能更改。


## `app.spec` 属性

你可以通过 `app.spec` 属性得到一个字典。它始终会返回最新的 spec：

```python
>>> from apiflask import APIFlask
>>> app = APIFlask(__name__)
>>> app.spec
{'info': {'title': 'APIFlask', 'version': '0.1.0'}, 'tags': [], 'paths': OrderedDict(), 'openapi': '3.0.3'}
>>> @app.get('/')
... def hello():
...     return {'message': 'Hello'}
...
>>> app.spec
{'info': {'title': 'APIFlask', 'version': '0.1.0'}, 'tags': [], 'paths': OrderedDict([('/', {'get': {'parameters': [], 'responses': OrderedDict([('200', {'content': {'application/json': {'schema': {}}}, 'description': 'Successful response'})]), 'summary': 'Hello'}})]), 'openapi': '3.0.3'}
>>>
```


## spec 端点

默认情况下，spec 符合 JSON 格式，且可以在 URL 路径 `/openapi.json` 中获得，
你可以使用 `spec_path` 参数来更换 spec 端点的 URL 规则：

```python
from apiflask import APIFlask

app = APIFlask(__name__, spec_path='/spec')
```

然后你可以在 http://localhost:5000/spec 得到 spec。

!!! tip

    你可以用配置变量 `YAML_SPEC_MIMETYPE` 与 `JSON_SPEC_MIMETYPE` 自定义 spec 响应的
     MIME 类型，在 [配置](/configuration#json_spec_mimetype) 中了解更多信息。


## `flask spec` 命令

!!! warning "Version >= 0.7.0"

    该功能在 [版本 0.7.0](/changelog/#version-070) 中添加。

当你执行 `flask spec` 命令时，它将会把 spec 输出到标准输出：

```
$ flask spec
```

通过 `flask spec --help` 查看该命令的完整 API 参考：

```
$ flask spec --help
```

假如你执行了上面的命令，以下三个部分你可以跳过。


### 将 spec 输出到文件

假如你为选项 `--option` 或 `-o` 提供了路径，APIFlask 将会在提供的路径中写入 spec：

```
$ flask spec --output openapi.json
```

!!! note "指定的文件或目录不存在？"

    假如指定的路径不存在，你必须手动创建目录，然后 APIFlask 将会为你创建文件。

你也可以通过配置变量 `LOCAL_SPEC_PATH` 来设置路径，假如 `--output/-o` 选项没有
被传递，`flask spec` 命令将会使用它的值：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
```

```
$ flask spec
```


### 更改 spec 格式

类似地，spec 格式可以通过 `--format` or `-f` 选项改变（默认是 `json`）：

```
$ flask spec --format json
```

你也可以通过配置变量 `SPEC_FORMAT`（默认是 `json`）来设定格式，假如 `--format/-f` 选项没有
被传递，`flask spec` 命令将会使用它的值：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['SPEC_FORMAT'] = 'yaml'
```

```
$ flask spec
```


### 更改本地 JSON spec 的缩进

对于本地的 spec 文件，为了可读性且方便追踪更改，缩进总是必要的。通过 `--indent` 或者 `-i`
 选项可以设置缩进：

```
$ flask spec --indent 4
```

你也可以通过配置变量 `LOCAL_SPEC_JSON_INDENT`（默认是 `2`）来设置缩进，当
 `--indent/-i` 选项没有传递时，`flask spec` 命令将会使用它的值：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
```

```
$ flask spec
```


## 同步本地 spec

!!! warning "Version >= 0.7.0"

    该功能在 [版本 0.7.0](/changelog/#version-070) 中添加。

通过 `flask spec` 命令，你可以轻松在本地文件生成 spec。
假如 spec 文件与项目的源码同步的话，生成的工作将会很方便。
要实现这个，你需要在配置变量 `LOCAL_SPEC_PATH` 中设定一个路径，
然后通过将 `SYNC_LOCAL_SPEC` 设为 `True` 来启用同步。

```python
from apiflask import APIFlask

app = APIFlask(__name__)

app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
```

!!! warning

    假如传递的路径是相对路径，别在开头加斜杠。

APIFlask 将会在你运行 `flask run` 命令时，在当前的工作目录下创建文件，我们推荐你使用绝对路径，
例如，你可以使用储存了 app 模块绝对路径的 `app.root_path`。

```python
from pathlib import Path

app = APIFlask(__name__)
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = Path(app.root_path) / 'openapi.json'
```

!!! tip

    你也可以使用
    [`app.instance_path`](https://flask.palletsprojects.com/config/#instance-folders){target=_blank},
    假如你的应用被包含在一个包内，这个很有用，因为它会返回根目录下 instance 文件夹的绝对路径。

或者使用 `os` 模块:

```python
import os

app = APIFlask(__name__)
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
```

当你使用应用工厂函数时，你也可以根据当前模块的 `__file__` 变量找到项目的根目录。
在这种情况下，你可以在根目录下 `config.py` 文件中正常放入配置数据。

```
- my_project/ -> 项目文件夹
  - app/ -> 应用包
  - config.py -> 配置文件
```

这样，你就可以找到根目录：

```python
from pathlib import Path

base_path = Path(__file__).parent
# you may need to use the following if your config module is
# inside the application package:
# base_path = Path(__file__).parent.parent

SYNC_LOCAL_SPEC = True
LOCAL_SPEC_PATH = base_path / 'openapi.json'
```

或者使用 `os` 模块：

```python
import os

base_path = os.path.dirname(__file__)
# you may need to use the following if your config module is
# inside the application package:
# base_path = os.path.dirname(os.path.dirname(__file__))

SYNC_LOCAL_SPEC = True
LOCAL_SPEC_PATH = os.path.join(base_path, 'openapi.json')
```


## 元信息

创建 `APIFlask` 示例时，可以传递 `title` 与 `version` 字段：

```python
from apiflask import APIFlask

app = APIFlask(__name__, title='My API', version='1.0')
```

`info` 对象中其它字段可以通过下列配置变量支持：

- `DESCRIPTION`
- `TERMS_OF_SERVICE`
- `CONTACT`
- `LICENSE`

你也可以直接用 [`INFO`](/configuration#info) 设置四个字段。

具体请参阅配置文档中 [OpenAPI 字段](/configuration#openAPI-fields) 部分。


## 标签

默认来说，`tag` 对象会基于蓝图自动生成：

- 一个蓝图生成一个标签，蓝图名称中每一个单词首字母大写处理，
得到的就是标签的名称。
- 蓝图下所有路径将会被自动标记相应的标签。

如果你想要自定义蓝图的标签名称或者想要给标签添加更多信息，你可以使用
 `APIBlueprint(tag=...)` 参数来传递一个新名称：

```python
from apiflask import APIBlueprint

bp = APIBlueprint(__name__, 'foo', tag='New Name')
```

This parameter also accepts a dict:

```python
bp = APIBlueprint(__name__, 'foo', tag={'name': 'New Name', 'description': 'blah...'})
```

假如你不喜欢这种基于蓝图的标签系统，你当然可以手动操作。
你可以向配置变量 `TAGS` 传递一个标签名列表，就像这样：

```python
app.config['TAGS'] = ['foo', 'bar', 'baz']
```

这个变量同时也支持接收一个字典组成的列表，假如说你希望为标签添加更多信息：

```python
app.config['TAGS'] = [
    {'name': 'foo', 'description': 'The description of foo'},
    {'name': 'bar', 'description': 'The description of bar'},
    {'name': 'baz', 'description': 'The description of baz'}
]
```

!!! tip

    `app.tags` 属性等价于配置变量 `TAGS`，因此你也可以使用：

    ```python
    app.tags = ['foo', 'bar', 'baz']
    ```

当 `TAGS` 的值被设置后，你可以用 `doc` 装饰器为每一个路径加入标签（OpenAPI 操作），具体见 [`tags` 操作](#operation-tags)。


## 路径项目与操作

`path` 与 `operation` 对象中大部分的信息是自动从你的视图函数/视图类中自动生成的，
而你可能希望去更改其中一部分。


### `responses` 操作

当你为视图函数添加 `output` 装饰器后，会生成 `responses` 操作：

```python hl_lines="2"
@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    return pets[pet_id]
```

你可以通过 `output` 装饰器中相应的参数设置 `description` 与 `status_code`（默认是 200）

```python hl_lines="2"
@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema, status_code=200, description='Output data of a pet')
def get_pet(pet_id):
    return pets[pet_id]
```

`responses` 操作有以下自动行为：

- 假如 `input` 加入了视图函数，APIFlask 将会添加 `400` 响应。
- 假如 `auth_required` 装饰器加入了视图函数，APIFlask 将会添加 `401` 响应。
- 假如视图函数只用了路径装饰器，APIFlask 会添加一个默认的 `200` 响应。
- （需要 0.8 以上版本）假如路径的 URL 包含变量（例如：`'/pets/<int:pet_id>'`），APIFlask 将会添加一个 `404` 响应。

你可以通过更改相关的 [配置变量](/configuration#automation-behavior-control) 来禁用，或者自定义这些行为。


### `requestBody` 与 `parameters` 操作

当你在视图函数中加入 `input` 装饰器时，APIFlask 将会生成 `requestBody` 操作。

```python hl_lines="2"
@app.post('/pets')
@app.input(PetInSchema)
def create_pet(pet_id):
    pass
```

当你使用不同于 `json` 的位置指定一个请求时，APIFlask 会生成 `parameters` 操作，而不是 `requestBody`。

```python hl_lines="2"
@app.get('/pets')
@app.input(PetQuerySchema, location='query')
def get_pets():
    pass
```


### `summary` 和 `description` 操作

默认来说，APIFlask 会使用视图函数的名称作为 summary 操作。
假如你的视图函数叫做 `get_pet`，`summary` 将会是「Get Pet」。

假如视图函数有文档字符串，那么文档字符串的第一行将会被用作 `summary`，空行之后的其它行将会作为 `description`。

!!! note "The precedence of summary setting"

    ```
    @app.doc(summary='blah') > the first line of docstring > the view function name
    ```

Here is an example of set `summary` and `description` with docstring:

```python hl_lines="3 5"
@app.get('/hello')
def hello():
    """Say hello

    Some description for the /hello
    """
    return 'Hello'
```


### Response and request `schema`

APIFlask (with apispec) will generate the operation `schema` object from the data schema
you passed.

To set the OpenAPI spec for schema fields, you can pass a dict with the `metadata` keyword:

```python
class PetInSchema(Schema):
    name = String(metatdata={'description': 'The name of the pet.'})
```

You can pass the OpenAPI schema field name as the key in this metadata dict. Currently,
the following fields are supported:

- `format`
- `title`
- `description`
- `default`
- `multipleOf`
- `maximum`
- `exclusiveMaximum`
- `minimum`
- `exclusiveMinimum`
- `maxLength`
- `minLength`
- `pattern`
- `maxItems`
- `minItems`
- `uniqueItems`
- `maxProperties`
- `minProperties`
- `required`
- `enum`
- `type`
- `items`
- `allOf`
- `properties`
- `additionalProperties`
- `readOnly`
- `writeOnly`
- `xml`
- `externalDocs`
- `example`
- `nullable`
- `deprecated`
- Any custom field starts with `x-` prefix

See the details of these fields at
[OpenAPI docs](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#schemaObject).

However, most of these fields will be generated when you set up the schema field.
For example, if you set `required` to `True`, pass a `Length(0, 10)` validator
to `validate`:

```python
from apiflask import Schema
from apiflask.fields import String

class PetInSchema(Schema):
    name = String(
        required=True,
        validate=Length(0, 10),
        metatdata={'description': 'The name of the pet.'}
     )
```

Then in the final spec, the `type`, `maxLength`, `minLength` and `required` field will have
the right value:

```json
"PetIn": {
    "properties": {
        "name": {
            "description": "The name of the pet.",
            "maxLength": 10,
            "minLength": 0,
            "type": "string"
        }
    },
    "required": [
        "name"
    ],
    "type": "object"
}
```

Normally, you only need to set the following fields manually with the `metadata` dict:

- `description`: Some description for this field.
- `title`: The title of the field.
- `example`: A example value for this field (property-level example).
- `deprecated`: If true, indicates this field is deprecated.
- `externalDocs`: A link points to the external documentation for this field.
- `xml`: Adds additional metadata to describe the XML representation format of this field.
See details in
*[OpenAPI XML object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#xmlObject)*.

!!! tip

    If the schema class' name ends with `Schema`, then it will be striped in the spec.


### Response and request example

When rendering the spec in the API documentation, the docs tool will generate a default
example for you. If you want to add a custom example, you can use the `example` parameter to pass a dict as the response `example` in the `input`/`output` decorator:

```python hl_lines="6"
from apiflask import APIFlask, input

app = APIFlask(__name__)

@app.post('/pets')
@app.input(PetInSchema, example={'name': 'foo', 'category': 'cat'})
def create_pet():
    pass
```

For multiple examples, use the `examples` parameter and pass a dict of dict, every
example dict maps a unique name:

```python hl_lines="17"
from apiflask import APIFlask, output

app = APIFlask(__name__)

examples = {
    'example foo': {
        'summary': 'an example of foo',
        'value': {'name': 'foo', 'category': 'cat', 'id': 1}
    },
    'example bar': {
        'summary': 'an example of bar',
        'value': {'name': 'bar', 'category': 'dog', 'id': 2}
    },
}

@app.get('/pets')
@app.output(PetOutSchema, examples=examples)
def get_pets():
    pass
```

!!! note

    Currently, the `example`/`examples` parameter in the `input` decorator is only
    support JSON body. When you need to set a custom example for query data,
    you can set the field example (property-level example) in the data schema:

    ```python
    class PetQuerySchema(Schema):
        name = String(metadata={'example': 'Flash'})
    ```


## Response `links`

!!! warning "Version >= 0.10.0"

    This feature was added in the [version 0.10.0](/changelog/#version-0100).

You can pass the links with `links` keyword in the `output` decorator:

```python
pet_links = {
    'getAddressByUserId': {
        'operationId': 'getUserAddress',
        'parameters': {
            'userId': '$request.path.id'
        }
    }
}

@app.post('/pets')
@app.output(PetOutSchem, links=pet_links)
def new_pet(data):
    pass
```

Or you can also add links to components then reference it in operation:

```python
links = {
    'getAddressByUserId': {
        'operationId': 'getUserAddress',
        'parameters': {
            'userId': '$request.path.id'
        }
    }
}

@app.spec_processor
def update_spec(spec):
    spec['components']['links'] = links
    return spec


@app.post('/pets')
@app.output(PetOutSchem, links={'getAddressByUserId': {'$ref': '#/components/links/getAddressByUserId'}})
def new_pet(data):
    pass
```


## Use the `doc` decorator

There is also a `doc` decorator that can be used to set operation fields explicitly.


### Operation `summary` and `description`

Here is the example of using the `doc` decorator to set `summary` and `description`:

```python hl_lines="6"
from apiflask import APIFlask, doc

app = APIFlask(__name__)

@app.get('/hello')
@app.doc(summary='Say hello', description='Some description for the /hello')
def hello():
    return 'Hello'
```


### Operation `tags`

When you are using blueprints in your application, APIFlask provides an automatic tagging system,
see [Tags](#tags) for more details.

You only need to set the tag if you are not using a blueprint or you want to control the tags by
yourself. The `tags` parameter accepts a list of tag name string, they should match the values you
passed in `TAGS` config or `app.tags` attribute:

```python hl_lines="2"
@app.get('/')
@app.doc(tags=['Foo'])
def hello():
    return 'Hello'
```


### Alternative operation `responses`

As described above, APIFlask will add some responses based on the decorators you added
on the view function (200, 400, 401, 404). Sometimes you may want to add alternative
responses the view function will return, then you can use the `@app.doc(responses=...)`
parameter, it accepts the following values:

- A list of status code int, for example, `[404, 418]`.
- A dict in a format of `{<STATUS_CODE>: <DESCRIPTION>}`, this will allow you to
set a custom description for each status, for example,
`{404: 'Not Found', 418: 'Blah...'}`. If a response with the same status code is
already exist, the existing description will be overwritten.

```python hl_lines="2"
@app.get('/')
@app.doc(responses=[204, 404])
def hello():
    return 'Hello'
```


### Mark an operation as `deprecated`

You can mark an operation as deprecated with the `deprecated` parameter:

```python hl_lines="2"
@app.get('/')
@app.doc(deprecated=True)
def hello():
    return 'Hello'
```


### Set `operationId`

!!! warning "Version >= 0.10.0"

    This feature was added in the [version 0.10.0](/changelog/#version-0100).

You can set `operationId` for a view funtion (operation) with the `operation_id` parameter:

```python hl_lines="2"
@app.get('/')
@app.doc(operation_id='myCustomHello')
def hello():
    return 'Hello'
```

APIFlask supports to generate operationId automatically. The auto-generating behavior is disabled
as default, you can enable it by setting the following configuration variable to `True`:

```python
app.config['AUTO_OPERATION_ID'] = True
```

The auto-operationId will in the format of `{HTTP method}_{endpoint of the view}` (e.g. `get_hello`).


## Security information

APIFlask will generate the `security` object and operation `security` field based on
the auth object passed with the `auth_required` decorator:

```python hl_lines="4 7"
from apiflask import APIFlask, HTTPTokenAuth, auth_required

app = APIFlask(__name__)
auth = HTTPTokenAuth()

@app.get('/')
@app.auth_required(auth)
def hello():
    return 'Hello'!
```

You can use the `description` parameter to set the description for auth objects:

```python hl_lines="4"
from apiflask import APIFlask, HTTPTokenAuth

app = APIFlask(__name__)
auth = HTTPTokenAuth(description='some description')
```


## Disable the OpenAPI support


### Disable globally

If you want to disable the whole OpenAPI support for the whole application, you
can set `enable_openapi` parameter to `False` when creating the `APIFlask` instance:

```python
from apiflask import APIFlask

app = APIFlask(__name__, enable_openapi=False)
```

!!! tip

    If you only need to disable the API documentation, see
    *[Disable the API documentations globally](/api-docs/#disable-the-api-documentations-globally)*.


### Disable for specific blueprints

To hide blueprints from API documentations (and OpenAPI spec), you can
set `enable_openapi` parameter to `False` when creating the `APIBlueprint` instance:

```python
from apiflask import APIBlueprint

bp = APIBlueprint(__name__, 'foo', enable_openapi=False)
```

!!! tip

    APIFlask will skip a blueprint if the blueprint is created by other Flask
    extensions.


### Disable for specific view functions

To hide a view function from API documentations (and OpenAPI spec), you
can set the `hide` parameter to `True` in the `doc` decorator:

```python hl_lines="6"
from apiflask import APIFlask, doc

app = APIFlask(__name__)

@app.get('/secret')
@app.doc(hide=True)
def some_secret():
    return ''
```

!!! note

    By default, APIFlask will add a view function into API documentations
    (and OpenAPI spec) even if the view function doesn't use `input`, `output`,
    and `doc` decorator. If you want to disable this behavior, set configruration
    variable `AUTO_200_RESPONSE` to `False`:

    ```python
    app.config['AUTO_200_RESPONSE'] = False
    ```


## Register a spec processor

You can register a function with the `app.spec_processor` decorator to update the
spec. The callback function should accept the spec as an argument and return it
in the end. The callback function will be called when generating the spec file.

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.spec_processor
def update_spec(spec):
    spec['info']['title'] = 'Updated Title'
    return spec
```

Notice the format of the spec depends on the value of the configuration
variable `SPEC_FORMAT` (defaults to `'json'`):

- `'json'` -> dict
- `'yaml'` -> string

Check out [the example application](https://github.com/apiflask/apiflask/tree/main/examples/openapi/app.py)
for OpenAPI support, see [the examples page](/examples) for running the example application.
