# 数据 Schema

要了解编写输入和输出 schema 的基本方法，请移步「基本用法」章节的 [这两个部分](/usage/#use-appinput-to-validate-and-deserialize-request-data)。

这些是数据 schema 的几个基本概念：

- APIFlask schema = [marshmallow](https://github.com/marshmallow-code/marshmallow) schema.
- APIFlask 中的 `apiflask.Schema` 基类是直接从 marshmallow 中导入的，具体参见 marshmallow 的
  [API 文档](https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html)
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

- `validates(field_name)`: to register a method to validate a specified field
- `validates_schema`: to register a method to validate the whole schema

!!! tips

    When using the `validates_schema`, notice the `skip_on_field_errors` is set to `True` as default:
    > If skip_on_field_errors=True, this validation method will be skipped whenever validation errors
    > have been detected when validating fields.

Import these decorators directly from marshmallow:

```python
from marshmallow import pre_load, post_dump, validates
```

See [this chapter](https://marshmallow.readthedocs.io/en/stable/extending.html) and the
[API documentation](https://marshmallow.readthedocs.io/en/stable/marshmallow.decorators.html)
of these decorators for the details.


## Data fields

APIFlask's `apiflask.fields` module includes all the data fields from marshmallow, webargs, and
Flask-Marshmallow. We recommend importing them from the `apiflask.fields` module:

```python
from apiflask.fields import String, Integer
```

Or you prefer to keep a reference:

```python
from apiflask import Schema, fields

class FooBarSchema(Schema):
    foo = fields.String()
    bar = fields.Integer()
```

!!! warning "Some field aliases were removed"

    The following field aliases were removed:

    - `Str`
    - `Int`
    - `Bool`
    - `Url`
    - `UrlFor`
    - `AbsoluteUrlFor`

    Instead, you will need to use:

    - `String`
    - `Integer`
    - `Boolean`
    - `URL`
    - `URLFor`
    - `AbsoluteURLFor`

    See [apiflask#63](https://github.com/apiflask/apiflask/issues/63) and
    [marshmallow#1828](https://github.com/marshmallow-code/marshmallow/issues/1828)for more details.


### marshmallow fields

API documentation: <https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html>

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


## Flask-Marshmallow fields

API documentation: <https://flask-marshmallow.readthedocs.io/en/latest/#flask-marshmallow-fields>

- `AbsoluteURLFor`
- `Hyperlinks`
- `URLFor`


## webargs fields

API documentation: <https://webargs.readthedocs.io/en/latest/api.html#module-webargs.fields>

- `DelimitedList`
- `DelimitedTuple`


## APIFlask fields

API documentation: <https://apiflask.com/api/fields/#apiflask.fields.File>

- `File`

!!! tips

    If the existing fields don't fit your needs, you can also create
    [custom fields](https://marshmallow.readthedocs.io/en/stable/custom_fields.html).


## Data validators

APIFlask's `aipflask.validators` contains all the validator class provided by marshmallow:

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

See the [API documentation](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html)
for the detailed usage.

When specifying validators for a field, you can pass a single validator to the `validate` parameter:

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import OneOf


class PetInSchema(Schema):
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

Or pass a list of validators:

```python
from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    category = String(required=True, validate=[OneOf(['dog', 'cat'], Length(0, 10)]))
```

!!! tips

    If the existing validators don't fit your needs, you can also create
    [custom validators](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation).


## Schema name resolver

!!! warning "Version >= 0.9.0"

    This feature was added in the [version 0.9.0](/changelog/#version-090).

The OpenAPI schema name of each schema is resolved based on a resolver function, here is
the default schema name resolver used in APIFlask:

```python
def schema_name_resolver(schema):
    name = schema.__class__.__name__  # get schema class name
    if name.endswith('Schema'):  # remove the "Schema" suffix
        name = name[:-6] or name
    if schema.partial:  # add a "Update" suffix for partial schema
        name += 'Update'
    return name
```

You can provide a custom schema name resolver by setting the `APIFlask.schema_name_resolver`
attribute:

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

The schema name resolver should accept the schema object as argument and return the name.


## Base response schema customization

!!! warning "Version >= 0.9.0"

    This feature was added in the [version 0.9.0](/changelog/#version-090).

When you set up the output of a view function with the `output` decorator, you need to
return the object or dict that matches the schema you passed to the `output` decorator. Then,
APIFlask will serialize the return value to response body:

```python
{
    "id": 2,
    "name": "Kitty",
    "category": "cat"
}
```

However, You may want to insert the output data into a data field and add some meta fields.
So that you can return a unified response for all endpoints. For example, make all the
responses to the following format:

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

To achieve this, you will need to set a base response schema, then pass it to the configuration variable
`BASE_RESPONSE_SCHEMA`:

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

The default data key is "data", you can change it to match your data field name in your schema
via the configuration variable `BASE_RESPONSE_DATA_KEY`:

```python
app.config['BASE_RESPONSE_DATA_KEY '] = 'data'
```

Now you can return a dict matches the base response schema in your view functions:

```python
@app.get('/')
def say_hello():
    data = {'name': 'Grey'}
    return {'message': 'Success!', 'status_code': 200, 'data': data}
```

To make it more elegant, you can create a function to make response dict:

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

Check out [the complete example application](https://github.com/apiflask/apiflask/tree/main/examples/base_response/app.py)
for more details, see [the examples page](/examples) for running the example application.
