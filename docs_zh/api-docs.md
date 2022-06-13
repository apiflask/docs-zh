# Swagger UI 和 Redoc

## 更改 Swagger UI 和 Redoc 的路径

Swagger UI 的默认路径是 `/docs`，它使用默认端口在本地运行时的 URL 为
<http://localhost:5000/docs>。你可以在创建 `APIFlask` 实例时，通过修改 `docs_path` 参数来更改此路径：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path='/swagger-ui')
```

同样，Redoc 的默认路径是 `/redoc`，你可以修改 `redoc_path` 参数来更改此路径：

```python
from apiflask import APIFlask

app = APIFlask(__name__, redoc_path='/api-doc')
```

`docs_path` 和 `redoc_path` 接受以斜杠开头的 URL 路径，因此你可以设置这样的前缀：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path='/docs/swagger-ui', redoc_path='/docs/redoc')
```

这时文档的本地 URL 将是 <http://localhost:5000/docs/swagger-ui> 和
<http://localhost:5000/docs/redoc>。

## 全局禁用 API 文档

你可以将 `docs_path` 参数设置为 `None` 以禁用 Swagger UI 文档：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path=None)
```

同样，你可以将 `redoc_path` 参数设置为 `None` 以禁用 Redoc
文档：

```python
from apiflask import APIFlask

app = APIFlask(__name__, redoc_path=None)
```

或者同时禁用两者：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path=None, redoc_path=None)
```

!!! tip
    如果你想禁用应用程序的所有 OpenAPI 支持，
    详情请参阅 *[禁用 OpenAPI 支持](/openapi/#disable-the-openapi-support)* 。

## 禁用指定蓝本的 API 文档

有关详细内容，请参阅 *[禁用指定蓝图的 OpenAPI 支持](/openapi/#disable-for-specific-blueprints)*。

## 禁用指定视图函数的 API 文档

有关详细内容，请参阅 *[禁用指定视图函数的 OpenAPI 支持](/openapi/#disable-for-specific-view-functions)*。

## 配置 Swagger UI/Redoc

以下配置变量可用于配置 Swagger UI/Redoc：

- `DOCS_FAVICON`
- `REDOC_USE_GOOGLE_FONT`
- `REDOC_CONFIG`
- `SWAGGER_UI_LAYOUT`
- `SWAGGER_UI_CONFIG`
- `SWAGGER_UI_OAUTH_CONFIG`

请参阅 *[配置](/configuration/#swagger-ui-and-redoc)*
来查看这些配置变量的介绍和示例。

## 对 Swagger UI/Redoc 资源使用不同的 CDN 服务

每个资源（JavaScript/CSS 文件）的 URL 都有一个配置变量。你可以传递你的首选 CDN 服务的 URL 到相应的配置变量上：

- `REDOC_STANDALONE_JS`
- `SWAGGER_UI_CSS`
- `SWAGGER_UI_BUNDLE_JS`
- `SWAGGER_UI_STANDALONE_PRESET_JS`

请参阅 *[配置](/configuration/#swagger-ui-and-redoc)*
来查看配置变量的介绍和示例。

## 从本地资源提供 Swagger UI/Redoc 服务

就同前面那样，如果想使用本地资源，可以传递本地静态文件的 URL 到相应的配置变量：

- `REDOC_STANDALONE_JS`
- `SWAGGER_UI_CSS`
- `SWAGGER_UI_BUNDLE_JS`
- `SWAGGER_UI_STANDALONE_PRESET_JS`

对于本地资源，您可以传递相对 URL 。 例如，如果你想在本地托管独立的 Redoc JavaScript 文件，请按照以下步骤操作：

手动下载文件：

- 从 [CDN 服务器][_redoc_cdn]{target=_blank} 下载文件。
- 将文件放在您的 `static` 文件夹中，将其命名为 `redoc.standalone.js` 或其他。
- 找出 js 文件的相对 URL。 如果文件在 `static` 文件夹中，那么 URL 将是 `/static/redoc.standalone.js`。如果你把它放到一个名为 `js` 的子文件夹里，那么 URL 则是 `/static/js/redoc.standalone.js`。
- 将 URL 传递给相应的配置变量：

    ```python
    app.config['REDOC_STANDALONE_JS'] = '/static/js/redoc.standalone.js'
    ```

[_redoc_cdn]: https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

!!! tip
    URL 的 `static` 部分将会匹配你传递的 `static_url_path` 参数到 `APIFlask` 类中，默认值为 `static`。

或者使用 npm:

- 使用 `npm init` 初始化 `static` 文件夹中的 npm。
- 通过 `npm i redoc` 命令安装文件。
- 将 URL 传递到相应的配置变量：

    ```python
    app.config['REDOC_STANDALONE_JS'] = 'static/node_modules/redoc/bundles/redoc.standalone.js'
    ```

!!! tip
    Swagger UI 的相关资源可以在 [Swagger UI 发行页][_swagger_ui_releases]{target=_blank} 中下载资源里的 `dist` 文件夹中找到。

[_swagger_ui_releases]: https://github.com/swagger-api/swagger-ui/releases
