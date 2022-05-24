# 配置

## 基础知识

在 Flask 中，配置系统是基于 `app.config` 属性构建的。它是一个类字典的属性，
因此你可以像操作字典一样操作它

`app.config` 属性将会包含以下配置：

- 内置于 Flask 的配置变量
- 内置于 Flask 扩展的配置变量
- 内置于 APIFlask 的配置变量
- 你自定义的配置变量

这是 `app.config` 基本操作的一个示例:

```python
from apiflask import APIFlask

app = APIFlask(__name__)

# 设置一个配置项
app.config['DESCRIPTION'] = 'A wonderful API'

# 读取一个配置项
description = app.config['DESCRIPTION']
```

因为它是一个类字典的对象，你也可以通过 `app.config.get()` 方法读取
一个带有默认值的配置变量：

```python
my_name = app.config.get('DESCRIPTION', '默认值')
```

或者通过 `app.config.update()` 方法同时更新多个值：

```python
app.config.update(
    'DESCRIPTION'='A wonderful API',
    'FOO'='bar',
    'ITEMS_PER_PAGE'=15
)
```

对于一个大型应用来说，你可以将所有的配置变量存储于一个独立的文件中。
例如， 可以将它们存储在 `settings.py`：

```python
MY_CONFIG = 'A wonderful API'
FOO = 'bar'
ITEMS_PER_PAGE = 15
```

现在，你可以通过 `app.config.from_pyfile()` 方法来设置配置变量。


```python
from apiflask import APIFlask

app = APIFlask(__name__)

# 设置从 settings.py 导入的所有配置变量
app.config.from_pyfile('settings.py')
```

阅读 Flask 文档中的 *[Configuration Handling][_config]{target:_blank}* 一章来了解更多有关配置管理的内容。

[_config]: https://flask.palletsprojects.com/config/

!!! warning

    所有的配置变量应当采用全大写的形式

!!! tip "在应用上下文之外读取配置"

    如果你想在应用上下文之外读取配置变量，你将看见：“在应用
    上下文之外工作（Working outside of the application context“
    的错误，这个错误通常在你采用应用工厂时出现。

    当你使用应用工厂时，你可以通过在视图函数中使用 `current_app.config`
    来访问配置：

    ```python
    from flask import current_app

    @bp.get('/foo')
    def foo():
        bar = current_app.config['BAR']
    ```

    但是，当你定义一个数据 schema 时，一般不会拥有应用上下文，
    所以你无法使用 `current_app`。在这种情况下从存储配置变量的模块访问它们：

    ```python hl_lines="3 6"
    from apiflask import Schema

    from .settings import CATEGORIES  # 导入配置变量

    class PetInSchema(Schema):
        name = String(required=True, validate=Length(0, 10))
        category = String(required=True, validate=OneOf(CATEGORIES))  # 使用配置变量
    ```


## 内置配置变量

以下时所有 APIFlask 内置的配置变量：


### OpenAPI 字段

生成 OpenAPI spec 时会用到 OpenAPI 相关字段的所有配置，它们也将由 API 文档呈现。


#### `OPENAPI_VERSION`

OpenAPI 规范的版本（`openapi.openapi`）。这个配置也可以通过
`app.openapi_version` 属性设置。

- 类型：`str`
- 默认值：`'3.0.3'`
- 示例：

```python
app.config['OPENAPI_VERSION'] = '3.0.2'
```

或：

```python
app.openapi_version = '3.0.2'
```

