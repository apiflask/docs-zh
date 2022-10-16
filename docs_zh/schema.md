# 数据 Schema

要了解编写输入和输出 schema 的基本方法，请移步「基本用法」章节的 [这两个部分](/usage/#use-appinput-to-validate-and-deserialize-request-data)。

这些是数据 schema 的几个基本概念：

- APIFlask schema = [marshmallow](https://github.com/marshmallow-code/marshmallow) schema.
- APIFlask 中的 `apiflask.Schema` 类是直接从 marshmallow 中导入的，具体请参阅 marshmallow 的
  [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html)。
- 我们建议你将输入与输出的 schema 分开来放，由于输出数据没有验证过程，你不用在输出的字段中定义验证器。
- `apiflask.fields` 包含了 marshmallow、webargs 与 flask-marshmallow 提供的所有字段（部分字段的别名被移除）。
- `apiflask.validators` 包含了 `marshmallow.validate` 提供的所有验证器。
- 对于其它函数与类，你只要直接从 marshmallow 导入即可。
- 如果你有时间，阅读一下 [marshmallow 文档](https://marshmallow.readthedocs.io/) 比较好。



## 反序列化（加载）与序列化（倾倒）

在 APIFlask（marshmallow）中，请求中输入数据的解析与验证过程被称作反序列化（我们在请求中**加载**了数据）。
相应地，将响应中的输出数据格式化的过程被称作序列化（我们把数据**倾倒**给了请求）。

请注意，我们使用了「加载」和「倾倒」两个词语来代表这两个过程。在创建 schema 的时候，我们用 `load_default` 参数设置
输入 schema 中每一个字段的默认值，相应地，输出 schema 的字段由 `dump_default` 参数设置。

下列四个装饰器可以注册加载与倾倒过程中的回调函数：

- `pre_load`：注册一个方法，该方法在解析与验证前调用。
- `post_load`：注册一个方法，该方法在解析与验证后调用。
- `pre_dump`：注册一个方法，该方法在视图函数返回值前调用。
- `post_dump`：注册一个方法，该方法在视图函数返回值后调用。

下列两个装饰器可以注册验证器方法：

- `validates(field_name)`：注册一个方法，来验证某个特定字段。
- `validates_schema`：注册一个方法，使得整个 schema 被验证。

!!! tips

    当你使用 `validates_schema` 的时候，请注意，`skip_on_field_errors` 的默认值是 `True`：
    > 如果 skip_on_field_errors=True，只要在验证字段的时候发现验证错误，这个验证方法将会被跳过。

你可以直接从 marshmallow 导入这些装饰器。

```python
from marshmallow import pre_load, post_dump, validates
```

要了解更多信息，请移步 marshmallow 文档的
 [这个章节](https://marshmallow.readthedocs.io/en/stable/extending.html) 与
 [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.decorators.html)。


## 数据字段

APIFlask 的 `apiflask.fields` 模块包含了 marshmallow、webargs、Flask-Marshmallow 提供的所有数据字段。
我们建议你从 `apiflask.fields` 导入它们。

```python
from apiflask.fields import String, Integer
```

或者这样，如果你喜欢保留引用：

```python
from apiflask import Schema, fields

class FooBarSchema(Schema):
    foo = fields.String()
    bar = fields.Integer()
```

!!! warning "部分字段的别名被移除"

    下列字段别名被移除：

    - `Str`
    - `Int`
    - `Bool`
    - `Url`
    - `UrlFor`
    - `AbsoluteUrlFor`

    相反，你需要使用下列名称代替它们：

    - `String`
    - `Integer`
    - `Boolean`
    - `URL`
    - `URLFor`
    - `AbsoluteURLFor`

    要了解更多信息，请参阅 [apiflask#63](https://github.com/apiflask/apiflask/issues/63) 和
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


### Flask-Marshmallow 字段

API 文档：<https://flask-marshmallow.readthedocs.io/en/latest/#flask-marshmallow-fields>

- `AbsoluteURLFor`
- `Hyperlinks`
- `URLFor`


### webargs 字段

API 文档：<https://webargs.readthedocs.io/en/latest/api.html#module-webargs.fields>

- `DelimitedList`
- `DelimitedTuple`


### APIFlask 字段

API 文档：<https://apiflask.com/api/fields/#apiflask.fields.File>

- `File`

!!! tips

    如果已经存在的字段并没有满足你的需求，你也可以创建
    [自定义字段](https://marshmallow.readthedocs.io/en/stable/custom_fields.html).


## 数据验证器

APIFlask 的 `aipflask.validators` 模块包含了 marshmallow 提供的所有验证器：

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

要了解具体用法，参见 marshmallow 的 [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html)。

当你指定一个字段的验证器的时候，你可以给 `validate` 参数传递单个验证器：

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import OneOf


class PetInSchema(Schema):
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

或者也可以传递一个验证器组成的列表

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    category = String(required=True, validate=[OneOf(['dog', 'cat']), Length(0, 10)])
```


!!! tips

    如果已经存在的字段并没有满足你的需求，你也可以创建
    [自定义字段](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation).


## Schema 名称解析器

!!! warning "需要 0.9.0 以上版本"

    这个功能在 [版本 0.9.0](/changelog/#version-090) 中添加。

OpenAPI 中每一个 schema 的名称都是基于一个函数解析而来，这里是 APIFlask 默认的 schema 名称解析函数：

```python
def schema_name_resolver(schema):
    name = schema.__class__.__name__  # get schema class name
    if name.endswith('Schema'):  # remove the "Schema" suffix
        name = name[:-6] or name
    if schema.partial:  # add a "Update" suffix for partial schema
        name += 'Update'
    return name
```

你可以通过设定 `APIFlask.schema_name_resolver` 来提供一个自定义的 schema 名称解析函数。

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

schema 的名称解析函数应该接收一个 schema 对象作为参数，并返回名称。

## 自定义基本的响应 schema

!!! warning "需要 0.9.0 以上版本"

    这个功能在 [版本 0.9.0](/changelog/#version-090) 中添加。

当你通过 `output` 装饰器设定一个视图函数的输出时，你需要返回一个对象或字典，其符合传递至 `output` 装饰器的 schema。
接下来，APIFlask 将会将返回值序列化到响应体：

```python
{
    "id": 2,
    "name": "Kitty",
    "category": "cat"
}
```

然而，你可能想要将输出数据插入到某个数据字段，然后添加一些元字段。这样你就可以给每一个端点返回一个统一的响应。
例如，将所有响应统一成下面的格式：

```python
{
    "data": {
        "id": 2,
        "name": "Kitty",
        "category": "cat"
    },
    "message": "some message",
    "status_code": "custom code"
}
```

要实现这个，你需要设定一个基本的响应 schema，然后把它传递到配置变量 `BASE_RESPONSE_SCHEMA` 中：

```python
from apiflask import APIFlask, Schema
from apiflask.fields import String, Integer, Field

app = APIFlask(__name__)

class BaseResponseSchema(Schema):
    message = String()
    status_code = Integer()
    data = Field()  # the data key

app.config['BASE_RESPONSE_SCHEMA'] = BaseResponseSchema
```

默认的数据键是 `data`，你可以通过配置变量 `BASE_RESPONSE_DATA_KEY` 把它换成别的，来迎合你的数据字段名称：

```python
app.config['BASE_RESPONSE_DATA_KEY '] = 'data'
```

现在，你可以在视图函数中返回一个符合基本 schema 的字典。

```python
@app.get('/')
def say_hello():
    data = {'name': 'Grey'}
    return {'message': 'Success!', 'status_code': 200, 'data': data}
```

如果要把代码变得优雅一点，你可以创建一个制作响应字典的函数：

```python
def make_resp(message, status_code, data):
    return {'message': message, 'status_code': status_code, 'data': data}


@app.get('/')
def say_hello():
    data = {'message': 'Hello!'}
    return make_resp('Success!', 200, data)


@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    if pet_id > len(pets) - 1 or pets[pet_id].get('deleted'):
        abort(404)
    return make_resp('Success!', 200, pets[pet_id])
```

要了解更多信息，你可以查看「[完整的示例应用](https://github.com/apiflask/apiflask/tree/main/examples/base_response/app.py)」，要运行这些示例应用，请访问「[示例应用](/examples)」页面。
