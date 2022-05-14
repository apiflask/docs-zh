# 错误处理

APIFlask 中的错误处理基于以下基本观念：

- 默认情况下，所有自动抛出的错误（404、405、500）都将采用 JSON 格式。
- 所有错误都建立在基本异常类  [`HTTPError`](/api/exceptions/#apiflask.exceptions.HTTPError) 之上。
- 使用 `APIFlask.abort()` 函数或者抛出 `HTTPError` 类来生成一个错误响应。
- 使用 `app.error_processor`（`app` 是 `apiflask.APIFlask` 的一个实例）来注册一个自定义的错误响应处理器。
- 使用 `auth.error_processor` （`auth`是`apiflask.HTTPBasicAuth`或 `apiflask.HTTPTokenAuth` 的一个实例）来注册一个自定义的鉴权错误响应的处理器。
- 子类化 `HTTPError` 来创建自定义的错误类。

!!! tip

    为处理特定的 HTTP 错误而使用 `app.errorhandler` 注册的错误处理器将在自定义的错误响应处理器之上使用。

## 自动的 JSON 格式的错误响应

在 Flask 中，对于 400/404/405/500 错误，将生成默认的错误响应。这个错误响应将采用 HTML 格式，并带有默认的错误讯息和错误描述。但在 APIFlask 中，这些错误都将以 JSON 格式返回，并带有以下的预设字段：

- `message`：HTTP 原因短语或自定义的错误描述。
- `detail`：空字典（404/405/500）或校验请求产生的详细错误信息（400）。

可以在创建 APIFlask 实例时使用 `json_errors` 参数来控制这个行为，`json_errors` 的默认值为 `True`。

```python
from apiflask import APIFlask

# this will disable the automatic JSON error response
app = APIFlask(__name__, json_errors=False)
```

如需自定义错误响应的正文，可以使用 `app.error_processor` 装饰器来注册自定义的错误处理器。 详见[这里](/error-handling/#custom-error-response-processor)。

## 使用 `abort` 和 `HTTPError` 生成错误响应

在视图函数中有两种方式可以中止请求处理的过程，并返回错误响应：

- 调用 `abort` 函数

就和在普通的 Flask 视图函数中所做的一样，只不过这个 `abort` 函数是由 APIFlask 提供：

```python
from apiflask import abort


@app.route('/')
def hello():
    abort(400, message='Something is wrong...')
    return 'Hello, world!'  # this line will never be reached
```

它会在幕后抛出一个 `HTTPError`，所以 `abort`  和 `HTTPError` 会接收相同的参数（见下文）。

- 抛出 `HTTPError` 类

抛出 `HTTPError` 将会做相同的事情：

```python
from apiflask import HTTPError


@app.route('/')
def hello():
    raise HTTPError(400, message='Something is wrong...')
    return 'Hello, world!'  # this line will never be reached
```

这个调用将生成如下的错误响应：

```json
{
    "message": "Something is wrong...",
    "detail": {}
}
```

所有可以传递给 `abort` 和 `HTTPError` 的参数，请参阅 [`HTTPError 的 API 文档`](/api/exceptions/#apiflask.exceptions.HTTPError)。

如果想向响应正文中添加更多字段，可以使用 `extra_data` ，例如：

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
将产生如下的响应：

```json
{
    "message": "Something is wrong...",
    "detail": {},
    "docs": "http://example.com",
    "error_code": 1234
}
```

在大多数情况下，应该使用预设值来创建自定义错误类，而不是直接将它们传递给 `abort` 或 `HTTPError` 。详见下一节。

## 自定义错误类

!!! warning "Version >= 0.11.0"

    这个特性在[版本 0.11.0](/changelog/#version-0110) 中被加入。

可以使用预设的错误信息创建自定义错误类来重用错误。这个自定义错误类应该继承自 `HTTPError`，在这个错误类中可以使用以下属性：

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

!!! tips "使用 Werkzeug 中的异常类"

    如果在创建 `app` 实例时没有将 `json_errors` 设置为 `False`，APIFlask 将捕获所有 Werkzeug 异常，包括被直接抛出的异常：

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

下面的配置变量可用于自定义校验和鉴权错误：

- `VALIDATION_ERROR_DESCRIPTION`
- `AUTH_ERROR_DESCRIPTION`
- `VALIDATION_ERROR_STATUS_CODE`
- `AUTH_ERROR_STATUS_CODE`

详见配置文档中 [自定义响应](/configuration#response-customization) 章节。

## 自定义错误响应处理器

可以使用 `app.error_processor` 装饰器来注册自定义的错误响应的处理器函数。它是一个全局错误处理器，处理所有的 HTTP 错误。

在以下情境下，被装饰的回调函数将被调用：

- 当 `APIFlask(json_errors=True)`（默认情况）时，任何 HTTP 异常都会被 Flask 会抛出。
- 解析请求时发生校验错误。
- 使用 [`HTTPError`][apiflask.exceptions.HTTPError] 触发的异常。
- 使用 [`abort`][apiflask.exceptions.abort] 触发的异常。

使用`app.errorhandler(code_or_exection)` 装饰器，仍可为特定的错误代码或是异常注册特定的错误处理器。在这种情况下，错误处理器的返回值将用作相应错误或异常发生时的响应。

回调函数必须接受一个错误对象作为参数，并返回一个有效的响应：

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

这个错误对象是 [`HTTPError`][apiflask.exceptions.HTTPError] 的一个实例，因此可以通过其属性来获取错误信息：

- status_code：如果这个错误是由校验错误触发的，该值将是 400（默认）或是配置在 `VALIDATION_ERROR_STATUS_CODE` 中的值。如果这个错误是由  [`HTTPError`][apiflask.exceptions.HTTPError] 或  [`abort`][apiflask.exceptions.abort] 触发的，该值将是传入的状态码。其他情况下，该值将是 `Werkzueg` 处理请求时设置的状态码。

- message：这个错误的错误描述，被传入的或是从 Werkzeug 中抓取的。

- detail：这个错误的细节。当校验错误触发时，它将被下面的结构自动填充：

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

    `location` 的值可以是 `json`（即请求正文）或 `query`（即查询字符串），这取决于校验错误发生的位置。

- headers：在  `HTTPError`  或是  `abort` 中设置的值，没有设置默认为 `{}` 。
- extra_data：通过  `HTTPError`  或  `abort` 传入的额外错误信息。

如果愿意，可以将整个响应正文重写为任何你喜欢的内容：

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

    建议在响应中保留 `detail`，因为它包含校验错误发生时的详细信息。

在更改错误响应后，为了 API 文档能正确匹配自定义错误响应的 Schema，还必须更新该错误响应对应的 OpenAPI Schema。

## 更新错误响应的 OpenAPI Schema

APIFlask 中有两种用于错误的 Schema：一种用于一般错误（包括鉴权错误），另一种用于校验错误。可以依次由  `HTTP_ERROR_SCHEMA`  和 `VALIDATION_ERROR_SCHEMA` 进行配置。

!!! question "为什么在错误响应中需要两种 Schema ？"

    给校验错误的响应设置一个单独的 Schema 背后的原因是保证校验错误中的 `detail` 字段始终有值。对于一般的 HTTP 错误，除非通过 `HTTPError` 和 `abort` 传入了一些内容，否则 `detail` 字段将会是空值。

当使用 `error_processor` 更改错误响应的正文时，还需要更新错误响应的 Schema，如此它将更新错误响应的 OpenAPI spec。其中 Schema 可以是一个 OpenAPI Schema 的字典形式，也可以是一个 marshmallow 的 Schema 类。下面是一个将 `status_code` 字段添加到默认错误响应并重命名现有字段的示例（使用 OpenAPI Schema 字典形式）：

```python
# use the built-in `validation_error_detail_schema` for the `detail` field
from apiflask import APIFlask
from apiflask.schemas import validation_error_detail_schema


# schema for generic error response, including auth errors
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


# schema for validation error response
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

## 处理鉴权错误

在创建 APIFlask 实例时将 `json_errors` 设置为 `True` 时（默认为 `True`），APIFlask 会针对鉴权错误返回 JSON 格式的错误，并调用内置的错误回调或调用通过 `app.error_processor` 创建的错误处理器。

在以下情况下，需要为鉴权错误注册一个单独的错误处理器：

- 如果想为 401/403 错误做一些额外的处理，还不想使用`app.errorhandler(401)` 或 `app.errorhandler(403)` 注册特定错误的处理器，就必须使用 `auth.error_processor` 来注册一个鉴权错误的处理器。
- 如果已将 `json_errors` 设置为 `False`，但还想自定义错误响应，由于全局错误处理器将不被使用，就得注册一个自定义的鉴权错误处理器。

可以使用 `auth.error_processor` 装饰器来注册一个鉴权错误的处理器。 它就像 `app.error_processor` 一样工作：

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

如果在 `json_error` 为 `True` 时注册了鉴权错误的处理器，那么它将覆盖全局错误处理器。

!!! question "为什么需要一个单独的错误处理器来处理鉴权错误？"

    APIFlask 的鉴权功能由 Flask-HTTPAuth 支持。由于 Flask-HTTPAuth 对其错误使用了一个单独的错误处理器，APIFlask 必须添加单独的错误处理器来处理它。将来我们可能会想出一个简单的方式来解决这个问题。
