# 请求处理

要了解请求处理的基本用法，请移步《基本用法》章节的 [这个小节](/usage/#use-appinput-to-validate-and-deserialize-request-data)。

首先是几个请求处理的基本概念：

- APIFlask 使用 [webargs](https://github.com/marshmallow-code/webargs) 解析和验证请求。
- 使用一个或多个 [`app.input()`](/api/app/#apiflask.scaffold.APIScaffold.input) 来声明请求数据来源，
  并使用 `location` 来声明请求数据位置。
- 假如解析与验证均成功，数据将会被传至视图函数，否则自动返回 422 错误响应。


## 请求数据的位置声明

APIFlask 提供了以下请求位置支持（`location` 参数）：

- `json` （默认）
- `form`
- `query` （与 `querystring` 相同）
- `path`（与 `view_args` 相同）
- `cookies`
- `headers`
- `files`
- `form_and_files`
- `json_or_form`

你可以使用多个 `app.input` 装饰器声明多组输入数据。然而，你只能使用下面的其中一个来为视图函数声明一个请求体（request body）位置：

- `json`
- `form`
- `files`
- `form_and_files`
- `json_or_form`

```python
@app.get('/')
@app.input(FooHeader, location='headers')  # header
@app.input(FooQuery, location='query')  # query string
@app.input(FooIn, location='json')  # JSON data (body location)
def hello(headers_data, query_data, data_data):
    pass
```

## 请求体的 media type

在生成的 OpenAPI 规范中，请求体的内容类型是根据你声明的输入位置设置的。

- `json`: `application/json`
- `form`: `application/x-www-form-urlencoded`
- `files`: `multipart/form-data`
- `form_and_files`: `multipart/form-data`
- `json_or_form`: `application/json` 和 `application/x-www-form-urlencoded`。对于这个位置，APIFlask 会
    尝试先将请求体解析为 JSON，如果失败，则会尝试将其解析为表单数据。在 OpenAPI 规范中会显示两种内容类型，例如：

    ```yaml
    requestBody:
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        ...
            application/x-www-form-urlencoded:
                schema:
                    type: object
                    properties:
                        ...
    ```

## 请求体的验证

当你使用 `app.input` 声明一个输入时，APIFlask（webargs）将会从指定的位置获取数据，并依据 schema 的定义验证它。

假如解析与验证均成功，数据将会以关键字参数 `{location}_data` 传至视图函数：

```python
@app.get('/')
@app.input(FooQuery, location='query')  # query data
@app.input(FooIn, location='json')  # JSON data
def hello(query_data, json_data):
    pass
```

如果你还定义了 URL 变量，它们也会作为关键字参数传入：

```python
@app.get('/<category>/articles/<int:article_id>')  # category, article_id
@app.input(ArticleQuery, location='query')  # query data
@app.input(ArticleIn, location='json')  # JSON data
def get_article(category, article_id, query_data, json_data):
    pass
```

!!! tip

    注意：URL 变量对应的参数名称（`category`, `article_id`）必须与变量名相同。

如果验证失败，APIFlask 将会自动返回 422 错误响应。与其它错误响应相同，
这个错误响应将会有消息（`message`）和详情（`detail`）等部分。

- 消息（`message`）

它的值将会是 `Validation error`，你可以通过在配置 `VALIDATION_ERROR_DESCRIPTION` 来更改这个值。

- 详情（`detail`）

这个字段中包含错误消息，它的格式如下：

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

`<location>` 的值是验证错误发生的请求数据位置。

- 状态码

默认的验证错误的状态码是 422，你可以在配置中更改 `VALIDATION_ERROR_STATUS_CODE` 的值来更改它。


## 字典 Schema

当你向 `app.input` 传递一个 schema 时，除了使用 schema 类，你也可以使用一个字典（`dict`）：

```python
from apiflask.fields import Integer


@app.get('/')
@app.input(
    {'page': Integer(load_default=1), 'per_page': Integer(load_default=10)},
    location='query'
)
@app.input(FooIn, location='json')
def hello(query_data, json_data):
    pass
```

字典 schema 的名字将会类似于 `"Generated"`，如果你要指定一个 schema 的名字，请使用 `schema_name` 参数：

```python hl_lines="7"
from apiflask.fields import Integer


@app.get('/')
@app.input(
    {'page': Integer(load_default=1), 'per_page': Integer(load_default=10)},
    location='query',
    schema_name='PaginationQuery'
)
@app.input(FooIn, location='json')
def hello(query_data, json_data):
    pass
```

然而，为了使代码更易读并且能够被重用，我们还是建议你尽可能地创建 schema 类。


## 文件上传

!!! warning "Version >= 1.0.0"

    这个功能在 [1.0.0 版本](/changelog/#version-100) 中添加。

你可以在 schema 中使用 [`apiflask.fields.File`](/api/fields/#apiflask.fields.File) 创建一个文件字段，
然后在 `app.input` 中用 `files` 位置：

```python
import os

from werkzeug.utils import secure_filename
from apiflask.fields import File


class Image(Schema):
    image = File()


@app.post('/images')
@app.input(Image, location='files')
def upload_image(files_data):
    f = files_data['image']

    filename = secure_filename(f.filename)
    f.save(os.path.join(the_path_to_uploads, filename))

    return {'message': f'file {filename} saved.'}
```

!!! tip

    这里我们使用了 `secure_filename` 来清理这些文件名，请注意，它只会保留 ASCII 字符。
    你可能想为新文件创建一个随机的文件名, 这个
    [StackOverflow 回答](https://stackoverflow.com/a/44992275/5511849) 可能会帮到你。

文件对象是 `werkzeug.datastructures.FileStorage` 类的实例，
如果要了解请移步 [Werkzeug 文档](https://werkzeug.palletsprojects.com/datastructures/#werkzeug.datastructures.FileStorage)。

如果你想要在 schema 中同时加入文件和其它表单字段，请用 `form_and_files` 位置：

```python
import os

from werkzeug.utils import secure_filename
from apiflask.fields import String, File


class ProfileIn(Schema):
    name = String()
    avatar = File()

@app.post('/profiles')
@app.input(ProfileIn, location='form_and_files')
def create_profile(form_and_files_data):
    avatar_file = form_and_files_data['avatar']
    name = form_and_files_data['name']

    avatar_filename = secure_filename(avatar_file.filename)
    avatar_file.save(os.path.join(the_path_to_uploads, avatar_filename))

    profile = Profile(name=name, avatar_filename=avatar_filename)
    # ...
    return {'message': 'profile created.'}
```

在目前的实现中，`files` 位置的数据将还会包含表单数据（相当于 `form_and_files`）。

!!! notes

    从 APIFlask 2.1.0 开始，你可以使用 `FileType` 和 `FileSize` 验证器来验证文件类型和大小：

    ```python
    from apiflask.validators import FileType, FileSize

    class Image(Schema):
        image = File(validate=[FileType(['.png', '.jpg', '.jpeg', '.gif']), FileSize(max='5 MB')])
    ```

## 请求示例

你可以用 `example` 和 `examples` 参数在 OpenAPI spec 中设定请求的示例，要了解更多信息，
参见《OpenAPI 支持》章节的 [这个部分](/openapi/#response-and-request-example)。
