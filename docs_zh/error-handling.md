# 错误处理

APIFlask 中的错误处理基于以下基本概念：

- 默认情况下，所有自动抛出的错误（404、405、500）响应都将采用 JSON 格式。
- 所有错误都建立在基本异常类 [`HTTPError`](/api/exceptions/#apiflask.exceptions.HTTPError) 之上。
- 使用 `APIFlask.abort()` 函数或抛出 `HTTPError` 类来生成一个错误响应。
- 使用 `app.error_processor`（`app` 是 `apiflask.APIFlask` 的一个实例）来注册一个自定义的错误响应处理器。
- 使用 `auth.error_processor` （`auth`是`apiflask.HTTPBasicAuth`或 `apiflask.HTTPTokenAuth` 的
  一个实例）来注册一个自定义的认证错误响应处理器。
- 子类化 `HTTPError` 来创建自定义的错误类。

!!! tip

    为处理特定的 HTTP 错误而使用 `app.errorhandler` 注册的错误处理器优先级高于使用 `app.error_processor`
    注册的自定义错误响应处理器。


## JSON 错误响应

Flask 会对 400/404/405/500 错误生成默认的错误响应。这个错误响应采用 HTML 格式，并带有默认的错误信息和描述。
但在 APIFlask 中，这些错误都将以 JSON 格式返回，并带有以下的预设字段：

- `message`：HTTP 原因短语或自定义的错误描述。
- `detail`：空字典（404/405/500）或校验请求时产生的详细错误信息（400）。

你可以在创建 APIFlask 实例时使用 `json_errors` 参数来控制这个行为，`json_errors` 的默认值为 `True`。

```python
from apiflask import APIFlask

# 这将会关闭自动返回 JSON 错误响应的特性
app = APIFlask(__name__, json_errors=False)
```

如需自定义错误响应的主体，可以使用 `app.error_processor` 装饰器来注册自定义的错误处理器。
详见 [这一节](error-handling/#自定义错误响应处理器)。


## 使用 `abort` 和 `HTTPError` 生成错误响应

在视图函数中有两种方式可以中止请求处理过程并返回错误响应：

- 调用 `abort` 函数

和在普通的 Flask 视图函数中所做的一样，只不过这个 `abort` 函数是由 APIFlask 提供：

```python
from apiflask import abort


@app.route('/')
def hello():
    abort(400, message='Something is wrong...')
    return 'Hello, world!'  # 这一行将不会被执行到
```

它会在幕后抛出一个 `HTTPError`，所以 `abort` 和 `HTTPError` 会接收相同的参数（见下文）。

- 抛出 `HTTPError` 类

抛出 `HTTPError` 将会做相同的事情：

```python
from apiflask import HTTPError


@app.route('/')
def hello():
    raise HTTPError(400, message='Something is wrong...')
    return 'Hello, world!'  # 这一行将不会被执行到
```

这个调用将生成如下的错误响应：

```json
{
    "message": "Something is wrong...",
    "detail": {}
}
```

所有可以传递给 `abort` 和 `HTTPError` 的参数，参阅
[`HTTPError 的 API 文档`](/api/exceptions/#apiflask.exceptions.HTTPError)。

如果想向响应主体中添加更多字段，可以使用 `extra_data` 参数，例如：

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

这将产生如下的响应：

```json
{
    "message": "Something is wrong...",
    "detail": {},
    "docs": "http://example.com",
    "error_code": 1234
}
```

在大多数情况下，应该使用预设值来创建自定义错误类，而不是直接将它们传递给 `abort` 或
`HTTPError`。详见下一节。


## 自定义错误类

!!! warning "Version >= 0.11.0"

    这个特性在 [版本 0.11.0](/changelog/#version-0110) 中加入。

你可以使用预设的错误信息创建自定义错误类来重用 API 错误。这个自定义错误类应该继承自
`HTTPError`，在这个错误类中可以使用以下属性：

- status_code
- message
- detail
- extra_data
- headers

这是个简单的示例：

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

之后可以在视图函数中 `raise` 这个异常类：

```python hl_lines="5"
@app.get('/pets/<pet_id>')
def get_pet(pet_id):
    pets = [1, 2, 3]
    if pet_id not in pets:
        raise PetNotFound
    return {'message': 'Pet'}
```

!!! tip "使用 Werkzeug 中的异常类"

    如果在创建 `app` 实例时没有将 `json_errors` 设置为 `False`，
    APIFlask 将捕获所有 Werkzeug 异常，包括被直接抛出的异常：

    ```python
    from werkzeug.exceptions import NotFound

    @app.get('/')
    def say_hello():
        if user is None:
            raise NotFound
        return {'message': 'Hello!'}
    ```

    但是，这个异常的 `description` 和 `body` 将被丢弃。


## 自定义错误状态码和描述

下面的配置变量可用于自定义请求校验和认证错误：

- `VALIDATION_ERROR_DESCRIPTION`
- `AUTH_ERROR_DESCRIPTION`
- `VALIDATION_ERROR_STATUS_CODE`
- `AUTH_ERROR_STATUS_CODE`

详见配置文档中 [自定义响应](/configuration#自定义响应) 章节。


## 自定义错误响应处理器

你可以使用 `app.error_processor` 装饰器来注册自定义错误响应处理器函数。
它是一个全局错误处理器，会处理所有的 HTTP 错误。

在以下情境下，被装饰的回调函数将被调用：

- 当 `APIFlask(json_errors=True)`（默认情况）时，有任何 Flask 抛出的 HTTP 异常。
- 解析请求时发生校验错误。
- 使用 [`HTTPError`][apiflask.exceptions.HTTPError] 触发的异常。
- 使用 [`abort`][apiflask.exceptions.abort] 触发的异常。

你仍然可以使用 `app.errorhandler(code_or_exection)` 装饰器来为特定的异常或错误状态码注册错误处理器。
在这种情况下，这些错误处理器的返回值将用作相应错误或异常发生时的响应。

回调函数必须接受一个错误对象作为参数，并返回一个有效响应：

```python
from apiflask import APIFlask

app = APIFlask(__name__)


@app.error_processor
def my_error_processor(error):
    return {
        'status_code': error.status_code,
        'message': error.message,
        'detail': error.detail
    }, error.status_code, error.headers
```

这个错误对象是 [`HTTPError`][apiflask.exceptions.HTTPError] 的一个实例，
因此可以通过其属性来获取错误信息：

- status_code：如果这个错误是由请求校验错误触发的，该值将是 400（默认）或是配置
  `VALIDATION_ERROR_STATUS_CODE` 的值。如果这个错误是由
  [`HTTPError`][apiflask.exceptions.HTTPError] 或 [`abort`][apiflask.exceptions.abort]
  触发，该值将是传入的状态码。其他情况下，该值将是 `Werkzueg` 处理请求时设置的状态码。
- message：这个错误的描述，由你手动传入或是从 Werkzeug 中获取。
- detail：这个错误的其他详细信息。当请求校验错误触发时，它将是下面的结构：

    ```python
    "<location>": {
        "<field_name>": ["<error_message>", ...],
        "<field_name>": ["<error_message>", ...],
        ...
    },
    "<location>": {
        ...
    },
    ...
    ```

    `location` 的值会是 `json`（即请求主体）、`query`（即查询字符串）或其他值，这取决于请求校验错误发生的位置
    (它匹配你在 `app.input` 装饰器传入的 `location` 参数值)。

- headers：在 `HTTPError` 或是 `abort` 中设置的值，默认为 `{}` 。
- extra_data：通过 `HTTPError` 或 `abort` 传入的额外错误信息。

如果你想的话，可以将整个响应主体重写为任何你喜欢的格式：

```python
@app.error_processor
def my_error_processor(error):
    body = {
        'error_message': error.message,
        'error_detail': error.detail,
        'status_code': error.status_code
    }
    return body, error.status_code, error.headers
```

!!! tip

    建议在响应中保留 `error.detail` 数据，因为它包含请求校验错误的详细信息。

在更改错误响应后，为了让 API 文档能正确匹配自定义错误响应的 schema，
还必须更新该错误响应对应的 OpenAPI schema（见下一节）。


## 更新错误响应的 OpenAPI Schema

APIFlask 中有两种用于错误的 schema：一种用于一般错误（包括认证错误），另一种用于请求校验错误。
可以依次由 `HTTP_ERROR_SCHEMA` 和 `VALIDATION_ERROR_SCHEMA` 进行配置。

!!! question "为什么在错误响应中需要两种 schema？"

    给请求校验错误的响应设置一个单独的 schema 背后的原因是为了保证校验错误中的 `detail` 字段始终有值。
    对于一般的 HTTP 错误，除非手动通过 `HTTPError` 和 `abort` 传入了一些内容，否则 `detail` 字段将会是空值。

当使用 `app.error_processor` 更改错误响应的主体时，还需要更新错误响应的 schema，如此它将更新错误响应的
OpenAPI spec。其中 schema 可以是一个 OpenAPI schema 的字典形式，也可以是一个 marshmallow 的 schema 类。
下面是一个将 `status_code` 字段添加到默认错误响应并重命名现有字段的示例（使用 OpenAPI schema 字典形式）：

```python
# 使用内置的 `validation_error_detail_schema` 作为 `detail` 字段的值
from apiflask import APIFlask
from apiflask.schemas import validation_error_detail_schema


# 一般错误响应的 schema，包括认证错误
http_error_schema = {
    "properties": {
        "error_detail": {
            "type": "object"
        },
        "error_message": {
            "type": "string"
        },
        "status_code": {
            "type": "integer"
        }
    },
    "type": "object"
}


# 请求校验错误的响应 schema
validation_error_schema = {
    "properties": {
        "error_detail": validation_error_detail_schema,
        "error_message": {
            "type": "string"
        },
        "status_code": {
            "type": "integer"
        }
    },
    "type": "object"
}

app = APIFlask(__name__)
app.config['VALIDATION_ERROR_SCHEMA'] = validation_error_schema
app.config['HTTP_ERROR_SCHEMA'] = http_error_schema
```


## 处理认证错误

在创建 APIFlask 实例时将 `json_errors` 设置为 `True` 时（默认即为 `True`），APIFlask 会针对认证错误返回
JSON 格式的错误，并调用内置的错误回调或通过 `app.error_processor` 创建的错误处理器。

对于以下情况，你需要为认证错误注册一个单独的错误处理器：

- 如果想对 401/403 错误做一些额外的处理，但不想使用`app.errorhandler(401)` 或
  `app.errorhandler(403)` 注册特定的错误处理器，这时就必须使用 `auth.error_processor`
  来注册一个认证错误处理器。
- 如果已将 `json_errors` 设置为 `False`，但还想自定义错误响应，由于全局错误处理器将不被使用，
  这时就得注册一个自定义的认证错误处理器。

你可以使用 `auth.error_processor` 装饰器来注册一个认证错误处理器。它的用法很像 `app.error_processor`：

```python
from apiflask import HTTPTokenAuth

auth = HTTPTokenAuth()


@auth.error_processor
def my_auth_error_processor(error):
    body = {
        'error_message': error.message,
        'error_detail': error.detail,
        'status_code': error.status_code
    }
    return body, error.status_code, error.headers
```

如果在 `json_error` 为 `True` 时注册了认证错误处理器，那么它将覆盖全局错误处理器。

!!! question "为什么需要一个单独的错误处理器来处理认证错误？"

    APIFlask 的认证功能由 Flask-HTTPAuth 提供。由于 Flask-HTTPAuth 对其错误使用了单独的错误处理函数，
    APIFlask 必须添加单独的错误处理器来处理它。将来我们可能会想出一个简单的方式来解决这个问题。
