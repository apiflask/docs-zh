# OpenAPI 生成

[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（最初称为 Swagger 规范）是一个流行的 REST API 描述规范。APIFlask 内置支持 OpenAPI。本章将介绍在 APIFlask 中生成 OpenAPI 的基本用法。

!!! note "代码优先或设计优先"

    使用 OpenAPI 时有两种方法：代码优先和设计优先。APIFlask 当前仅支持代码优先的方法。它会在你编写代码后为你生成 OpenAPI spec 。我们计划在 1.0 版本发布后支持设计优先的方法。


## OpenAPI 支持的概览

APIFlask 从配置值、已注册的路由以及通过装饰器传递的信息中收集数据，然后基于这些信息生成 OpenAPI spec。

字段名称 | APIFlask 的生成方式 | 如何自定义
-----------|-----------------------------|---------------------
openapi    | - | 使用配置变量 [`OPENAPI_VERSION`](/configuration/#openapi_version)
info | - | 参见 *[元信息](#meta-information)*
servers | - | 使用配置变量 [`SERVERS`](/configuration/#servers)
paths | 根据路由和装饰器生成 | 使用 `input`、`output`、`doc` 装饰器和文档字符串
components | 从数据模式生成 | -
security | 根据认证对象生成安全信息 | 使用 `auth_required` 装饰器
tags | 根据蓝本名称生成 | 参见 *[标签](#tags)*
externalDocs | - | 使用配置变量 [`EXTERNAL_DOCS`](/configuration/#external_docs)

它提供了三种方式获取 spec 文档（规范文档，即 specification document，指存储 OpenAPI 规范的 JSON 或 YAML 文件，后文会简称为 spec）文件：

- 一个返回字典格式 spec 的 `app.spec` 属性。
- 一个提供 spec 的端点。
- 一个 `flask spec` 命令，用于将 spec 输出到标准输出或文件。

此外，它还提供了一个 `app.spec_processor` 装饰器，你可以使用它注册一个 spec 处理函数，在返回 spec 之前更新它。详情请参见 *[注册 spec 处理器](#register-a-spec-processor)*。


### 自动化行为

在从代码生成 OpenAPI spec 时，APIFlask 具有以下自动化行为：

- 从视图函数名称生成默认的 operation 摘要（summary）。
- 从视图函数的文档字符串生成默认的 operation 描述。
- 从蓝本名称生成标签。
- 为注册到应用程序的任何视图添加默认的 200 响应。
- 如果视图使用了 `app.input` 装饰器，则添加 422 响应。
- 如果视图使用了 `app.auth_required` 装饰器，则添加 401 响应。
- 如果视图的 URL 规则包含变量，则添加 404 响应。

所有这些自动化行为都可以通过 [相应的配置](/configuration/#automation-behavior-control) 禁用。


### spec 格式

OpenAPI spec 的默认格式是 JSON，同时也支持 YAML。如果你想启用 YAML 支持，请安装带有 `yaml` 额外依赖的 APIFlask（它会安装 `PyYAML`）：

```
$ pip install "apiflask[yaml]"
```

现在你可以通过 `SPEC_FORMAT` 配置更改格式：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['SPEC_FORMAT'] = 'yaml'
```

spec 端点的默认 URL 路径是 `/openapi.json`，如果你想使用 YAML 格式，也可以更新它：

```python hl_lines="3"
from apiflask import APIFlask

app = APIFlask(__name__, spec_path='/openapi.yaml')
app.config['SPEC_FORMAT'] = 'yaml'
```

`SPEC_FORMAT` 配置还会控制 `flask spec` 命令的 spec 格式输出。


### JSON spec 的缩进

当你通过 `/openapi.json` 从浏览器查看 spec 时，如果启用了调试模式或将配置变量 `JSONIFY_PRETTYPRINT_REGULAR` 设置为 `True`，缩进将设置为 `2`。否则，为了节省带宽和加快请求速度，JSON spec 将以无缩进和空格的形式发送。

本地 spec 文件的缩进默认启用。默认缩进值是 `LOCAL_SPEC_JSON_INDENT` 配置的默认值（即 `2`）。当你使用 `flask spec` 命令时，可以通过 `--indent` 或 `-i` 选项更改缩进。

YAML spec 的缩进始终为 `2`，目前无法更改。


## `app.spec` 属性

你可以通过 `app.spec` 属性以字典格式获取 spec 。它将始终返回最新的 spec ：

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

默认情况下，spec 以 JSON 格式提供，并可通过 URL 路径 `/openapi.json` 访问。你可以通过 `spec_path` 参数更改 spec 端点的 URL 规则：

```python
from apiflask import APIFlask

app = APIFlask(__name__, spec_path='/spec')
```

然后，spec 将可通过 http://localhost:5000/spec 访问。

!!! tip

    你可以通过配置变量 `YAML_SPEC_MIMETYPE` 和 `JSON_SPEC_MIMETYPE` 配置 spec 响应的 MIME 类型，详情请参见 [配置文档](/configuration#json_spec_mimetype)。


## `flask spec` 命令

!!! warning "版本 >= 0.7.0"

    此功能在 [版本 0.7.0](/changelog/#version-070) 中添加。

执行 `flask spec` 命令时，spec 将输出到标准输出：

```
$ flask spec
```

执行 `flask spec --help` 查看此命令的完整 API 参考：

```
$ flask spec --help
```

如果你已经执行了上述命令，可以跳过接下来的三个小节。


### 将 spec 输出到文件

如果使用 `--output` 或 `-o` 选项提供路径，APIFlask 将把 spec 写入到指定路径：

```
$ flask spec --output openapi.json
```

!!! warning "没有这样的文件或目录？"

    如果指定的路径不存在，你需要自行创建目录，APIFlask 将为你创建文件。

你还可以通过配置变量 `LOCAL_SPEC_PATH` 设置路径，当未传递 `--output/-o` 选项时，此值将用于 `flask spec` 命令：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
```

```
$ flask spec
```


### 更改 spec 格式

同样，可以通过 `--format` 或 `-f` 选项设置 spec 格式（默认为 `json`）：

```
$ flask spec --format json
```

你还可以通过配置变量 `SPEC_FORMAT`（默认为 `'json'`）设置格式，当未传递 `--format/-f` 选项时，此值将用于 `flask spec` 命令：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['SPEC_FORMAT'] = 'yaml'
```

```
$ flask spec
```


### 更改本地 JSON spec 的缩进

对于本地 spec 文件，缩进始终是必要的，以便于阅读和跟踪更改。可以通过 `--indent` 或 `-i` 选项设置缩进：

```
$ flask spec --indent 4
```

你还可以通过配置变量 `LOCAL_SPEC_JSON_INDENT`（默认为 `2`）设置缩进，当未传递 `--indent/-i` 选项时，此值将用于 `flask spec` 命令：

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
```

```
$ flask spec
```

### 抑制 spec 输出

!!! warning "版本 >= 2.1.1"

    此功能在 [版本 2.1.1](/changelog/#version-211) 中添加。

如果你希望将 spec 写入本地文件而不同时打印到标准输出，可以指定 `--quiet/-q` 选项：

```
$ flask spec --output openapi.json --quiet
```


## 保持本地 spec 同步

!!! warning "版本 >= 0.7.0"

    此功能在 [版本 0.7.0](/changelog/#version-070) 中添加。

通过 `flask spec` 命令，你可以轻松地将 spec 生成到本地文件中。如果希望 spec 文件与项目代码保持同步，可以设置配置 `LOCAL_SPEC_PATH` 的路径，然后通过将配置 `SYNC_LOCAL_SPEC` 设置为 `True` 来启用同步：

```python
from apiflask import APIFlask

app = APIFlask(__name__)

app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
```

!!! warning

    如果你传递的路径是相对路径，请不要在路径前加斜杠。

APIFlask 将在你当前的工作目录（执行 `flask run` 命令的目录）中创建文件。我们建议使用绝对路径。例如，你可以使用 `app.root_path`，它存储了应用模块的绝对根路径：

```python
from pathlib import Path

app = APIFlask(__name__)
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = Path(app.root_path) / 'openapi.json'
```

!!! tip

    你还可以使用 [`app.instance_path`](https://flask.palletsprojects.com/config/#instance-folders){target=_blank}，如果你的应用位于包中，它将非常有用，因为它返回位于项目根路径的实例文件夹路径。

或者使用 `os` 模块：

```python
import os

app = APIFlask(__name__)
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
```

如果你使用应用工厂并根据当前模块的 `__file__` 变量手动找到项目根路径，可以这样操作：

```python
from pathlib import Path

base_path = Path(__file__).parent
# 如果你的配置模块位于应用包中，可能需要使用以下代码：
# base_path = Path(__file__).parent.parent

SYNC_LOCAL_SPEC = True
LOCAL_SPEC_PATH = base_path / 'openapi.json'
```

或者使用 `os` 模块：

```python
import os

base_path = os.path.dirname(__file__)
# 如果你的配置模块位于应用包中，可能需要使用以下代码：
# base_path = os.path.dirname(os.path.dirname(__file__))

SYNC_LOCAL_SPEC = True
LOCAL_SPEC_PATH = os.path.join(base_path, 'openapi.json')
```

## 元信息

可以在创建 `APIFlask` 实例时通过参数设置 `title` 和 `version` 字段：

```python
from apiflask import APIFlask

app = APIFlask(__name__, title='我的 API', version='1.0')
```

`info` 对象中的其他字段可以通过以下配置变量设置：

- `DESCRIPTION`
- `TERMS_OF_SERVICE`
- `CONTACT`
- `LICENSE`

你还可以通过 [`INFO`](/configuration#info) 一次性设置以上四个字段。

有关详细信息，请参阅配置文档中的 [OpenAPI 字段](/configuration#openAPI-fields) 部分。


## 标签（tag）

默认情况下，`tag` 对象是基于蓝本自动生成的：

- 每个蓝本会生成一个标签，蓝本名称会被转换为标题形式作为标签名称。
- 蓝本下的所有路由会自动标记为对应的标签。

如果你希望为蓝本使用自定义标签名称或为标签添加更多详细信息，可以使用 `APIBlueprint(tag=...)` 参数传递新名称：

```python
from apiflask import APIBlueprint

bp = APIBlueprint('foo', __name__, tag='新名称')
```

此参数也接受一个字典：

```python
bp = APIBlueprint('foo', __name__, tag={'name': '新名称', 'description': '描述...'})
```

如果你不喜欢这种基于蓝本的标签系统，也可以手动设置。你可以通过配置变量 `TAGS` 传递一个标签名称列表：

```python
app.config['TAGS'] = ['foo', 'bar', 'baz']
```

如果需要为标签添加详细信息，也可以传递一个字典列表：

```python
app.config['TAGS'] = [
    {'name': 'foo', 'description': 'foo 的描述'},
    {'name': 'bar', 'description': 'bar 的描述'},
    {'name': 'baz', 'description': 'baz 的描述'}
]
```

!!! tip

    `app.tags` 属性等同于配置变量 `TAGS`，因此你也可以这样使用：

    ```python
    app.tags = ['foo', 'bar', 'baz']
    ```

设置了 `TAGS` 后，你可以使用 `doc` 装饰器为每个路由（OpenAPI operation）添加标签，详见 [Operation `tags`](#operation-tags)。


## path 和 operation

`path` 和 `operation` 对象中的大部分信息会根据你的视图函数或视图类自动生成，但你可能需要更改其中的一些内容。


### Operation `responses`

当你在视图函数上添加 `output` 装饰器时，会生成 operation 的 `responses`：

```python hl_lines="2"
@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    return pets[pet_id]
```

你可以通过 `output` 装饰器中的 `description` 和 `status_code` 参数设置描述和状态码（默认为 `200`）：

```python hl_lines="2"
@app.get('/pets/<int:pet_id>')
@app.output(PetOut, status_code=200, description='宠物的输出数据')
def get_pet(pet_id):
    return pets[pet_id]
```

operation 的 `responses` 对象具有以下自动化行为：

- 如果视图函数添加了 `input` 装饰器，APIFlask 会添加一个 `422` 响应。
- 如果视图函数添加了 `auth_required` 装饰器，APIFlask 会添加一个 `401` 响应。
- 如果视图函数仅使用路由装饰器，APIFlask 会添加一个默认的 `200` 响应。
- 如果路由 URL 包含变量（例如 `'/pets/<int:pet_id>'`），APIFlask 会添加一个 `404` 响应（版本 >= 0.8）。

你可以通过相关的 [配置变量](/configuration#automation-behavior-control) 禁用或配置这些行为。


### Operation 的 `requestBody` 和 `parameters`

当你在视图函数上添加 `input` 装饰器时，会生成 operation 的 `requestBody`：

```python hl_lines="2"
@app.post('/pets')
@app.input(PetIn)
def create_pet(pet_id):
    pass
```

如果你指定了请求数据的位置（非 `json`），则会生成 operation 的 `parameters`：

```python hl_lines="2"
@app.get('/pets')
@app.input(PetQuery, location='query')
def get_pets():
    pass
```

### Operation 的 `summary` 和 `description`

默认情况下，APIFlask 会使用视图函数的名称作为 operation 的摘要（`summary`）。如果你的视图函数名为 `get_pet`，那么 `summary` 将是 "Get Pet"。

如果视图函数有文档字符串（docstring），那么文档字符串的第一行将用作 `summary`，文档字符串中空行之后的内容将用作 `description`。

!!! note "设置 `summary` 的优先级"

    ```
    @app.doc(summary='自定义摘要') > 文档字符串的第一行 > 视图函数名称
    ```

以下是通过文档字符串设置 `summary` 和 `description` 的示例：

```python hl_lines="3 5"
@app.get('/hello')
def hello():
    """打招呼

    关于 /hello 的一些描述
    """
    return 'Hello'
```


### 响应和请求的 `schema`

APIFlask（通过 apispec）会根据你传递的数据模式生成 operation 的 `schema` 对象。

要为模式字段设置 OpenAPI 规范，可以通过 `metadata` 关键字传递一个字典：

```python
class PetIn(Schema):
    name = String(metadata={'description': '宠物的名字。'})
```

你可以在此 `metadata` 字典中传递 OpenAPI 模式字段名称作为键。目前支持以下字段：

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
- 任何以 `x-` 前缀开头的自定义字段

有关这些字段的详细信息，请参阅 [OpenAPI 文档](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#schemaObject)。

然而，大多数字段会在你设置模式字段时自动生成。例如，如果你将 `required` 设置为 `True`，并为 `validate` 传递一个 `Length(0, 10)` 验证器：

```python
from apiflask import Schema
from apiflask.fields import String

class PetIn(Schema):
    name = String(
        required=True,
        validate=Length(0, 10),
        metadata={'description': '宠物的名字。'}
    )
```

那么在最终的规范中，`type`、`maxLength`、`minLength` 和 `required` 字段将具有正确的值：

```json
"PetIn": {
    "properties": {
        "name": {
            "description": "宠物的名字。",
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

通常，你只需要通过 `metadata` 字典手动设置以下字段：

- `description`：此字段的一些描述。
- `title`：字段的标题。
- `example`：此字段的示例值（属性级别示例）。
- `deprecated`：如果为 true，表示此字段已弃用。
- `externalDocs`：指向此字段的外部文档的链接。
- `xml`：添加额外的元数据以描述此字段的 XML 表示格式。详情请参阅
*[OpenAPI XML 对象](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#xmlObject)*。

!!! tip

    如果模式类的名称以 `Schema` 结尾，那么在规范中将会被去掉。


### 响应和请求示例

在 API 文档中渲染规范时，文档工具会为你生成一个默认示例。如果你想添加自定义示例，可以使用 `example` 参数在 `input`/`output` 装饰器中传递一个字典作为响应的 `example`：

```python hl_lines="6"
from apiflask import APIFlask

app = APIFlask(__name__)

@app.post('/pets')
@app.input(PetIn, example={'name': 'foo', 'category': 'cat'})
def create_pet():
    pass
```

对于多个示例，可以使用 `examples` 参数并传递一个字典的字典，每个示例字典映射一个唯一名称：

```python hl_lines="17"
from apiflask import APIFlask

app = APIFlask(__name__)

examples = {
    '示例 foo': {
        'summary': 'foo 的示例',
        'value': {'name': 'foo', 'category': 'cat', 'id': 1}
    },
    '示例 bar': {
        'summary': 'bar 的示例',
        'value': {'name': 'bar', 'category': 'dog', 'id': 2}
    },
}

@app.get('/pets')
@app.output(PetOut, examples=examples)
def get_pets():
    pass
```

!!! warning

    目前，`input` 装饰器中的 `example`/`examples` 参数仅支持 JSON 请求体。如果需要为查询数据设置自定义示例，可以在数据模式中设置字段示例（属性级别示例）：

    ```python
    class PetQuery(Schema):
        name = String(metadata={'example': 'Flash'})
    ```

## 响应 `links`

!!! warning "版本 >= 0.10.0"

    此功能在 [版本 0.10.0](/changelog/#version-0100) 中添加。

你可以通过 `output` 装饰器中的 `links` 参数传递链接：

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
@app.output(PetOut, links=pet_links)
def new_pet():
    pass
```

或者，你也可以将链接添加到组件中，然后在操作中引用它：

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
@app.output(PetOut, links={'getAddressByUserId': {'$ref': '#/components/links/getAddressByUserId'}})
def new_pet():
    pass
```


## 响应 `headers`

!!! warning "版本 >= 2.1.0"

    此功能在 [版本 2.1.0](/changelog/#version-210) 中添加。

你可以在 `output` 装饰器中通过 `headers` 参数传递一个模式类：

```python
class Header(Schema):
    x_token = String(
        data_key='X-Token',
        metadata={'description': '一个自定义的 token 头'}
    )

@app.post('/pets')
@app.output(PetOut, headers=Header)
def new_pet():
    pass
```

当传递模式到 `headers` 时，你也可以使用字典而不是模式类：

```python
@app.post('/pets')
@app.output(PetOut, headers={'X-Token': String(metadata={'description': '一个自定义的 token 头'})})
def new_pet():
    pass
```


## 请求和响应的内容类型 / 媒体类型

对于请求，内容类型（media/content type）会根据输入的位置自动设置：

- `json`: `application/json`
- `form`: `application/x-www-form-urlencoded`
- `files`, `form_and_files`: `multipart/form-data`

对于响应，默认的内容类型是 `application/json`。你可以通过 `output()` 装饰器中的 `content_type` 参数（APIFlask >= 1.3.0）设置自定义内容类型：

```python
@app.post('/foo')
@app.output({FooSchema}, content_type='custom/type')
def get_foo():
    pass
```

!!! note

    为了与 Flask/Werkzeug 保持一致，我们使用 `content_type` 而不是 `media_type`。


## 文件响应

!!! warning "版本 >= 2.0.0"

    此功能在 [版本 2.0.0](/changelog/#version-0200) 中添加。

当你创建一个返回文件的端点时，应使用 `FileSchema`：

```python
from apiflask.schemas import FileSchema
from flask import send_from_directory

@app.get('/images/<filename>')
@app.output(FileSchema, content_type='image/png')
def get_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)
```

根据 OpenAPI 规范，如果文件格式是二进制的，可以省略模式，因此你也可以使用 `EmptySchema`：

```python
from apiflask.schemas import EmptySchema

@app.get('/images/<filename>')
@app.output(EmptySchema, content_type='image/png')
```

或者：

```python
@app.get('/images/<filename>')
@app.output({}, content_type='image/png')
```

你可以使用 `type` 和 `format` 设置自定义文件类型和格式（`binary` 和 `base64` 之一，默认为 `binary`）：

```python
@app.output(FileSchema(format='base64'), content_type='image/png')
```


## 使用 `doc` 装饰器

你还可以使用 `doc` 装饰器显式设置操作字段。


### Operation 的 `summary` 和 `description`

以下是使用 `doc` 装饰器设置 `summary` 和 `description` 的示例：

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.get('/hello')
@app.doc(summary='打招呼', description='关于 /hello 的一些描述')
def hello():
    return 'Hello'
```


### Operation 的 `tags`

当你在应用中使用蓝本时，APIFlask 提供了一个自动标签系统，详见 [标签](#tags)。

如果你没有使用蓝本，或者希望自己控制标签，则需要设置标签。`tags` 参数接受一个标签名称字符串的列表，这些名称应与 `TAGS` 配置或 `app.tags` 属性中传递的值匹配：

```python
@app.get('/')
@app.doc(tags=['Foo'])
def hello():
    return 'Hello'
```


### 为 operation 设置替代的 `responses`

如上所述，APIFlask 会根据你在视图函数上添加的装饰器（200、422、401、404）添加一些响应。有时你可能希望添加视图函数将返回的替代响应，此时可以使用 `@app.doc(responses=...)` 参数。它接受以下值：

- 一个状态码的整数列表，例如 `[404, 418]`。
- 一个格式为 `{<STATUS_CODE>: <DESCRIPTION>}` 的字典，这允许你为每个状态设置自定义描述，例如 `{404: '未找到', 418: 'Blah...'}`。如果已存在相同状态码的响应，则现有描述将被覆盖。

```python hl_lines="2"
@app.get('/')
@app.doc(responses=[204, 404])
def hello():
    return 'Hello'
```


### 为响应设置媒体类型（media type）

你可以为响应添加额外的媒体类型，这些媒体类型将被添加到 OpenAPI 文档中。这允许你描述在某些情况下可能返回资源的不同表示形式，例如通过执行基于请求某些参数的[内容协商][content_negotiation]。这可以通过提供自定义的 `responses` 并在每个响应的 `content` 部分中包含额外的媒体类型来实现，如下所示：

```python
@app.get("/pets/<int:pet_id>")
@app.input(Accept, location="headers")
@app.output(PetOut)
@app.doc(responses={
    200: {
        'description': '以 JSON 或 HTML 格式返回资源',
        'content': {
            'text/html': {}
        }
    }
})
def get_pet(pet_id, headers_data):
    pet = pets[pet_id]
    if "html" in headers_data.get('accept'):
        result = render_template('pets/pet-detail.j2.html', pet=pet)
    else:
        result = pet
    return result
```

上面的代码片段展示了如何检查请求的 `Accept` 头，然后返回资源的 HTML 表示或 JSON 表示。

请注意，APIFlask 允许你补充默认的 `application/json` 媒体类型（对于包含 `@app.output` 装饰器的视图，APIFlask 会自动添加此媒体类型），并添加额外的媒体类型。

[content_negotiation]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation


### 将 operation 标记为 `deprecated`

你可以使用 `deprecated` 参数将 operation 标记为已弃用：

```python hl_lines="2"
@app.get('/')
@app.doc(deprecated=True)
def hello():
    return 'Hello'
```


### 设置 `operationId`

!!! warning "版本 >= 0.10.0"

    此功能在 [版本 0.10.0](/changelog/#version-0100) 中添加。

你可以使用 `operation_id` 参数为视图函数（对应 operation）设置 `operationId`：

```python hl_lines="2"
@app.get('/')
@app.doc(operation_id='myCustomHello')
def hello():
    return 'Hello'
```

APIFlask 支持自动生成 `operationId`。默认情况下，自动生成行为是禁用的，你可以通过将以下配置变量设置为 `True` 来启用它：

```python
app.config['AUTO_OPERATION_ID'] = True
```

自动生成的 `operationId` 格式为 `{HTTP 方法}_{视图的端点}`（例如 `get_hello`）。


### Operation spec 扩展

!!! warning "版本 >= 2.2.0"

    此功能在 [版本 2.2.0](/changelog/#version-220) 中添加。

你可以使用 `extensions` 参数向 operation 对象添加自定义字段：

```python
@app.get('/')
@app.doc(extensions={'x-foo': 'bar'})
def hello():
    return 'Hello'
```

## 安全信息

APIFlask 将根据通过 `auth_required` 装饰器传递的认证对象生成 `security` 对象 operation 的 `security` 字段：

```python hl_lines="4 7"
from apiflask import APIFlask, HTTPTokenAuth, auth_required

app = APIFlask(__name__)
auth = HTTPTokenAuth()

@app.get('/')
@app.auth_required(auth)
def hello():
    return 'Hello'!
```

你可以使用 `description` 参数为认证对象设置描述：

```python hl_lines="4"
from apiflask import APIFlask, HTTPTokenAuth

app = APIFlask(__name__)
auth = HTTPTokenAuth(description='一些描述')
```

## 保护 OpenAPI 端点

如果你希望对 OpenAPI 端点应用身份验证或自定义处理逻辑，可以使用以下配置选项：`SPEC_DECORATORS`、`DOCS_DECORATORS` 和 `SWAGGER_UI_OAUTH_REDIRECT_DECORATORS`：

```python
app.config['SPEC_DECORATORS'] = [app.auth_required(auth)]
app.config['DOCS_DECORATORS'] = [app.auth_required(auth)]
```

查看完整示例：[examples/openapi/custom_decorators/app.py](https://github.com/apiflask/apiflask/tree/main/examples/openapi/custom_decorators/app.py)

## 禁用 OpenAPI 支持

### 全局禁用

如果你希望为整个应用禁用 OpenAPI 支持，可以在创建 `APIFlask` 实例时将 `enable_openapi` 参数设置为 `False`：

```python
from apiflask import APIFlask

app = APIFlask(__name__, enable_openapi=False)
```

!!! tip

    如果你只需要禁用 API 文档，请参阅
    *[全局禁用 API 文档](/api-docs/#disable-the-api-documentations-globally)*。


### 禁用特定蓝本

要从 API 文档（和 OpenAPI 规范）中隐藏蓝本，可以在创建 `APIBlueprint` 实例时将 `enable_openapi` 参数设置为 `False`：

```python
from apiflask import APIBlueprint

bp = APIBlueprint('foo', __name__, enable_openapi=False)
```

!!! tip

    如果蓝本是由其他 Flask 扩展创建的，APIFlask 将跳过该蓝本。


### 禁用特定视图函数

要从 API 文档（和 OpenAPI 规范）中隐藏视图函数，可以在 `doc` 装饰器中将 `hide` 参数设置为 `True`：

```python hl_lines="6"
from apiflask import APIFlask, doc

app = APIFlask(__name__)

@app.get('/secret')
@app.doc(hide=True)
def some_secret():
    return ''
```

!!! warning

    默认情况下，即使视图函数没有使用 `input`、`output` 和 `doc` 装饰器，APIFlask 也会将其添加到 API 文档（和 OpenAPI 规范）中。如果你希望禁用此行为，请将配置变量 `AUTO_200_RESPONSE` 设置为 `False`：

    ```python
    app.config['AUTO_200_RESPONSE'] = False
    ```


## 注册 spec 处理器

你可以使用 `app.spec_processor` 装饰器注册一个函数来更新 spec。回调函数应接受 spec 作为参数，并在最后返回它。生成 spec 文件时将调用回调函数。

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.spec_processor
def update_spec(spec):
    spec['info']['title'] = '更新后的标题'
    return spec
```

默认情况下，`spec` 参数是一个字典。当配置项 `SPEC_PROCESSOR_PASS_OBJECT` 设置为 `True` 时，`spec` 参数将是一个 [`apispec.APISpec`](https://apispec.readthedocs.io/en/latest/api_core.html#apispec.APISpec) 对象。

```python
from apiflask import APIFlask

app = APIFlask(__name__)
app.config['SPEC_PROCESSOR_PASS_OBJECT'] = True

class FooSchema(Schema):
    id = Integer()

@app.spec_processor
def update_spec(spec):
    spec.title = '更新后的标题'
    spec.components.schema('Foo', schema=FooSchema)  # 手动添加一个 schema
    return spec
```

查看 [示例应用程序](https://github.com/apiflask/apiflask/tree/main/examples/openapi/) 以了解 OpenAPI 支持，参阅 [示例页面](/examples) 以运行示例应用程序。