!!! warning "Version >= 0.4.0"

    这个配置变量在 [0.4.0 版本中](/changelog/#version-040) 添加。


#### `SERVERS`

API 项目的服务器信息（`openapi.servers`），接受多个服务器信息的字典。
这个配置也可以通过 `app.servers` 属性设置。

- 类型：`List[Dict[str, str]]`
- 默认值：`None`
- 示例：

```python
app.config['SERVERS'] = [
    {
        'name': 'Production Server',
        'url': 'http://api.example.com'
    }
]
```

或：

```python
app.servers = [
    {
        'name': 'Production Server',
        'url': 'http://api.example.com'
    }
]
```


#### `TAGS`

OpenAPI spec 文档的标签列表（`openapi.tags`）接受一个字典的列表，你也可以传入
一个包含所有标签名字的字符串列表。这个配置也可以通过 `app.tags` 属性设置。

如果没有设置的话，蓝本的名字将会用作标签，所有定义于蓝本中的端点将会自动被这个标签标记。

- 类型：`Union[List[str], List[Dict[str, str]]]`
- 默认值：`None`
- 示例：

简单标签名字列表的示例：

```python
app.config['TAGS'] = ['foo', 'bar', 'baz']
```

包含标签描述的示例：

```python
app.config['TAGS'] = [
    {'name': 'foo', 'description': 'The description of foo'},
    {'name': 'bar', 'description': 'The description of bar'},
    {'name': 'baz', 'description': 'The description of baz'}
]
```

包含完整 OpenAPI 标签的示例：

```python
app.config['TAGS'] = [
    {
        'name': 'foo',
        'description': 'tag description',
        'externalDocs': {
            'description': 'Find more info here',
            'url': 'http://example.com'
        }
    }
]
```

使用 `app.tags`：

```python
app.tags = ['foo', 'bar', 'baz']
```


#### `EXTERNAL_DOCS`

API 项目的外部文档信息（`openapi.externalDocs`），这个配置也可以
通过 `app.external_docs` 属性设置。

- 类型: `Dict[str, str]`
- 默认值: `None`
- 示例：

```python
app.config['EXTERNAL_DOCS'] = {
    'description': 'Find more info here',
    'url': 'http://docs.example.com'
}
```

或:

```python
app.external_docs = {
    'description': 'Find more info here',
    'url': 'http://docs.example.com'
}
```


#### `INFO`

API 项目的信息字段（`openapi.info`），这个配置也可以通过 `app.info` 属性
设置，信息对象（openapi.info）接受一个包含以下信息字段的字典：`description`，
`termsOfService`，`contact`，`license`。你可以使用分开的配置变量来覆盖这个字典。

- 类型: `Dict[str, str]`
- 默认值: `None`
- 示例：

```python
app.config['INFO'] = {
    'description': '...',
    'termsOfService': 'http://example.com',
    'contact': {
        'name': 'API Support',
        'url': 'http://www.example.com/support',
        'email': 'support@example.com'
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    }
}
```

或：

```python
app.info = {
    'description': '...',
    'termsOfService': 'http://example.com',
    'contact': {
        'name': 'API Support',
        'url': 'http://www.example.com/support',
        'email': 'support@example.com'
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    }
}
```


#### `DESCRIPTION`

API 项目的描述（`openapi.info.description`），这个配置也可以通过
`app.description` 属性设置。

- 类型: `str`
- 默认值: `None`
- 示例：

```python
app.config['DESCRIPTION'] = 'Some description of my API.'
```

或：

```python
app.description = 'Some description of my API.'
```


#### `TERMS_OF_SERVICE`

API 项目的服务条款 URL（`openapi.info.termsOfService`），
这个配置也可以通过 `app.terms_of_service` 属性设置。

- 类型: `str`
- 默认值: `None`
- 示例：

```python
app.config['TERMS_OF_SERVICE'] = 'http://example.com/terms/'
```

或：

```python
app.terms_of_service = 'http://example.com/terms/'
```


#### `CONTACT`

API 项目的联系信息（`openapi.info.contact`）。
这个配置也可以通过 `app.contact` 设置。

- 类型: `Dict[str, str]`
- 默认值: `None`
- 示例：

```python
app.config['CONTACT'] = {
    'name': 'API Support',
    'url': 'http://example.com',
    'email': 'support@example.com'
}
```

或：

```python
app.contact = {
    'name': 'API Support',
    'url': 'http://example.com',
    'email': 'support@example.com'
}
```


#### `LICENSE`

API 项目的协议（`openapi.info.license`），这个配置也可以通过 `app.license` 设置。

- 类型: `Dict[str, str]`
- 默认值: `None`
- 示例：

```python
app.config['LICENSE'] = {
    'name': 'Apache 2.0',
    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
}
```

或：

```python
app.license = {
    'name': 'Apache 2.0',
    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
}
```


### OpenAPI spec

自定义 OpenAPI spec 的生成。


#### `SPEC_FORMAT`

OpenAPI spec 的格式，接受 `'json'`、`'yaml'` 或 `'yml'`中的一个。
这个配置在以下几种情形下使用：

- 通过内置的路由返回 spec 信息。
- 在不传入 `--format`/`-f` 选项时运行 `flask spec` 命令。

!!! warning
    `APIFlask(spec_path=...)` 在 0.7.0 及之后的版本中去除了对格式的自动检测。

- 类型: `str`
- 默认值: `'json'`
- 示例：

```python
app.config['SPEC_FORMAT'] = 'yaml'
```

!!! warning "Version >= 0.7.0"

    这个配置变量在 [0.7.0 版本](/changelog/#version-070) 中添加。


#### `LOCAL_SPEC_PATH`

OpenAPI spec 文件的路径。

- 类型: `str`
- 默认值: `None`
- 示例：

```python
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
```

!!! warning

    如果你传入的路径是一个相对路径，请不要在前面添加一个斜杠（`/`）。

!!! warning "Version >= 0.7.0"

    这个配置变量在 [0.7.0 版本](/changelog/#version-070) 中添加。


#### `LOCAL_SPEC_JSON_INDENT`

本地 OpenAPI spec 在 JSON 格式下的缩进量。

- 类型: `int`
- 默认值: `2`
- 示例：

```python
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
```

!!! warning "Version >= 0.7.0"

    这个配置变量在 [0.7.0 版本](/changelog/#version-070) 中添加。


#### `SYNC_LOCAL_SPEC`

如果这个配置为 `True`，那么本地的 spec 文件将会自动同步更新，在
[保持本地 spec 文件自动同步更新](/openapi#keep-the-local-spec-in-sync-automatically)
一节中查看示例用法。

- 类型: `bool`
- 默认值: `None`
- 示例：

```python
app.config['SYNC_LOCAL_SPEC'] = True
```

!!! warning "Version >= 0.7.0"

    这个配置变量在 [0.7.0 版本](/changelog/#version-070) 中添加。


#### `JSON_SPEC_MIMETYPE`

用作 OpenAPI spec JSON 响应值的 MIME 类型字符串。

- 类型: `str`
- 默认值: `'application/json'`
- 示例：

```python
app.config['JSON_SPEC_MIMETYPE'] = 'application/custom-json'
```

!!! warning "Version >= 0.4.0"

    这个配置变量在 [0.4.0 版本](/changelog/#version-040) 中添加。


#### `YAML_SPEC_MIMETYPE`

用作 OpenAPI spec YAML 响应值的 MIME 类型字符串。

- 类型: `str`
- 默认值: `'text/vnd.yaml'`
- 示例：

```python
app.config['YAML_SPEC_MIMETYPE'] = 'text/x-yaml'
```

!!! warning "Version >= 0.4.0"

    这个配置变量在 [0.4.0 版本](/changelog/#version-040) 中添加。


### 对自动化行为的控制

以下配置变量被用来控制 APIflask 的自动化行为，所有这些配置变量的默认值都是
`True`，你可以在需要时禁用它们。


#### `AUTO_TAGS`

启用或禁用自动从蓝本名生成标签（`openapi.tags`）。

!!! tip

    这种自动化行为仅当 `app.tags` 或 `TAGS` 配置没有被设置的时候才会进行。

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_TAGS'] = False
```


#### `AUTO_OPERATION_SUMMARY`

启用或禁用自动从视图函数名或文档生成 OpenAPI 中路径的概要（summary）。

!!! tip

    这种自动化行为仅当视图函数没有被 `app.doc(summary=...)` 装饰时才会进行。

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_OPERATION_SUMMARY'] = False
```

!!! warning

    在 0.8.0 及之后的版本中，这个变量从 `AUTO_PATH_SUMMARY` 重命名为 `AUTO_OPERATION_SUMMARY`。


#### `AUTO_OPERATION_DESCRIPTION`

启用或禁用自动从视图函数文档生成 OpenAPI 中对路径的描述。

!!! tip

    这种自动化行为仅当视图函数没有被 `@app.doc(description=...)` 装饰时才会进行。

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_OPERATION_DESCRIPTION'] = False
```

!!! warning

    在 0.8.0 及之后的版本中，这个变量从 `AUTO_PATH_DESCRIPTION`
    重命名为 `AUTO_OPERATION_DESCRIPTION`。


#### `AUTO_OPERATION_ID`

!!! warning "Version >= 0.10.0"

    这个功能在 [0.10.0 版本中](/changelog/#version-0100) 添加。

启用或禁用自动从视图函数的请求方法和端点处生成 operationId。在 [设置 `operationId`](/openapi/#set-operationid) 一节中了解详细内容。

- 类型: `bool`
- 默认值: `False`
- 示例：

```python
app.config['AUTO_OPERATION_ID'] = True
```


#### `AUTO_200_RESPONSE`

如果一个视图函数不被 `@app.input`、`@app.output`、`@app.auth_required`、`@app.doc`
装饰，APIFlask 会默认在 OpenAPI spec 中为这个视图默认添加一个 200 响应。
将这个配置设为 `False` 来禁用这种行为。

!!! tip

    You can change the description of the default 200 response with config
    `SUCCESS_DESCRIPTION`.

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_200_RESPONSE'] = False
```


#### `AUTO_404_RESPONSE`

If a view function's URL rule contains a variable. By default, APIFlask will add a
404 response for this view into OpenAPI spec. Set this config to `False` to disable
this behavior.

!!! tip

    You can change the description of the automatic 404 response with config
    `NOT_FOUND_DESCRIPTION`.

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_404_RESPONSE'] = False
```

!!! warning "Version >= 0.8.0"

    这个配置变量在 [0.8.0 版本](/changelog/#version-080) 中添加。


#### `AUTO_VALIDATION_ERROR_RESPONSE`

If a view function uses `@app.input` to validate input request data, APIFlask will add a
validation error response into OpenAPI spec for this view. Set this config to `False`
to disable this behavior.

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_VALIDATION_ERROR_RESPONSE'] = False
```


#### `AUTO_AUTH_ERROR_RESPONSE`

If a view function uses `@app.auth_required` to restrict the access, APIFlask will add
an authentication error response into OpenAPI spec for this view. Set this
config to `False` to disable this behavior.

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['AUTO_AUTH_ERROR_RESPONSE'] = False
```


### Response customization

The following configuration variables are used to customize auto-responses.


#### `SUCCESS_DESCRIPTION`

The default description of the 2XX responses.

- 类型: `str`
- 默认值: `Successful response`
- 示例：

```python
app.config['SUCCESS_DESCRIPTION'] = 'Success!'
```

!!! warning "Version >= 0.4.0"

    这个配置变量在 [0.4.0 版本](/changelog/#version-040) 中添加。


#### `NOT_FOUND_DESCRIPTION`

The default description of the 404 response.

- 类型: `str`
- 默认值: `Not found`
- 示例：

```python
app.config['NOT_FOUND_DESCRIPTION'] = 'Missing'
```

!!! warning "Version >= 0.8.0"

    这个配置变量在 [0.8.0 版本](/changelog/#version-080) 中添加。


#### `VALIDATION_ERROR_STATUS_CODE`

The status code of validation error response.

- 类型: `int`
- 默认值: `400`
- 示例：

```python
app.config['VALIDATION_ERROR_STATUS_CODE'] = 422
```


#### `VALIDATION_ERROR_DESCRIPTION`

The description of validation error response.

- 类型: `str`
- 默认值: `'Validation error'`
- 示例：

```python
app.config['VALIDATION_ERROR_DESCRIPTION'] = 'Invalid JSON body'
```


#### `VALIDATION_ERROR_SCHEMA`

The schema of validation error response, accepts a schema class or
a dict of OpenAPI schema definition.

- 类型: `Union[Schema, dict]`
- 默认值: `apiflask.schemas.validation_error_schema`
- 示例：

```python
app.config['VALIDATION_ERROR_SCHEMA'] = CustomValidationErrorSchema
```


#### `AUTH_ERROR_STATUS_CODE`

The status code of authentication error response.

- 类型: `int`
- 默认值: `401`
- 示例：

```python
app.config['AUTH_ERROR_STATUS_CODE'] = 403
```


#### `AUTH_ERROR_DESCRIPTION`

The description of authentication error response.

- 类型: `str`
- 默认值: `'Authentication error'`
- 示例：

```python
app.config['AUTH_ERROR_DESCRIPTION'] = 'Auth error'
```


#### `HTTP_ERROR_SCHEMA`

The schema of generic HTTP error response, accepts a schema class or
a dict of OpenAPI schema definition.

- 类型: `Union[Schema, dict]`
- 默认值: `apiflask.schemas.http_error_schema`
- 示例：

```python
app.config['HTTP_ERROR_SCHEMA'] = CustomHTTPErrorSchema
```


#### `BASE_RESPONSE_SCHEMA`

The schema of base response schema, accepts a schema class or a dict of
OpenAPI schema definition.

- 类型: `Union[Schema, dict]`
- 默认值: `None`
- 示例：

```python
from apiflask import APIFlask, Schema
from apiflask.fields import String, Integer, Field

app = APIFlask(__name__)

class BaseResponseSchema(Schema):
    message = String()
    status_code = Integer()
    data = Field()

app.config['BASE_RESPONSE_SCHEMA'] = BaseResponseSchema
```

!!! warning "Version >= 0.9.0"

    这个配置变量在 [0.9.0 版本](/changelog/#version-090) 中添加。


#### `BASE_RESPONSE_DATA_KEY`

The data key of the base response, it should match the data field name in the base
response schema.

- 类型: `str`
- 默认值: `'data'`
- 示例：

```python
app.config['BASE_RESPONSE_DATA_KEY'] = 'data'
```

!!! warning "Version >= 0.9.0"

    这个配置变量在 [0.9.0 版本](/changelog/#version-090) 中添加。


### Swagger UI and Redoc

The following configuration variables used to customize Swagger UI and
Redoc documentation.


#### `DOCS_FAVICON`

The absolute or relative URL of the favicon image file of API documentations.

- 类型: `str`
- 默认值: `'https://apiflask.com/_assets/favicon.png'`
- 示例：

```python
app.config['DOCS_FAVICON'] = 'https://cdn.example.com/favicon.png'
```


#### `REDOC_USE_GOOGLE_FONT`

Enable or disable Google font in Redoc documentation.

- 类型: `bool`
- 默认值: `True`
- 示例：

```python
app.config['REDOC_USE_GOOGLE_FONT'] = False
```


#### `REDOC_CONFIG`

The configuration options pass to Redoc. See the available options in the
[Redoc documentation]（https://github.com/Redocly/redoc#redoc-options-object），

- 类型: `dict`
- 默认值: `None`
- 示例：

```python
app.config['REDOC_CONFIG'] = {'disableSearch': True, 'hideLoading': True}
```

!!! warning "Version >= 0.9.0"

    这个配置变量在 [0.9.0 版本](/changelog/#version-090) 中添加。


#### `REDOC_STANDALONE_JS`

The absolute or relative URL of the Redoc standalone JavaScript file.

- 类型: `str`
- 默认值: `'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'`
- 示例：

```python
app.config['REDOC_STANDALONE_JS'] = 'https://cdn.example.com/filename.js'
```


#### `SWAGGER_UI_CSS`

The absolute or relative URL of the Swagger UI CSS file.

- 类型: `str`
- 默认值: `'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css'`
- 示例：

```python
app.config['SWAGGER_UI_CSS'] = 'https://cdn.example.com/filename.js'
```


#### `SWAGGER_UI_BUNDLE_JS`

The absolute or relative URL of the Swagger UI bundle JavaScript file.

- 类型: `str`
- 默认值: `'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js'`
- 示例：

```python
app.config['SWAGGER_UI_BUNDLE_JS'] = 'https://cdn.example.com/filename.js'
```


#### `SWAGGER_UI_STANDALONE_PRESET_JS`

The absolute or relative URL of the Swagger UI standalone preset JavaScript file.

- 类型: `str`
- 默认值: `'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-standalone-preset.js'`
- 示例：

```python
app.config['SWAGGER_UI_STANDALONE_PRESET_JS'] = 'https://cdn.example.com/filename.js'
```


#### `SWAGGER_UI_LAYOUT`

The layout of Swagger UI, one of `'BaseLayout'` and `'StandaloneLayout'`.

- 类型: `str`
- 默认值: `'BaseLayout'`
- 示例：

```python
app.config['SWAGGER_UI_LAYOUT'] = 'StandaloneLayout'
```


#### `SWAGGER_UI_CONFIG`

The config for Swagger UI, this config value will overwrite the existing config,
such as `SWAGGER_UI_LAYOUT`.

!!! tip

    See *[Configuration][_swagger_conf]{target=_blank}* of the Swagger UI docs
    for more details.

[_swagger_conf]: https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/

- 类型: `dict`
- 默认值: `None`
- 示例：

```python
app.config['SWAGGER_UI_CONFIG'] = {
    'layout': 'StandaloneLayout'
}
```


#### `SWAGGER_UI_OAUTH_CONFIG`

The config for Swagger UI OAuth:

```js
ui.initOAuth(yourConfig)
```

!!! tip

    See the *[OAuth 2.0 configuration][_swagger_oauth]{target=_blank}* in Swagger UI
    docs for more details.

[_swagger_oauth]: https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/

- 类型: `dict`
- 默认值: `None`
- 示例：

```python
app.config['SWAGGER_UI_OAUTH_CONFIG'] = {
    'realm': 'foo'
}
```


## Flask built-in configuration variables

See *[Builtin Configuration Values][_flask_config]{target:_blank}* for the
built-in configuration variables provided by Flask.

[_flask_config]: https://flask.palletsprojects.com/config/#builtin-configuration-values
