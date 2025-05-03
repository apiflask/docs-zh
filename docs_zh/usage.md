# 基本用法

本章将介绍 APIFlask 的主要用法。

## 要求

- Python 3.8+
- Flask 2.2+

你还需要了解 Flask 的基本知识。以下是一些学习 Flask 的免费资源：

- [Flask 官方文档](https://flask.palletsprojects.com/){target=_blank}
- [Flask 官方教程](https://flask.palletsprojects.com/tutorial/#tutorial){target=_blank}
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world){target=_blank}
- [Flask 入门教程](https://github.com/greyli/flask-tutorial){target=_blank}（中文）

## 安装

=== "Linux/macOS"

    ```
    $ pip3 install apiflask
    ```

=== "Windows"

    ```
    > pip install apiflask
    ```

!!! tip "Python 依赖管理工具"

    上述命令使用 [pip][_pip]{target=_blank} 安装 APIFlask，你也可以使用其他依赖管理工具，如 [Poetry][_poetry]{target=_blank}、[Pipenv][_pipenv]{target=_blank}、[PDM][_pdm]{target=_blank} 等。

    [_pip]: https://pip.pypa.io/
    [_poetry]: https://python-poetry.org/
    [_pipenv]: https://pipenv.pypa.io/
    [_pdm]: https://pdm.fming.dev/

## 使用 `APIFlask` 类创建 `app` 实例

与创建 Flask `app` 实例类似，你需要从 `apiflask` 包中导入 `APIFlask` 类，然后使用该类创建 `app` 实例：

```python
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
def index():
    return {'message': 'hello'}
```

API 的默认标题和版本号分别为 `APIFlask` 和 `0.1.0`；你可以通过传递 `title` 和 `version` 参数来修改这些设置：

```python
app = APIFlask(__name__, title='Wonderful API', version='1.0')
```

要运行此程序，你可以将其保存为 `app.py`，然后运行 `flask run` 命令：

```bash
$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

如果你的脚本名称不是 `app.py`，在执行 `flask run` 之前需要声明要启动的程序。详见下方说明。

??? note "指定要运行的程序"

    默认情况下，Flask 会在名为 `app` 或 `wsgi` 的模块/包中查找名为 `app` 或 `application` 的程序实例，或名为 `create_app` 或 `make_app` 的程序工厂函数。这就是为什么建议将文件命名为 `app.py`。如果你使用了不同的名称，需要通过 `--app`（Flask 2.2+）选项或环境变量 `FLASK_APP` 告诉 Flask 程序模块的路径。例如，如果你的程序实例存储在名为 `hello.py` 的文件中，则需要将 `--app` 或 `FLASK_APP` 设置为模块名 `hello`：

    ```
    $ flask --app hello run
    ```

    或者：

    === "Bash"

        ```
        $ export FLASK_APP=hello
        ```

    === "Windows CMD"

        ```
        > set FLASK_APP=hello
        ```

    === "Powershell"

        ```
        > $env:FLASK_APP="hello"
        ```

    类似地，如果你的程序实例或程序工厂函数存储在 `mypkg/__init__.py` 中，可以传递包名：

    ```
    $ flask --app mypkg run
    ```

    === "Bash"

        ```
        $ export FLASK_APP=mypkg
        ```

    === "Windows CMD"

        ```
        > set FLASK_APP=mypkg
        ```

    === "Powershell"

        ```
        > $env:FLASK_APP="mypkg"
        ```

    然而，如果程序实例或程序工厂函数存储在 `mypkg/myapp.py` 中，则需要使用：

    ```
    $ flask --app mypkg.myapp run
    ```

    或者：

    === "Bash"

        ```
        $ export FLASK_APP=mypkg.myapp
        ```

    === "Windows CMD"

        ```
        > set FLASK_APP=mypkg.myapp
        ```

    === "Powershell"

        ```
        > $env:FLASK_APP="mypkg.myapp"
        ```

    更多详情请参见 *[程序发现][_app_discovery]{target=_blank}*。

    [_app_discovery]: https://flask.palletsprojects.com/cli/#application-discovery

如果你希望在代码更改时自动重新启动程序，可以使用 `--reload` 选项启用重新加载器：

```bash
$ flask run --reload
```

!!! tip

    安装 `watchdog` 以提升程序重新加载器的性能：

    === "Linux/macOS"

        ```bash
        $ pip3 install watchdog
        ```

    === "Windows"

        ```
        > pip install watchdog
        ```

强烈建议在开发 Flask 程序时启用“调试模式”。详见下方说明。

??? note "启用调试模式"

    Flask 可以在代码更改时自动重新启动和重新加载程序，并在出现错误时显示有用的调试信息。要在 Flask 程序中启用这些功能，需要使用 `--debug` 选项：

    ```
    $ flask run --debug
    ```

    如果你未使用最新的 Flask 版本（>=2.2.3），则需要将环境变量 `FLASK_DEBUG` 设置为 `True`：

    === "Bash"

        ```bash
        $ export FLASK_DEBUG=True
        ```

    === "Windows CMD"

        ```
        > set FLASK_DEBUG=True
        ```

    === "Powershell"

        ```
        > $env:FLASK_DEBUG="True"
        ```

    更多详情请参见 *[调试模式][_debug_mode]{target=_blank}*。

    [_debug_mode]: https://flask.palletsprojects.com/quickstart/#debug-mode

??? "使用 python-dotenv 管理环境变量"

    手动设置环境变量有些不便，因为变量仅在当前终端会话中有效。每次重新打开终端或重启计算机时都需要重新设置。因此，我们需要使用 python-dotenv，Flask 也对此提供了特殊支持。

    使用 pip 安装 `python-dotenv`：

    === "Linux/macOS"

        ```bash
        $ pip3 install python-dotenv
        ```

    === "Windows"

        ```
        > pip install python-dotenv
        ```

    现在，我们可以将环境变量存储在 `.env` 文件中。与 Flask 相关的环境变量应保存在名为 `.flaskenv` 的文件中：

    ```ini
    # 保存为 .flaskenv
    FLASK_APP=hello
    FLASK_DEBUG=1
    ```

    而敏感信息应保存在 `.env` 文件中：

    ```ini
    # 保存为 .env
    SECRET_KEY=some-random-string
    DATABASE_URL=your-database-url
    FOO_APP_KEY=some-app-key
    ```

    !!! warning

        由于 `.env` 文件包含敏感信息，请勿将其提交到 Git 历史记录中。确保通过将文件名添加到 `.gitignore` 来忽略它。

    在程序中，我们现在可以通过 `os.getenv(key, default_value)` 读取这些变量：

    ```python
    import os

    from apiflask import APIFlask

    app = APIFlask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    ```

    任何 `flask` 命令都会读取 `.flaskenv` 和 `.env` 设置的环境变量。现在，当你运行 `flask run` 时，Flask 将读取 `.flaskenv` 文件中的 `FLASK_APP` 和 `FLASK_DEBUG` 的值，以从给定的导入路径中找到程序实例并启用调试模式：

    ```bash
    $ flask run
    * Environment: development
    * Debug mode: on
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 101-750-099
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

    更多详情请参见 *[从 dotenv 加载环境变量][_dotenv]{target=_blank}*。

    [_dotenv]: https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv

## 交互式 API 文档

一旦你创建了程序实例，交互式 API 文档将可通过 <http://localhost:5000/docs> 访问。此外，OpenAPI 规范文件可通过 <http://localhost:5000/openapi.json> 获取。

如果你想预览规范或将其保存到本地文件，请使用 [flask spec 命令](/openapi/#the-flask-spec-command)。

每当你添加新路由或为视图函数添加输入和输出定义时，都可以刷新文档。

有关 API 文档的高级主题，请阅读 *[API 文档](/api-docs)* 章节。

## 使用路由装饰器创建路由

要创建一个视图函数，以前我们会使用 `app.route` 并设置 `methods` 参数：

```python
@app.route('/pets', methods=['POST'])
def create_pet():
    return {'message': 'created'}, 201
```

你可以使用以下快捷装饰器代替：

- `app.get()`: 注册一个只接受 *GET* 请求的路由。
- `app.post()`: 注册一个只接受 *POST* 请求的路由。
- `app.put()`: 注册一个只接受 *PUT* 请求的路由。
- `app.patch()`: 注册一个只接受 *PATCH* 请求的路由。
- `app.delete()`: 注册一个只接受 *DELETE* 请求的路由。

下面是使用快捷装饰器的同一个例子：

```python
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/pets')
def get_pets():
    return {'message': 'OK'}


@app.post('/pets')
def create_pet():
    return {'message': 'created'}, 201


@app.put('/pets/<int:pet_id>')
def update_pet(pet_id):
    return {'message': 'updated'}


@app.delete('/pets/<int:pet_id>')
def delete_pet(pet_id):
    return '', 204
```

!!! note "在一个视图函数中处理多个 HTTP 方法"

    你不能在快捷装饰器中传递 `methods` 参数。如果你希望视图函数接受多个 HTTP 方法，
    你需要使用 `app.route()` 装饰器并传递 `methods` 参数：

    ```python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return {'message': 'hello'}
    ```

    或者你可以这样做：

    ```python
    @app.get('/')
    @app.post('/')
    def index():
        return {'message': 'hello'}
    ```

    顺带一提，在你的程序中，你可以混合使用 `app.route()` 与快捷装饰器。


## 使用 `@app.input` 来验证和反序列化请求数据

要验证和反序列化请求体或请求查询参数，我们需要先创建一个数据模式类。
你可以把它看作是描述合法输入数据的一种方式。如果你熟悉 marshmallow，那么你已经会写 schema 了。

下面是一个用于 Pet 输入资源的简单输入 schema：

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! tip

    参阅 [数据模式章节](/schema) 了解如何编写 schema 和各字段与验证器的使用示例。

* schema 类应继承自 `apiflask.Schema` 类。
* 字段由 `apiflask.fields` 中的字段类表示。
* 若要为字段添加验证规则，你可以将一个验证器或验证器列表（从 `apiflask.validators` 中导入）传递给字段类的 `validate` 参数。

!!! tip

    注意我们通过 `required` 参数标记字段为必填项。
    如果你希望在输入数据中缺少字段时设置默认值，可以使用 `load_default` 参数：

    ```python
    name = String(load_default='default name')
    ```

使用该 schema，我们声明输入请求体应为以下格式：

```json
{
    "name": "宠物的名字",
    "category": "宠物的分类：dog 或 cat"
}
```

!!! notes

    阅读 *[数据模式](/schema)* 章节，了解关于数据模式的高级内容。

现在将其应用到用于创建新宠物的视图函数中：

```python hl_lines="14"
from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


@app.post('/pets')
@app.input(PetIn)
def create_pet(json_data):
    print(json_data)
    return {'message': 'created'}, 201
```

你只需将 schema 类传递给 `@app.input` 装饰器。当接收到请求时，APIFlask 会根据该 schema 验证请求体。

如果你希望更改输入数据的来源，可以传递 `location` 参数给 `@app.input()` 装饰器，取值如下：

- 请求 JSON 体：`'json'`（默认值）
- 上传文件：`'files'`
- 表单数据：`'form'`
- 表单数据与文件：`'form_and_files'`
- Cookies：`'cookies'`
- HTTP 首部：`'headers'`
- 查询字符串：`'query'`（等同于 `'querystring'`）
- 路径变量（URL 变量）：`'path'`（等同于 `'view_args'`，APIFlask 1.0.2 新增）

如果验证通过，数据会以名为 `{location}_data`（如 `json_data`）的关键字参数形式以字典结构传递给视图函数。
否则会返回带有详细验证错误信息的响应。

你可以通过 `arg_name` 设置自定义参数名：

```python
@app.post('/pets')
@app.input(PetIn, arg_name='pet')
def create_pet(pet):
    print(pet)
    return {'message': 'created'}, 201
```

这是一个多个输入数据的示例：

```python
@app.post('/foo')
@app.input(PetIn, location='json')
@app.input(PaginationIn, location='query')
def foo(json_data, query_data):
    return {'message': 'success'}
```

由于解析后的数据是字典，你可以这样创建一个 ORM 模型实例：

```python hl_lines="5"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut)
def create_pet(pet_id, json_data):
    pet = Pet(**json_data)
    return pet
```

或像这样更新一个 ORM 模型实例：

```python hl_lines="6 7"
@app.patch('/pets/<int:pet_id>')
@app.input(PetIn)
@app.output(PetOut)
def update_pet(pet_id, json_data):
    pet = Pet.query.get(pet_id)
    for attr, value in json_data.items():
        setattr(pet, attr, value)
    return pet
```

如果你希望禁用输入验证，可以设置 `validation=False`。这时输入数据会直接传入视图函数，未做任何验证。如果没有输入数据，视图函数将接收到一个空字典：

```python
@app.patch('/pets_without_validation/<int:pet_id>')
@app.input(PetIn, location='json', validation=False)
def pets_without_validation(pet_id, json_data):
    return {'pet_id': pet_id, 'json_data': json_data}
```

`headers` 和 `cookies` 是特殊位置，它们包含所有首部和 cookie 数据，因此不能跳过验证。

!!! warning

    请确保将 `@app.input` 装饰器放在路由装饰器（例如 `app.route`、`app.get`、`app.post` 等）下面。


阅读 *[请求处理](/request)* 章节了解请求处理的高级用法。


## 使用 `@app.output` 格式化响应数据

类似地，我们可以通过 `@app.output` 装饰器为响应数据定义一个 schema。如下所示：

```python
from apiflask.fields import String, Integer


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()
```

由于 APIFlask 不会验证响应数据，我们只需列出所有输出字段即可。

!!! tip

    你可以使用 `dump_default` 为输出字段设置默认值：

    ```python
    name = String(dump_default='default name')
    ```

现在将其添加到用于获取宠物资源的视图函数中：

```python hl_lines="14"
from apiflask import APIFlask
from apiflask.fields import String, Integer

app = APIFlask(__name__)


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    return {
        'name': 'Coco',
        'category': 'dog'
    }
```

输出响应的默认状态码为 `200`，你可以通过 `status_code` 参数设置为其他状态码：

```python
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(json_data):
    pet = Pet(**json_data)
    return pet
```

如果你希望返回 204 响应，可以使用 `apiflask.schemas` 中的 `EmptySchema`：

```python
from apiflask.schemas import EmptySchema


@app.delete('/pets/<int:pet_id>')
@app.output(EmptySchema, status_code=204)
def delete_pet(pet_id):
    return ''
```

`EmptySchema` 表示空 schema。在 204 响应中表示空响应体。

从 0.4.0 版本开始，你也可以使用空字典作为简写：

```python
@app.delete('/pets/<int:pet_id>')
@app.output({}, status_code=204)
def delete_pet(pet_id):
    return ''
```

!!! warning "`@app.output` 装饰器只能使用一次"

    每个视图函数只能定义一个主要成功响应，
    也就是说只能使用一个 `@app.output` 装饰器。
    如果你希望在 OpenAPI 规范中为视图添加更多响应选项，
    可以使用 `@app.doc` 装饰器并通过 `responses` 参数传递响应列表。例如：

    ```python
    @app.put('/pets/<int:pet_id>')
    @app.input(PetIn)
    @app.output(PetOut)  # 200
    @app.doc(responses=[204, 404])
    def update_pet(pet_id, json_data):
        pass
    ```

!!! warning

    请确保将 `@app.output` 装饰器放在路由装饰器（例如 `app.route`、`app.get`、`app.post` 等）下面。


阅读 *[响应格式化](/response)* 章节了解响应格式的高级用法。

## 视图函数的返回值

当使用 `@app.output(schema)` 装饰器时，应该返回一个与传递的 schema 匹配的字典或对象。例如，下面是你的 schema：

```python
from apiflask import Schema
from apiflask.fields import String, Integer


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()
```

现在你可以返回一个字典：

```python
@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    return {
        'id': 1,
        'name': 'Coco',
        'category': 'dog'
    }
```

或者可以直接返回一个 ORM 模型实例：

```python hl_lines="5"
@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    return pet
```

请注意，你的 ORM 模型类应当定义与 schema 类中相匹配的字段：

```python
class Pet(Model):
    id = Integer()
    name = String()
    category = String()
```

!!! tip "如果我想使用不同的外部字段名怎么办？"

    例如，在你的 ORM 模型类中，你有一个 `phone` 字段，
    用于存储用户的电话号码：

    ```python
    class User(Model):
        phone = String()
    ```

    现在你想将该字段输出为 `phone_number`，那么你可以使用
    `data_key` 来声明实际的键名：

    ```python
    class UserOut(Schema):
        phone = String(data_key='phone_number')
    ```

    这个 schema 会生成类似 `{'phone_number': ...}` 的输出。

    类似地，你可以告诉 APIFlask 在输入 schema 中从不同的键加载数据：

    ```python
    class UserIn(Schema):
        phone = String(data_key='phone_number')
    ```

    这个 schema 期望用户输入类似 `{'phone_number': ...}` 的数据。

默认的状态码是 `200`，如果你想使用不同的状态码，
可以在 `@app.output` 装饰器中传递一个 `status_code` 参数：

```python
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(json_data):
    # ...
    return pet
```

你不需要在视图函数的最后返回相同的状态码
（即 `return data, 201`）：

```python
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(json_data):
    # ...
    # 等同于：
    # return pet, 201
    return pet
```

当你想传递一个 header 字典时，可以将字典作为返回元组的第二个元素传递：

```python
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(json_data):
    # ...
    # 等同于：
    # return pet, 201, {'FOO': 'bar'}
    return pet, {'FOO': 'bar'}
```

!!! tip

    当你想使用非 200 状态码时，确保在 `@app.output` 中始终设置 `status_code` 参数。
    如果存在不匹配的情况，`@app.output` 中传递的 `status_code` 将用于 OpenAPI 规范，而实际响应将使用你在视图函数末尾返回的状态码。

## OpenAPI 生成支持和 `@app.doc` 装饰器

APIFlask 提供自动生成 OpenAPI 规范的支持，同时允许
你自定义规范：

* `info` 对象的大多数字段和 `OpenAPI` 对象的顶级字段都可以通过配置变量访问。
* `tag` 对象、操作的 `summary` 和 `description` 将从蓝图名称、视图函数名称和文档字符串生成。
* 你可以注册一个规范处理函数来处理规范。
* `requestBody` 和 `responses` 字段可以通过 `input` 和 `output` 装饰器设置。
* 其他操作字段可以通过 `@app.doc` 装饰器设置：

```python hl_lines="7"
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/hello')
@app.doc(summary='Say hello', description='Some description for the /hello')
def hello():
    return 'Hello'
```

有关 OpenAPI 生成和 `doc` 装饰器的更多详细信息，请参阅 *[使用 `doc` 装饰器](/openapi/#use-the-doc-decorator)*。

!!! warning

    确保将 `@app.doc` 装饰器放在路由装饰器下方
    （即 `app.route`、`app.get`、`app.post` 等）。

## 使用 `@app.auth_required` 来保护视图

基于 [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)，APIFlask
提供了三种认证方式：

### HTTP 基本认证

要实现 HTTP 基本认证，你需要：

* 创建一个 `auth` 对象，使用 `HTTPBasicAuth`
* 使用 `@auth.verify_password` 注册一个回调函数，该函数应接受 `username` 和 `password`，返回对应的用户对象或 `None`。
* 使用 `@app.auth_required(auth)` 保护视图函数。
* 在视图函数中使用 `auth.current_user` 访问当前用户对象。

```python
from apiflask import APIFlask, HTTPBasicAuth

app = APIFlask(__name__)
auth = HTTPBasicAuth()  # 创建认证对象


@auth.verify_password
def verify_password(username, password):
    # 从数据库获取用户，检查密码
    # 如果密码匹配，则返回用户
    # ...

@app.route('/')
@app.auth_required(auth)
def hello():
    return f'Hello, {auth.current_user}!'
```

!!! tip

    要访问当前的用户对象，你需要在视图函数中使用 `auth.current_user` 属性。
    这等同于在 Flask-HTTPAuth 中使用 `auth.current_user()` 方法。

### HTTP Bearer 认证

要实现 HTTP Bearer 认证，你需要：

* 创建一个 `auth` 对象，使用 `HTTPTokenAuth`
* 使用 `@auth.verify_token` 注册一个回调函数，该函数应接受 `token`，返回对应的用户对象或 `None`。
* 使用 `@app.auth_required(auth)` 保护视图函数。
* 在视图函数中使用 `auth.current_user` 访问当前用户对象。

```python
from apiflask import APIFlask, HTTPTokenAuth

app = APIFlask(__name__)
auth = HTTPTokenAuth()  # 创建认证对象
# 或者使用 HTTPTokenAuth(scheme='Bearer')


@auth.verify_token  # 注册回调函数以验证令牌
def verify_token(token):
    # 验证令牌并获取用户 ID
    # 然后从数据库查询并返回对应的用户
    # ...

@app.get('/')
@app.auth_required(auth)  # 保护视图
def hello():
    # 使用 auth.current_user 访问当前用户
    return f'Hello, {auth.current_user}!'
```

### API 密钥（在首部）

与 Bearer 类型相似，但在创建认证对象时将 `scheme` 设置为 `ApiKey`：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey')
```

或者使用自定义首部：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey', header='X-API-Key')

# ...
```

你可以使用 `description` 参数设置 OpenAPI 安全描述
在 `HTTPBasicAuth` 和 `HTTPTokenAuth` 中。

请参阅 [Flask-HTTPAuth 文档][_flask-httpauth] 了解更多详细信息。但是，记住要
从 APIFlask 导入 `HTTPBasicAuth` 和 `HTTPTokenAuth`，并使用 `@app.auth_required`
而不是 `@auth.login_required` 来保护视图函数。

!!! warning

    确保将 `@app.auth_required` 装饰器放在路由装饰器下方
    （即 `app.route`、`app.get`、`app.post` 等）。

[_flask-httpauth]: https://flask-httpauth.readthedocs.io/

请阅读 *[认证](/authentication)* 章节了解认证的高级主题。

## 使用基于类的视图

!!! warning "版本 >= 0.5.0"

    此功能是在 [版本 0.5.0](/changelog/#version-050) 中新增的。

你可以使用 `MethodView` 类创建一组路由，属于相同的 URL 规则。
下面是一个简单的示例：

```python
from apiflask import APIFlask
from flask.views import MethodView

app = APIFlask(__name__)


class Pet(MethodView):

    def get(self, pet_id):
        return {'message': 'OK'}

    def delete(self, pet_id):
        return '', 204


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

创建视图类时，需要继承自 `MethodView` 类，因为 APIFlask
只能为基于 `MethodView` 的视图类生成 OpenAPI 规范。

现在，你可以为每种 HTTP 方法定义视图方法，使用（HTTP）方法名称作为方法名：

```python
class Pet(MethodView):

    def get(self, pet_id):  # 由 GET 请求触发
        return {'message': 'OK'}

    def post(self, pet_id):  # 由 POST 请求触发
        return {'message': 'OK'}

    def put(self, pet_id):  # 由 PUT 请求触发
        return {'message': 'OK'}

    def delete(self, pet_id):  # 由 DELETE 请求触发
        return '', 204

    def patch(self, pet_id):  # 由 PATCH 请求触发
        return {'message': 'OK'}


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

在上述示例中，当用户向 `/pets/<int:pet_id>` 发送 *GET* 请求时，
将调用 `Pet` 类的 `get()` 方法，其他请求类型同理。

通常情况下，你不需要指定方法，除非你想为一个视图类注册多个规则。例如，将 `post` 方法
注册到与其他方法不同的 URL 规则：

```python
class Pet(MethodView):
    # ...

pet_view = Pet.as_view('pet')
app.add_url_rule('/pets/<int:pet_id>', view_func=pet_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])
app.add_url_rule('/pets', view_func=pet_view, methods=['POST'])
```

但是，你可能希望为不同的 URL 规则创建独立的类。

当使用像 `@app.input`、`@app.output` 这样的装饰器时，请确保它们应用于方法而不是类：

```python
class Pet(MethodView):

    @app.output(PetOut)
    @app.doc(summary='Get a pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetIn)
    @app.output(PetOut)
    def put(self, pet_id, json_data):
        # ...

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, json_data):
        # ...


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

如果你想为所有方法应用装饰器，可以将装饰器传递给类属性 `decorators`，它接受
一个装饰器列表：

```python
class Pet(MethodView):

    decorators = [auth_required(auth), doc(responses=[404])]

    @app.output(PetOut)
    @app.doc(summary='Get a pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetIn)
    @app.output(PetOut)
    def put(self, pet_id, json_data):
        # ...

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, json_data):
        # ...


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

阅读 [Flask 文档关于基于类的视图](https://flask.palletsprojects.com/views/) 了解更多信息。

## 使用 `abort()` 返回错误响应

与 Flask 中的 `abort` 类似，但 APIFlask 中的 `abort` 会返回一个 JSON 响应。

示例：

```python
from apiflask import APIFlask, abort

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        abort(404, 'This user is missing.')
    return {'hello': name}
```

!!! tip

    当 `app.json_errors` 为 `True`（默认值）时，Flask 的 `abort` 也会返回
    JSON 错误响应。

你也可以通过抛出 `HTTPError` 异常来返回错误响应：

```python
from apiflask import APIFlask, HTTPError

app = APIFlask(__name__)

@app.get('/users/<name>')
def hello(name):
    if name == 'Foo':
        raise HTTPError(404, 'This user is missing.')
    return {'hello': name}
```

`abort()` 和 `HTTPError` 接受以下参数：

* `status_code`：错误的状态码（4XX 和 5XX）。
* `message`：错误的简短描述。如果未提供，状态码的原因短语将被使用。
* `detail`：错误的详细信息，可用于提供附加信息，如自定义错误代码、文档 URL 等。
* `headers`：用于错误响应的首部字典。

!!! warning

    `abort_json()` 函数在 [版本 0.4.0](/changelog/#version-040) 中被重命名为 `abort()`。

## `apiflask` 包概览

最后，让我们来看看 `apiflask` 包中包含的内容：

* `APIFlask`：用于创建程序实例的类（Flask 的 `Flask` 类的包装器）。
* `APIBlueprint`：用于创建蓝图实例的类（Flask 的 `Blueprint` 类的包装器）。
* `@app.input()`：用于验证请求体、查询字符串等的输入/请求数据的装饰器。
* `@app.output()`：用于格式化响应的装饰器。
* `@app.auth_required()`：用于保护视图，防止未认证用户访问的装饰器。
* `@app.doc()`：用于为视图函数设置 OpenAPI 规范的装饰器。
* `abort()`：用于中止请求处理过程并返回错误响应的函数。Flask 的 `flask.abort()` 函数的 JSON 版本。
* `HTTPError`：用于返回错误响应的异常（由 `abort()` 使用）。
* `HTTPBasicAuth`：用于创建认证实例的类。
* `HTTPTokenAuth`：用于创建认证实例的类。
* `Schema`：资源模式的基类（将是 marshmallow 的 `Schema` 的包装器）。
* `fields`：一个模块，包含所有字段（来自 marshmallow）。
* `validators`：一个模块，包含所有字段验证器（来自 marshmallow）。
* `app.get()`：用于注册仅接受 *GET* 请求的路由的装饰器。
* `app.post()`：用于注册仅接受 *POST* 请求的路由的装饰器。
* `app.put()`：用于注册仅接受 *PUT* 请求的路由的装饰器。
* `app.patch()`：用于注册仅接受 *PATCH* 请求的路由的装饰器。
* `app.delete()`：用于注册仅接受 *DELETE* 请求的路由的装饰器。
* `app.route()`：用于注册路由的装饰器。它接受 `methods` 参数来指定接受的方法列表，默认为仅 *GET*。它也可以用于 `MethodView` 基础的视图类。
* `$ flask spec`：一个命令，用于将规范输出到标准输出或文件。

你可以在 [API 参考](/api/app) 中详细了解这些 API，或者继续阅读接下来的章节。
