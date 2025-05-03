# API 文档

APIFlask 支持下面这几种 API 文档 UI：

- [Swagger UI](https://github.com/swagger-api/swagger-ui)
- [Redoc](https://github.com/Redocly/redoc)
- [Elements](https://github.com/stoplightio/elements)
- [RapiDoc](https://github.com/rapi-doc/RapiDoc)
- [RapiPDF](https://github.com/mrin9/RapiPdf)


## 更改 API 文档库

API 文档库通过实例化 APIFlask 类时使用 `docs_ui` 参数控制：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_ui='redoc')
```

可选值如下所示：

- `swagger-ui` (default value)
- `redoc`
- `elements`
- `rapidoc`
- `rapipdf`


## 更改 API 文档的路径

API 文档的默认路径是 `/docs`，它使用默认端口在本地运行时的 URL 为
<http://localhost:5000/docs>。你可以在创建 `APIFlask` 实例时，通过修改 `docs_path` 参数来更改此路径：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path='/api-docs')
```

`docs_path` 接受以斜杠开头的 URL 路径，因此你可以设置这样的前缀：


```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path='/openapi/docs')
```

这时文档的本地 URL 将是 <http://localhost:5000/openapi/docs>。

你也可以设置 `openapi_blueprint_url_prefix` 来给所有 OpenAPI 相关的路径添加一个前缀：

```python
from apiflask import APIFlask

app = APIFlask(__name__, openapi_blueprint_url_prefix='/openapi')
```

现在 OpenAPI 文档和 spec 的路径将会分别是 <http://localhost:5000/openapi/docs>
和 <http://localhost:5000/openapi/openapi.json>。


## 添加自定义 API 文档

你可以自己来为其他 API 文档添加支持，或者是自己来提供上面提到的那些 API 文档。

以 Redoc 为例，你只需要创建一个视图函数渲染文档的模板：

```python
from apiflask import APIFlask
from flask import render_template

app = APIFlask(__name__)


@app.route('/redoc')
def my_redoc():
    return render_template('/redoc.html')
```

下面是 Redoc 对应的 `redoc.html` 模板:

```html hl_lines="17"
<!DOCTYPE html>
<html>
  <head>
    <title>My Redoc</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url="{{ url_for('openapi.spec') }}"></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"> </script>
  </body>
</html>
```

在模板中，我们使用 `{{ url_for('openapi.spec') }}` 获取 OpenAPI spec 对应的 URL。

现在访问 <http://localhost:5000/redoc>，你会看到你自己提供的 API 文档。

通过这种方式，你可以同时支持多个 API 文档，或是为文档视图添加安全认证。如果你想要为 API 文档使用内置的配置变量或者只是想少些一点代码，可以直接从 APIFlask 导入 API 文档的模板：

```python
from apiflask import APIFlask
from apiflask.ui_templates import redoc_template
from flask import render_template_string

app = APIFlask(__name__)


@app.route('/redoc')
def my_redoc():
    return render_template_string(redoc_template, title='My API', version='1.0')
```

## 为 API 文档添加认证保护

有关更多详细信息，请参阅 *[保护 OpenAPI 端点](/openapi/#protect-openapi-endpoints)*。


## 全局禁用 API 文档

你可以将 `docs_path` 参数设置为 `None` 以禁用 API 文档：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_path=None)
```

!!! tip
    如果你想禁用应用程序的所有 OpenAPI 支持，
    详情请参阅 [禁用 OpenAPI 支持](/openapi/#disable-the-openapi-support)。


## 禁用指定蓝本的 API 文档

有关详细内容，请参阅 [禁用指定蓝本的 OpenAPI 支持](/openapi/#disable-for-specific-blueprints)。


## 禁用指定视图函数的 API 文档

有关详细内容，请参阅 [禁用指定视图函数的 OpenAPI 支持](/openapi/#disable-for-specific-view-functions)。


## 配置 API 文档

以下配置变量可用于配置 API 文档：

- `DOCS_FAVICON`
- `REDOC_USE_GOOGLE_FONT`
- `REDOC_CONFIG`
- `SWAGGER_UI_LAYOUT`
- `SWAGGER_UI_CONFIG`
- `SWAGGER_UI_OAUTH_CONFIG`
- `ELEMENTS_LAYOUT`
- `ELEMENTS_CONFIG`
- `RAPIDOC_THEME`
- `RAPIDOC_CONFIG`
- `RAPIPDF_CONFIG`

请参阅 [API 文档配置](/configuration/#API文档)
来查看这些配置变量的介绍和示例。


## 为 API 文档库资源使用不同的 CDN 服务

每个资源（JavaScript/CSS 文件）的 URL 都有一个配置变量。你可以传递你的首选 CDN 服务的 URL 到相应的配置变量上：

- `REDOC_STANDALONE_JS`
- `SWAGGER_UI_CSS`
- `SWAGGER_UI_BUNDLE_JS`
- `SWAGGER_UI_STANDALONE_PRESET_JS`
- `RAPIDOC_JS`
- `ELEMENTS_JS`
- `ELEMENTS_CSS`
- `RAPIPDF_JS`

下面是一些示例：

```py
# Swagger UI
app.config['SWAGGER_UI_CSS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css'
app.config['SWAGGER_UI_BUNDLE_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.min.js'
app.config['SWAGGER_UI_STANDALONE_PRESET_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-standalone-preset.min.js'
# Redoc
app.config['REDOC_STANDALONE_JS'] = 'https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js'
# Elements
app.config['ELEMENTS_JS'] = 'https://cdn.jsdelivr.net/npm/@stoplight/elements-dev-portal@1.7.4/web-components.min.js'
app.config['ELEMENTS_CSS'] = 'https://cdn.jsdelivr.net/npm/@stoplight/elements-dev-portal@1.7.4/styles.min.css'
# RapiDoc
app.config['RAPIDOC_JS'] = 'https://cdn.jsdelivr.net/npm/rapidoc@9.3.2/dist/rapidoc-min.min.js'
# RapiPDF
app.config['RAPIPDF_JS'] = 'https://cdn.jsdelivr.net/npm/rapipdf@2.2.1/src/rapipdf.min.js'
```

请参阅 [API 文档配置](/configuration/#API文档)
来查看这些配置变量的介绍和示例。


## 从本地资源提供 API 文档资源

和上一节类似，如果想使用本地资源，可以传递本地静态文件的 URL 到相应的配置变量：

- `REDOC_STANDALONE_JS`
- `SWAGGER_UI_CSS`
- `SWAGGER_UI_BUNDLE_JS`
- `SWAGGER_UI_STANDALONE_PRESET_JS`
- `RAPIDOC_JS`
- `ELEMENTS_JS`
- `ELEMENTS_CSS`
- `RAPIPDF_JS`

对于本地资源，你可以传递相对 URL。例如，如果你想在本地托管独立的 Redoc JavaScript 文件，请按照以下步骤操作：

手动下载文件：

- 从 [CDN 服务器][_redoc_cdn]{target=_blank} 下载文件。
- 将文件放在你的 `static` 文件夹中，将其命名为 `redoc.standalone.js` 或其他任意名称。
- 确定 js 文件的相对 URL。 如果文件在 `static` 文件夹中，那么 URL 将是 `/static/redoc.standalone.js`。如果你把它放到一个名为 `js` 的子文件夹里，那么 URL 则是 `/static/js/redoc.standalone.js`。
- 将 URL 传递给相应的配置变量：

    ```python
    app.config['REDOC_STANDALONE_JS'] = '/static/js/redoc.standalone.js'
    ```

[_redoc_cdn]: https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

!!! tip
    URL 的 `static` 部分将会匹配你传递的 `static_url_path` 参数到 `APIFlask` 类中，默认值为 `static`。

或者使用 NPM:

- 使用 `npm init` 在 `static` 文件夹中初始化 npm。
- 通过 `npm i redoc` 命令安装文件。
- 将 URL 传递到相应的配置变量：

    ```python
    app.config['REDOC_STANDALONE_JS'] = 'static/node_modules/redoc/bundles/redoc.standalone.js'
    ```

!!! tip
    Swagger UI 的相关资源可以在 [Swagger UI 发行页][_swagger_ui_releases]{target=_blank} 中下载资源里的 `dist` 文件夹中找到。

    [_swagger_ui_releases]: https://github.com/swagger-api/swagger-ui/releases

### 独立的静态 HTML 文档

对于离线使用，你可以使用 RapiPDF 将 OpenAPI 文档生成 PDF 文件：

```python
from apiflask import APIFlask

app = APIFlask(__name__, docs_ui='rapipdf')
```

如果生成的 PDF 文件无法满足你的需求，你也可以将静态 HTML 文件作为 API 文档提供。

以 Swagger UI 为例，你需要：

1. 创建一个加载 Swagger UI JavaScript 和 CSS 文件的静态 HTML 文件。
2. 使用 `flask spec` 命令生成本地 OpenAPI 规范文件，并设置以下配置：

    ```python
    app.config['SYNC_LOCAL_SPEC'] = True  # 保持规范文件与代码同步
    app.config['LOCAL_SPEC_PATH'] = 'openapi.json'  # 规范文件的路径
    app.config['LOCAL_SPEC_JSON_INDENT'] = 0  # 设置为 0 以移除缩进
    ```

3. 创建一个 shell 脚本来读取 OpenAPI 规范文件并将其传递给 Swagger UI HTML 文件。例如：

    ```sh
    #!/bin/sh

    spec_value=$(python3 -c "import json; print(open('openapi.json').read())")
    # 替换 index.html 中的 var spec = {...} 行
    sed -i "s|var spec = {.*}|var spec = $spec_value|g" index.html
    ```

这里是[一个完整的示例](https://github.com/apiflask/apiflask/tree/main/examples/openapi/static_docs)。

另请参阅 [Swagger UI 文档](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/installation.md#plain-old-htmlcssjs-standalone)
了解独立安装的更多信息。
