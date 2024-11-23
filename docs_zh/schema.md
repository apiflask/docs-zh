# 数据模式

请先阅读基础使用章节中[这一节](/usage/#use-appinput-to-validate-and-deserialize-request-data)及后续内容来了解编写输入输出模式的基础知识。

数据模式的基本概念：

- APIFlask 的 `apiflask.Schema` 基类直接从 marshmallow 导入，带有一些细微改动，详见 [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html) 。
- 我们建议分开定义输入和输出模式。由于输出数据不需要验证，因此无需在输出字段上定义验证器。
- `apiflask.fields` 包含了 marshmallow、webargs 和 flask-marshmallow 提供的所有字段（某些别名已被移除）。
- `apiflask.validators` 包含 `marshmallow.validate` 中的所有验证器。
- 对于其他函数/类，直接从 marshmallow 导入即可。
- 建议在空闲时阅读[marshmallow](https://marshmallow.readthedocs.io/) 的文档 。

## 反序列化（load）和序列化（dump）

在 APIFlask（marshmallow）中，解析和验证输入请求数据的过程称为反序列化（我们从请求中 **load** 数据）。而格式化输出响应数据的过程称为序列化（我们将数据 **dump** 到响应中）。

注意我们使用 "load" 和 "dump" 来表示这两个过程。创建模式时，我们使用 `load_default` 参数为输入模式中的字段设置默认值，使用 `dump_default` 参数为输出模式中的字段设置默认值。

有四个装饰器用于在 load/dump 过程中注册回调方法：

- `pre_load`：注册在解析/验证请求数据之前调用的方法
- `post_load`：注册在解析/验证请求数据之后调用的方法
- `pre_dump`：注册在格式化视图函数返回值之前调用的方法
- `post_dump`：注册在格式化视图函数返回值之后调用的方法

还有两个装饰器用于注册验证方法：

- `validates(field_name)`：注册验证指定字段的方法
- `validates_schema`：注册验证整个模式的方法

!!! tip

    使用 `validates_schema` 时，注意 `skip_on_field_errors` 默认设为 `True`：
    > 如果 skip_on_field_errors=True，当验证字段时检测到验证错误时，这个验证方法将被跳过。

直接从 marshmallow 导入这些装饰器：

```python
from marshmallow import pre_load, post_dump, validates
```

详细用法请参阅[这一章节](https://marshmallow.readthedocs.io/en/stable/extending.html) 和这些装饰器的 [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.decorators.html) 。

## 数据字段

APIFlask 的 `apiflask.fields` 模块包含了来自 marshmallow、webargs 和 Flask-Marshmallow 的所有数据字段。我们建议从 `apiflask.fields` 模块导入它们：

```python
from apiflask.fields import String, Integer
```

或者你也可以这样引用：

```python
from apiflask import Schema, fields

class FooBar(Schema):
    foo = fields.String()
    bar = fields.Integer()
```

!!! warning "部分字段别名已被移除"

    以下字段别名已被移除：

    - `Str`
    - `Int`
    - `Bool`
    - `Url`
    - `UrlFor`
    - `AbsoluteUrlFor`

    请改用：

    - `String`
    - `Integer`
    - `Boolean`
    - `URL`
    - `URLFor`
    - `AbsoluteURLFor`

    详见 [apiflask#63](https://github.com/apiflask/apiflask/issues/63) 和
    [marshmallow#1828](https://github.com/marshmallow-code/marshmallow/issues/1828)。

### marshmallow 字段

API 文档：<https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html>

- `AwareDateTime`
- `Boolean`
- `Constant`
- `Date`
- `DateTime`
- `Decimal`
- `Dict`
- `Email`
- `Field`
- `Float`
- `Function`
- `Integer`
- `IP`
- `IPv4`
- `IPv6`
- `List`
- `Mapping`
- `Method`
- `NaiveDateTime`
- `Nested`
- `Number`
- `Pluck`
- `Raw`
- `String`
- `Time`
- `TimeDelta`
- `Tuple`
- `URL`
- `UUID`

## Flask-Marshmallow 字段

API 文档：<https://flask-marshmallow.readthedocs.io/en/latest/#flask-marshmallow-fields>

- `AbsoluteURLFor`
- `Hyperlinks`
- `URLFor`

## webargs 字段

API 文档：<https://webargs.readthedocs.io/en/latest/api.html#module-webargs.fields>

- `DelimitedList`
- `DelimitedTuple`

## APIFlask 字段

API 文档：<https://apiflask.com/api/fields/#apiflask.fields.File>

- `File`

!!! tip

    如果现有字段不能满足你的需求，你也可以创建[自定义字段](https://marshmallow.readthedocs.io/en/stable/custom_fields.html)。
## 数据验证器

APIFlask 的 `apiflask.validators` 包含了 marshmallow 提供的所有验证器类：

- `ContainsNoneOf`
- `ContainsOnly`
- `Email`
- `Equal`
- `Length`
- `NoneOf`
- `OneOf`
- `Predicate`
- `Range`
- `Regexp`
- `URL`
- `Validator`

详细用法请参阅 [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html)。

为字段指定验证器时，你可以向 `validate` 参数传递单个验证器：

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import OneOf


class PetIn(Schema):
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

或传递一个验证器列表：

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    category = String(required=True, validate=[OneOf(['dog', 'cat']), Length(0, 10)])
```

!!! tip

    如果现有验证器不能满足你的需求，你也可以创建[自定义验证器](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation)。

## 模式名称解析器

!!! warning "Version >= 0.9.0"

    此功能在 [0.9.0 版本](/changelog/#version-090)中添加。

每个模式的 OpenAPI 模式名称都基于解析器函数来解析，以下是 APIFlask 中使用的默认模式名称解析器：

```python
def schema_name_resolver(schema):
    name = schema.__class__.__name__  # 获取模式类名
    if name.endswith('Schema'):  # 移除 "Schema" 后缀
        name = name[:-6] or name
    if schema.partial:  # 为部分模式添加 "Update" 后缀
        name += 'Update'
    return name
```

你可以通过设置 `APIFlask.schema_name_resolver` 属性来提供自定义的模式名称解析器：

```python hl_lines="14"
from apiflask import APIFlask


def my_schema_name_resolver(schema):
    name = schema.__class__.__name__
    if name.endswith('Schema'):
        name = name[:-6] or name
    if schema.partial:
        name += 'Partial'
    return name


app = APIFlask(__name__)
app.schema_name_resolver = my_schema_name_resolver
```

模式名称解析器应该接受模式对象作为参数并返回名称。

## 基础响应模式自定义

!!! warning "Version >= 0.9.0"

    此功能在 [0.9.0 版本](/changelog/#version-090)中添加。

当你使用 `output` 装饰器设置视图函数的输出时，你需要返回与传递给 `output` 装饰器的模式相匹配的对象或字典。然后，APIFlask 会将返回值序列化到响应体中：

```python
{
    "id": 2,
    "name": "Kitty",
    "category": "cat"
}
```

然而，你可能希望将输出数据插入到一个 data 字段中，并添加一些元数据字段。这样你就可以为所有端点返回统一的响应。例如，让所有响应采用以下格式：

```python
{
    "data": {
        "id": 2,
        "name": "Kitty",
        "category": "cat"
    },
    "message": "some message",
    "code": "custom code"
}
```

要实现这一点，你需要设置一个基础响应模式，然后将其传递给配置变量 `BASE_RESPONSE_SCHEMA`：

```python
from apiflask import APIFlask, Schema
from apiflask.fields import String, Integer, Field

app = APIFlask(__name__)

class BaseResponse(Schema):
    data = Field()  # data 键
    message = String()
    code = Integer()

app.config['BASE_RESPONSE_SCHEMA'] = BaseResponse
```

默认的 data 键是 "data"，你可以通过配置变量 `BASE_RESPONSE_DATA_KEY` 将其更改为与你的模式中的数据字段名称相匹配：

```python
app.config['BASE_RESPONSE_DATA_KEY'] = 'data'
```

现在你可以在视图函数中返回与基础响应模式相匹配的字典：

```python
@app.get('/')
def say_hello():
    data = {'name': 'Grey'}
    return {
        'data': data,
        'message': 'Success!',
        'code': 200
    }
```

查看[完整示例应用](https://github.com/apiflask/apiflask/tree/main/examples/base_response/app.py) 了解更多详情，运行示例应用请参阅[示例页面](/examples) 。

## 使用 dataclass 作为数据模式

借助 [marshmalow-dataclass](https://github.com/lovasoa/marshmallow_dataclass) ,你可以定义 dataclass 然后将其转换为 marshmallow 模式。

```bash
$ pip install marshmallow-dataclass
```

你可以使用 marshmallow-dataclass 中的 `dataclass` 装饰器来创建数据类，然后调用 `.Schema` 属性获取相应的 marshmallow 模式：

```python
from dataclasses import field

from apiflask import APIFlask
from apiflask.validators import Length, OneOf
from marshmallow_dataclass import dataclass


app = APIFlask(__name__)


@dataclass
class PetIn:
    name: str = field(
        metadata={'required': True, 'validate': Length(min=1, max=10)}
    )
    category: str = field(
        metadata={'required': True, 'validate': OneOf(['cat', 'dog'])}
    )


@dataclass
class PetOut:
    id: int
    name: str
    category: str


@app.post('/pets')
@app.input(PetIn.Schema)
@app.output(PetOut.Schema, status_code=201)
def create_pet(pet: PetIn):
    return {
        'id': 0,
        'name': pet.name,
        'category': pet.category
    }
```

查看[完整示例应用](https://github.com/apiflask/apiflask/tree/main/examples/dataclass/app.py) 了解更多详情。运行示例应用请参阅[示例页面](/examples)。

阅读 [mashmallow-dataclass 的文档](https://lovasoa.github.io/marshmallow_dataclass/html/marshmallow_dataclass.html) 和 [dataclasses](https://docs.python.org/3/library/dataclasses.html) 了解更多信息。
