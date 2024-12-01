# 基本用法

本章将介绍 APIFlask 的主要用法。

## 要求

- Python 3.7+
- Flask 1.1+

在此之前，你还需要了解 Flask 的基本知识。这里有一些有用的免费资源学习 Flask ：

- [Flask's Documentation（官方文档）](https://flask.palletsprojects.com/){target=_blank}
- [Official Flask Tutorial（官方教程）](https://flask.palletsprojects.com/tutorial/#tutorial){target=_blank}
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
  {target=_blank}
- [Flask for Beginners](https://github.com/greyli/flask-tutorial){target=_blank} (中文)

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

    以上的命令是通过 [pip][_pip]{target=_blank} 来安装 APIFlask， 你也可以通过其他依赖管理工具如
    [Poetry][_poetry]{target=_blank}、[Pipenv][_pipenv]{target=_blank}、[PDM][_pdm]{target=_blank}
    等来安装.

    [_pip]: https://pip.pypa.io/
    [_poetry]: https://python-poetry.org/
    [_pipenv]: https://pipenv.pypa.io/
    [_pdm]: https://pdm.fming.dev/


## 使用 `APIFlask` 类创建 `app` 实例

与 Flask 创建 `app` 实例类似，你需要从 `apiflask` 包中导入 `APIFlask` 类，再通过
`APIFlask` 类创建 `app` 实例：

```python hl_lines="1 3"
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
def index():
    return {'message': 'hello'}
```

API 的默认标题和版本号为 `APIFlask` 和 `0.1.0`；你可以 指定 `title` 和 `version` 参数来更改这些设置：

```python
app = APIFlask(__name__, title='Wonderful API', version='1.0')
```

要运行程序，你需要将代码保存为 `app.py` 文件，然后使用 `flask run` 命令运行：

```bash
$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

如果脚本的名称不是 `app.py`，则需要在执行 `flask run` 命令时声明你要运行的应用。
更多详细信息，请参阅下面的注释。

??? note "指定要运行的特定应用"

    默认情况下，Flask 将在名为 `app` 或 `wsgi` 的模块/包中查找名为 `app` 或 `application`
    的应用实例，或查找名为 `create_app` 或 `make_app` 的应用工厂函数。因此，我推荐将文件命名
    为 `app.py`。如果你使用不同的名称，你需要通过 `--app` （Flask 2.2+）选项或环境变量 `FLASK_APP`
    来告诉 Flask 应用模块的路径。例如，如果你的应用实例存储在名为 `hello.py` 的文件中，那么需要将
    `--app` 或 `FLASK_APP` 设置为模块名称 `hello`：

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

    同样的，如果应用实例或应用工厂函数存储在 `mypkg/__init__.py` 中，你可以传递包名：

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

    但是，如果你的应用实例或者应用工厂函数存储在 `mypkg/myapp.py` 中，你需要使用：

    ```
    $ flask --app mypkg.myapp run
    ```

    或者:

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

    查看 *[Application Discovery][_app_discovery]{target=_blank}* 获取更多详细信息。

    [_app_discovery]: https://flask.palletsprojects.com/cli/#application-discovery

如果你想在代码更改时自动重启应用，可以使用 `--reload` 选项:

```bash
$ flask run --reload
```

!!! tip

    安装 `watchdog` 以获得更好的重启性能：

    === "Linux/macOS"

        ```bash
        $ pip3 install watchdog
        ```

    === "Windows"

        ```
        > pip install watchdog
        ```

我们推荐在开发 Flask 应用时启用“调试模式”。查看以下注释了解更多细节。

??? note "开启调试模式"

    Flask 可以在代码更改时自动重启和重新加载应用程序，并显示有用的错误调试信息。
    要在 Flask 应用中启用这些功能，我们需要使用 `--debug` 选项：

    ```
    $ flask --debug run
    ```

    如果使用的不是最新的 Flask 版本（> 2.2），你需要将环境变量 `FLASK_DEBUG` 设置为 `True`。

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

    查看 *[Debug Mode][_debug_mode]{target=_blank}* 获取更多关于调试模式的信息。

    [_debug_mode]: https://flask.palletsprojects.com/quickstart/#debug-mode


## 使用 python-dotenv 管理环境变量

手动设置环境变量很麻烦，因为变量只在当前的终端会话中存在。你必须在每次重新打开终端或重启电脑时都设置它。
这就是为什么我们需要使用 python-dotenv，同样 Flask 还有专门的支持。

通过pip安装 `python-dotenv` ：

=== "Linux/macOS"

    ```bash
    $ pip3 install python-dotenv
    ```

=== "Windows"

    ```
    > pip install python-dotenv
    ```

现在，我们可以将环境变量存储在 .env 文件中。Flask 相关的环境变量应该保存在名为 `.flaskenv` 的文件中：

```ini
# save as .flaskenv
FLASK_APP=hello
FLASK_ENV=development
```

当需要保存敏感信息时，应该保存在名为 `.env` 的文件中：

```ini
# save as .env
SECRET_KEY=some-random-string
DATABASE_URL=your-database-url
FOO_APP_KEY=some-app-key
```

!!! warning

    当 `.env` 中包含敏感信息时，请不要将其提交到 Git 历史中。确保将其添加到 `.gitignore` 中。

现在，我们可以在应用程序中通过 `os.getenv(key, default_value)` 获取这些变量：

```python hl_lines="1 5"
import os

from apiflask import APIFlask

app = APIFlask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
```

任何 `flask` 命令都会读取 `.flaskenv` 和 `.env` 中的环境变量。现在当你运行 `flask run`，
Flask会获取 `FLASK_APP` 和 `FLASK_ENV` 的值来查找应用实例，并启用调试模式:

```bash
$ flask run
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 101-750-099
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

查看 *[Environment Variables From dotenv][_dotenv]{target=_blank}* 获取更多关于环境变量的信息。

[_dotenv]: https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv

## 交互式 API 文档

创建应用实例后，可以通过 <http://localhost:5000/docs> 查看交互式 API 文档，除此之外，也可以通过
<http://localhost:5000/openapi.json> 查看 OpenAPI 规范文件。

如果想在本地预览规范文件，使用 [the `flask spec` command](/openapi/#the-flask-spec-command) 命令

当你添加了新的路由或添加了视图函数的输入和输出定义时，也可以刷新此文档。

阅读 *[API 文档](/api-docs)* 获取更多关于 API 文档的信息。

## 使用路由修饰器创建路由


对于创建视图函数，你可以使用与 Flask 相同的方式：

```python
from apiflask import APIFlask

app = APIFlask(__name__)


@app.route('/')
def index():
    return {'message': 'hello'}


@app.route('/pets/<int:pet_id>')
def get_pet(pet_id):
    return {'message': 'OK'}


@app.route('/pets')
def get_pets():
    return {'message': 'OK'}


@app.route('/pets', methods=['POST'])
def create_pet():
    return {'message': 'created'}, 201


@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    return {'name': 'updated'}


@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    return '', 204
```

但是，你也可以通过 APIFlask 使用快捷路由修饰器来替代路由装饰器的 `methods` 参数:

- `app.get()`: 注册 *GET* 请求的路由。
- `app.post()`: 注册 *POST* 请求的路由。
- `app.put()`: 注册 *PUT* 请求的路由。
- `app.patch()`: 注册 *PATCH* 请求的路由。
- `app.delete()`: 注册 *DELETE* 请求的路由。

这里是使用这些路由修饰器的例子：

```python hl_lines="6 11 16 21 26 31"
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
def index():
    return {'message': 'hello'}


@app.get('/pets/<int:pet_id>')
def get_pet(pet_id):
    return {'message': 'OK'}


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

!!! note "在视图函数中处理多种 HTTP 方法"

    如果想让视图函数接受多种 HTTP 方法，你不能在快捷路由修饰器中使用 `methods` 参数。
    只使用 `app.route()` 装饰器来传递 `methods` 参数：

    ```python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return {'message': 'hello'}
    ```

    或者你可以这样做:

    ```python
    @app.get('/')
    @app.post('/')
    def index():
        return {'message': 'hello'}
    ```

    通过这种方式，你可以应用中混合使用 `app.route()` 装饰器和快捷路由修饰器。


## 迁移到新的 API 装饰器

从 APIFlask 0.12 起，四个单独的 API 装饰器（即 `@input`, `@output`, `@doc`, 和 `@auth_required`）
已被移动到 `APIFlask` 和 `APIBlueprint` 类中。现在可以通过应用或蓝图实例来访问它们:

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.get('/')
@app.input(Foo)
@app.output(Bar)
def hello():
    return {'message': 'Hello'}
```

使用以上方式来替代：

```python
from apiflask import APIFlask, input, output

app = APIFlask(__name__)

@app.get('/')
@input(Foo)
@output(Bar)
def hello():
    return {'message': 'Hello'}
```

旧的单独装饰器从 0.12 版本起已被弃用，同时将在 1.0 版本中移除。注意在文档中所有的用法都已更新，
如果你需要升级 APIFlask，可以参考 [升级指南](/changelog/)。


## 使用 `@app.input` 来验证请求数据和反序列化

要验证和反序列化请求数据或请求查询参数，首先需要创建一个 schema 类。这是一种有效地描述输入数据的方式。
如果你已经熟悉了 marshmallow，那么你已经知道如何编写一个 schema。

这是一个简单的 schema 用于 Pet 类输入：

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! tip

    查看 Schema 和 Fields 章节（WIP）了解更多关于如何编写 schema 和字段以及验证器的信息。

schema 类应该继承 `apiflask.Schema` 类。

```python hl_lines="1 6"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

字段使用 `apiflask.fields` 中的字段类：

```python hl_lines="2 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

要使用特定规则验证字段，可以将验证器或验证器列表（从 `apiflask.validators` 导入验证器）
传递给字段类的 `validate` 参数。

```python hl_lines="3 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! tip

    注意，我们可以使用 `required` 参数将字段标记为必填字段。如果你想在输入数据缺失该字段时使用默认值，
    可以使用 `load_default` 参数:

    ```python
    name = String(load_default='default name')
    ```

通过此 schema，我们声明输入请求体应该以下格式出现:

```json
{
    "name": "the name of the pet",
    "category": "the category of the pet: one of dog and cat"
}
```
!!! notes

    查看 *[数据 Schema](/schema)* 章节了解更多关于数据 Schema 的信息。

现在，让我们将其添加到新建宠物的视图函数中:

```python hl_lines="1 14"
from apiflask import APIFlask, Schema, input
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


@app.post('/pets')
@app.input(PetIn)
def create_pet(data):
    print(data)
    return {'message': 'created'}, 201
```

只需要将 schema 类传递给 `@app.input` 装饰器。当收到请求时，APIFlask 将通过此 schema 验证请求体。

如果验证通过，数据将转换为 `dict` 注入到视图函数的位置参数中。否则，返回验证结果的错误响应。

在上面的例子中，使用 `data` 来接受输入数据字典。你可以将参数名更改为想使用的名字。
同时，你可以从这个字典中创建一个 ORM 模型实例。

```python hl_lines="5"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut)
def create_pet(pet_id, data):
    pet = Pet(**data)
    return pet
```

或者像这样更新 ORM 模型实例:

```python hl_lines="6 7"
@app.patch('/pets/<int:pet_id>')
@app.input(PetIn)
@app.output(PetOut)
def update_pet(pet_id, data):
    pet = Pet.query.get(pet_id)
    for attr, value in data.items():
        setattr(pet, attr, value)
    return pet
```

如果想将输入标记为请求的不同的位置，可以传递 `location` 参数给 `@app.input()` 装饰器，该值可以是:

- 请求JSON正文： `'json'` （默认值）
- 上传文件： `'files'`
- 表单数据： `'form'`
- 表单数据和文件： `'form_and_files'`
- Cookies： `'cookies'`
- HTTP 请求头： `'headers'`
- 查询参数: `'query'` （同 `'querystring'`）
- Path 变量（URL变量）： `'path'` （同 APIFlask 1.0.2 增加的 `'view_args'` 参数）

!!! warning

    请确保 `@app.input` 装饰器位于路由装饰器之下（即 `app.route` 、`app.get` 、`app.post` 等）。


查看 *[请求处理](/request)* 章节了解更多关于请求处理的信息。


## 使用 `@app.output` 来格式化响应数据

同样的，我们可以使用 `@app.output` 装饰器来定义输出数据的 schema。这是一个示例：

```python
from apiflask.fields import String, Integer


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()
```

在 APIFlask 中不会验证输出数据，我们只需要在输出数据的 schema 中列出所有字段。

!!! tip

    你可以使用 `dump_default` 参数设置输出字段的默认值：

    ```python
    name = String(dump_default='default name')
    ```

现在将它添加到获取宠物资源的视图函数中:

```python hl_lines="1 14"
from apiflask import APIFlask, output
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

输出响应的默认状态码为 `200`，你可以使用 `status_code` 设置不同的状态码：

```python hl_lines="3"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(data):
    data['id'] = 2
    return data
```

或者只是:

```python
@app.output(PetOut, status_code=201)
```

如果想要返回一个 204 响应，你可以使用从 `apiflask.schemas` 中导入的 `EmptySchema`:

```python hl_lines="1 5"
from apiflask.schemas import EmptySchema


@app.delete('/pets/<int:pet_id>')
@app.output(EmptySchema, status_code=204)
def delete_pet(pet_id):
    return ''
```

从 0.4.0 版本开始，可以使用空字典来表示空 schema：

```python hl_lines="2"
@app.delete('/pets/<int:pet_id>')
@app.output({}, status_code=204)
def delete_pet(pet_id):
    return ''
```

!!! warning " `@app.output` 装饰器只能使用一次"

    对于视图函数，只能定义一个主要成功响应，这意味着只能使用一次 `@app.output` 装饰器。
    如果想要在 OpenAPI 规范中为视图函数添加更多的备选响应，你可以使用 `@app.doc`，并传递
    一个列表到 `responses` 参数。
    比如：

    ```python hl_lines="4"
    @app.put('/pets/<int:pet_id>')
    @app.input(PetIn)
    @app.output(PetOut)  # 200
    @app.doc(responses=[204, 404])
    def update_pet(pet_id, data):
        pass
    ```

!!! warning

    请确保 `@app.output` 装饰器位于路由装饰器之下（即 `app.route`、 `app.get`、 `app.post` 等）。


查看 *[响应格式](/response)* 章节了解更多关于响应格式的信息。


## 视图函数的返回值

当你使用 `@app.output(schema)` 装饰器时，应该返回与传递的 schema 匹配的字典或对象。
例如，这是你的 schema：

```python
from apiflask import Schema
from apiflask.fields import String, Integer


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()
```

现在可以返回一个字典：

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

或者直接返回 ORM 模型实例:

```python hl_lines="5"
@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    return pet
```

注意，ORM 模型类应该包含在 schema 类中定义的字段。

```python
class Pet(Model):
    id = Integer()
    name = String()
    category = String()
```

!!! tip "如果我想使用其他外部字段名怎么办？"

    例如，ORM 模型类中有一个 `phone` 字段，它存储用户的电话号码：

    ```python
    class User(Model):
        phone = String()
    ```

    现在想输出字段的名为 `phone_number`，那么你可以使用 `data_key` 声明实际的键名：

    ```python
    class UserOut(Schema):
        phone = String(data_key='phone_number')
    ```

    这个 schema 会生成一个字典，就像 `{'phone_number': ...}`。

    同样的，你可以在输入 schema 中使用 `data_key` 声明实际的键名：

    ```python
    class UserIn(Schema):
        phone = String(data_key='phone_number')
    ```

    这个 schema 会输入你期望的字典，就像 `{'phone_number': ...}`。

默认的状态码是 `200`，如果想使用不同的状态码，你可以在 `@app.output` 装饰器中传递一个 `status_code` 参数：

```python hl_lines="3"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(data):
    # ...
    return pet
```

你不需要在视图函数的最后返回相同的状态码 （例如， `return data, 201`）:

```python hl_lines="8"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(data):
    # ...
    # 等同于：
    # return pet, 201
    return pet
```

当你想要传递请求头字典数据时，在 return 元组的第二个参数传递：

```python hl_lines="8"
@app.post('/pets')
@app.input(PetIn)
@app.output(PetOut, status_code=201)
def create_pet(data):
    # ...
    # 等同于：
    # return pet, 201, {'FOO': 'bar'}
    return pet, {'FOO': 'bar'}
```

!!! tip

    请确保 `@app.output` 中的 `status_code` 仅在你想要使用非 200 状态码时设置。如果存在设置的与实际返回不匹配情况，
    OpenAPI 规范中会使用 `@app.output` 中的 `status_code` ，而实际响应将使用你在视图函数中返回的状态码。


## OpenAPI 生成支持和 `@app.doc` 装饰器

APIFlask 提供了 OpenAPI 规范生成支持，同时还允许你自定义规范：

- 大部分 `info` 对象的字段和 `OpenAPI` 对象的顶层字段都可以通过变量配置。
- `tag` 、 `summary` 和 `description` 可以从蓝图名、视图函数名和 docstring 中生成。
- 你可以注册规范处理函数来处理规范。
- `requestBody` 和 `responses` 字段可以通过 `input` 和 `output` 装饰器设置。
- 其他操作字段可以通过 `doc` 装饰器设置：

```python hl_lines="1 7"
from apiflask import APIFlask, doc

app = APIFlask(__name__)


@app.get('/hello')
@app.doc(summary='Say hello', description='Some description for the /hello')
def hello():
    return 'Hello'
```

查看 [使用 `doc` 装饰器](/openapi/#use-the-doc-decorator) 获取更多关于 OpenAPI 规范生成
和 `doc` 装饰器的使用信息。

!!! warning

    请确保 `@app.doc` 装饰器在路由装饰器之下（即 `app.route`、 `app.get`、 `app.post` 等）。


## 使用 `@app.auth_required` 来保护你的视图

基于 [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)，APIFlask 提供了三种认证方式：

### HTTP Basic

实现 HTTP 基本认证，你需要:

- 通过 `HTTPBasicAuth` 类创建 `auth` 对象。
- 使用 `@auth.verify_password` 注册一个回调函数，这个函数应该接受 `username` 和 `password` 作为参数，
返回对应的用户对象或 `None`。
- 使用 `@app.auth_required(auth)` 保护视图函数。
- 在视图函数中通过 `auth.current_user` 访问当前用户。

```python
from apiflask import APIFlask, HTTPBasicAuth

app = APIFlask(__name__)
auth = HTTPBasicAuth()  # 创建一个认证对象


@auth.verify_password
def verify_password(username, password):
    # 从数据库中获取用户并校验密码
    # 如果密码匹配则返回用户
    # ...

@app.route('/')
@app.auth_required(auth)
def hello():
    return f'Hello, {auth.current_user}!'
```

### HTTP Bearer

实现 HTTP Bearer 认证，你需要:

- 通过 `HTTPTokenAuth` 类创建 `auth` 对象。
- 使用 `@auth.verify_password` 注册一个回调函数，这个函数应该接受 `token` 作为参数，返回对应的用户对象或 `None`。
- 使用 `@app.auth_required(auth)` 保护视图函数。
- 在视图函数中通过 `auth.current_user` 访问当前用户。

```python
from apiflask import APIFlask, HTTPTokenAuth

app = APIFlask(__name__)
auth = HTTPTokenAuth()  # 创建一个认证对象
# 或者使用 HTTPTokenAuth(scheme='Bearer')


@auth.verify_token  # 注册一个用于验证 token 的回调函数
def verify_token(token):
    # 校验 token 和获取用户 id
    # 然后从数据库中查询并返回相应的用户
    # ...

@app.get('/')
@app.auth_required(auth)  # 保护视图
def hello():
    # 通过 auth.current_user 访问当前用户
    return f'Hello, {auth.current_user}'!
```

### API Keys (在请求头中)

和 Bearer 类似，但在创建 auth 对象时设置 `scheme` 为 `ApiKey`：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey')
```

或者自定义请求头：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey', header='X-API-Key')

# ...
```

你可以通过 `description` 参数在 `HTTPBasicAuth` 和 `HTTPTokenAuth` 中设置 OpenAPI 安全描述。

查看 [Flask-HTTPAuth's documentation][_flask-httpauth] 来了解更多详情。但请记住从 APIFlask
中导入 `HTTPBasicAuth` 和 `HTTPTokenAuth`，并使用 `@app.auth_required` 而不是 `@auth.login_required`
作为你的视图函数认证。

!!! warning

    请确保 `@app.auth_required` 装饰器在路由装饰器之下（即 `app.route`、 `app.get`、 `app.post` 等）。

[_flask-httpauth]: https://flask-httpauth.readthedocs.io/

阅读 *[认证](/authentication)* 章节获取更多高级认证主题。


## 使用基于类的视图

!!! warning "Version >= 0.5.0"

    这个特性在 [version 0.5.0](/changelog/#version-050) 中添加 。

你可以通过 `MethodView` 类在同一个 URL 规则下创建一组路由，这里是一个简单的例子：

```python
from apiflask import APIFlask
from apiflask.views import MethodView

app = APIFlask(__name__)


class Pet(MethodView):

    def get(self, pet_id):
        return {'message': 'OK'}

    def delete(self, pet_id):
        return '', 204


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

当创建一个视图类时，它需要继承自 `MethodView` 类，因为 APIFlask 从继承于 `MethodView` 基类的视图类中
生成 OpenAPI 规范。

现在，你可以为每个 HTTP 方法定义视图方法，使用 (HTTP) 方法名作为视图函数名:

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

对于上述示例应用，当用户发送一个 *GET* 请求到 `pets/<int:pet_id>` 时， `Pet` 类的 `get()` 方法将被调用，以此类推。

通常你不需要在路由规则中指定方法名，除非你想为一个视图类注册多个 URL 规则。例如，注册 `post` 方法到其他 URL 规则中:

```python
class Pet(MethodView):
    # ...

pet_view = Pet.as_view('pet')
app.add_url_rule('/pets/<int:pet_id>', view_func=pet_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])
app.add_url_rule('/pets', view_func=pet_view, methods=['POST'])
```

然而，你可能希望为不同的 URL 规则创建不同的类。

当使用 `@app.input`、`@app.output` 这类的装饰器时，一定要在方法上使用它，而不是类：

```python
class Pet(MethodView):

    @app.output(PetOut)
    @app.doc(summary='Get a Pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetIn)
    @app.output(PetOut)
    def put(self, pet_id, data):
        # ...

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, data):
        # ...


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

如果想将装饰器应用于所有方法，你可以将装饰器传递给类属性 `decorators`，它用于接收一个装饰器列表:

```python hl_lines="3"
class Pet(MethodView):

    decorators = [auth_required(auth), doc(responses=[404])]

    @app.output(PetOut)
    @app.doc(summary='Get a Pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetIn)
    @app.output(PetOut)
    def put(self, pet_id, data):
        # ...

    @app.input(PetIn(partial=True))
    @app.output(PetOut)
    def patch(self, pet_id, data):
        # ...


app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

阅读 [Flask docs on class-based views](https://flask.palletsprojects.com/views/) 获取更多关于类视图的信息。


## 使用 `abort()` 返回错误响应

与 Flask 的 `abort` 不同，APIFlask 的 `abort` 会返回一个 JSON 响应。

例:

```python hl_lines="1 8"
from apiflask import APIFlask, abort

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        abort(404, 'This man is missing.')
    return {'hello': name}
```

!!! tip

    当 `app.json_errors` 为 `True`（默认） 时，Flask 的 `abort` 也会返回 JSON 格式的错误响应。

你也可以使用 `HTTPError` 异常来返回错误响应：

```python hl_lines="1 8"
from apiflask import APIFlask, HTTPError

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        raise HTTPError(404, 'This man is missing.')
    return {'hello': name}
```

`abort()` 和 `HTTPError` 接受以下参数:

- `status_code`: 错误状态码（4XX 和 5XX）。
- `message`: 简单的错误描述。如果未提供，将使用状态码的原因短语。
- `detail`: 错误的详细信息，它可以用于提供额外的信息，例如自定义错误代码、文档 URL 等。
- `headers`: 一个用于错误响应的请求头字典。

!!! warning

    在 [ version 0.4.0](/changelog/#version-040) 中，`abort_json()` 被重命名为 `abort()`。


## `apiflask` 包概述

最终，我们来解包整个 `apiflask` 包，看看它包含了哪些内容：

- `APIFlask`：一个用于创建应用实例的类（Flask 类的包装）。
- `APIBlueprint`：一个用于创建蓝图实例的类（Flask `Blueprint` 类的包装）。
- `@app.input()`：用于验证请求数据（如请求体、查询字符串等）的装饰器。
- `@app.output()`：用于格式化响应数据的装饰器。
- `@app.auth_required()`：用于保护视图，防止未经认证的用户访问的装饰器。
- `@app.doc()`：用于设置视图函数的 OpenAPI 规范的装饰器。
- `abort()`：用于中止请求处理并返回错误响应的函数。是 Flask 的 `abort()` 函数的 JSON 版本。
- `HTTPError`：用于返回错误响应的异常（由 `abort()` 使用）。
- `HTTPBasicAuth`：一个用于创建基本认证实例的类。
- `HTTPTokenAuth`：一个用于创建令牌认证实例的类。
- `Schema`：用于资源模式的基类（是 Marshmallow `Schema` 的包装）。
- `fields`：包含所有字段的模块（来自 Marshmallow）。
- `validators`：包含所有字段验证器的模块（来自 Marshmallow）。
- `app.get()`：用于注册仅接受 *GET* 请求的路由装饰器。
- `app.post()`：用于注册仅接受 *POST* 请求的路由的装饰器。
- `app.put()`：用于注册仅接受 *PUT* 请求的路由的装饰器。
- `app.patch()`：用于注册仅接受 *PATCH* 请求的路由的装饰器。
- `app.delete()`：用于注册仅接受 *DELETE* 请求的路由的装饰器。
- `app.route()`：用于注册路由的装饰器。它接受一个 `methods` 参数来指定可接受的请求方法，
默认为 *GET*。也可以在基于 `MethodView` 的视图类中使用。
- `$ flask spec`：用于输出 OpenAPI 规范到标准输出或文件的命令。

你可以在 [API 参考](/api/app) 中学习这些 API，或者你可以继续阅读下一章节
