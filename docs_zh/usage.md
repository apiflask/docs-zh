# 基本用法

本章将介绍APIFlask的主要用法。


## 前提条件

- Python 3.7+
- Flask 1.1+

您还需要了解 Flask 的基本知识。以下是一些有用的免费资源用于学习 Flask :

- [ Flask 官方文档](https://flask.palletsprojects.com/){target=_blank}
- [ Flask 官方教程](https://flask.palletsprojects.com/tutorial/#tutorial){target=_blank}
- [ Flask 大型教程项目](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world){target=_blank}
- [Flask 初学者教程](https://github.com/greyli/flask-tutorial){target=_blank} (Chinese)


## 安装

=== "Linux/macOS"

    ```
    $ pip3 install apiflask
    ```

=== "Windows"

    ```
    > pip install apiflask
    ```

!!! 提示 "Python 依赖管理工具"

    以上命令使用 [pip][_pip]{target=_blank} 安装 APIFlask, 你也可以使用其他依赖管理工具，例如[Poetry][_poetry]{target=_blank}, [Pipenv][_pipenv]{target=_blank}, [PDM][_pdm]{target=_blank}, 等等等.

    [_pip]: https://pip.pypa.io/
    [_poetry]: https://python-poetry.org/
    [_pipenv]: https://pipenv.pypa.io/
    [_pdm]: https://pdm.fming.dev/


## 使用`APIFlask` 类创建一个 `app` 实例 

与你创建一个 Flask `app` 实例类似, 你需要从 `apiflask` 包导入 `APIFlask` 类, 然后从`APIFlask` 类创建 `app` 实例:

```python hl_lines="1 3"
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
def index():
    return {'message': 'hello'}
```

API 的默认标题和版本是 `APIFlask` 和 `0.1.0`; 你可以通过 `title` 和 `version` 变量这些设置:

```python
app = APIFlask(__name__, title='Wonderful API', version='1.0')
```

要运行这个应用, 你可以把它保存为 `app.py`, 然后运行 `flask run` 命令:

```bash
$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

如果你的脚本文件名称不是 `app.py`, 您需要在执行`flask run`之前声明应该启动哪个应用程序. 请参阅注释获取更多细节.

??? 注意 "分配特定应用程序以使用 `FLASK_APP` 运行"

    默认情况下，Flask 将在名为 `app` 或 `wsgi` 的模块/包中查找名为 `app` 或 `application` 的应用程序实例或名为 `create_app` 或 `make_app` 的应用程序工厂函数。 
    这就是为什么我建议将文件命名为 `app.py`。
    如果你想使用不同的名称，则需要通过环境变量 `FLASK_APP` 告诉 Flask 应用程序模块路径。
    例如，如果您的应用程序实例存储在名为 `hello.py` 的文件中，则需要将 `FLASK_APP` 设置为模块名称 `hello`：

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

    同样，如果你的应用程序实例或应用程序工厂函数存储在 `mypkg/__init__.py` 中，
你可以将 `FLASK_APP` 设置为包名：

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

    但是，如果应用程序实例或应用程序工厂函数存储在 `mypkg/myapp.py` 中，
则需要将 `FLASK_APP` 设置为：

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

    查看 *[Application Discovery][_app_discovery]{target=_blank}* 获取更多细节.

    [_app_discovery]: https://flask.palletsprojects.com/cli/#application-discovery

如果你想让应用程序在代码更改时重新启动，你可以使用 `--reload` 选项启用重新加载器:

```bash
$ flask run --reload
```

!!! 提示

    安装 `watchdog` 以获得更好的应用程序重新加载性能：

    === "Linux/macOS"

        ```bash
        $ pip3 install watchdog
        ```

    === "Windows"

        ```
        > pip install watchdog
        ```

我们强烈建议在开发 Flask 应用程序时启用“调试模式”。 有关详细信息，请参阅下面的注释。

??? 注意 "使用 `FLASK_ENV` 启用调试模式"

    Flask 可以在代码更改时自动重启和重新加载应用程序，并显示有用的错误调试信息。如果要在你的 Flask 应用程序中启用这些功能，我们需要将环境变量 `FLASK_ENV` 设置为 `development`:

    === "Bash"

        ```bash
        $ export FLASK_ENV=development
        ```

    === "Windows CMD"

        ```
        > set FLASK_ENV=development
        ```

    === "Powershell"

        ```
        > $env:FLASK_APP="development"
        ```

    查看 *[Debug Mode][_debug_mode]{target=_blank}* 获取更多细节.

    [_debug_mode]: https://flask.palletsprojects.com/quickstart/#debug-mode


## 使用 python-dotenv 管理环境变量

手动设置环境有点不方便，因为变量只存在于当前终端会话中。 每次重新打开终端或重新启动计算机时都必须设置它。 这就是为什么我们需要使用python-dotenv，Flask也对它有特殊的支持。

使用 pip 安装 `python-dotenv`:

=== "Linux/macOS"

    ```bash
    $ pip3 install python-dotenv
    ```

=== "Windows"

    ```
    > pip install python-dotenv
    ```

现在我们可以将环境变量存储在 .env 文件中。 Flask 相关的环境变量应该保存在一个名为 `.flaskenv` 的文件中:

```ini
# 保存为 .flaskenv
FLASK_APP=hello
FLASK_ENV=development
```

虽然加密值应保存在 `.env` 文件中:

```ini
# 保存为 .env
SECRET_KEY=some-random-string
DATABASE_URL=your-database-url
FOO_APP_KEY=some-app-key
```

!!! 警告

    由于 `.env` 包含敏感信息，请不要将其提交到 Git 历史记录中。 确保通过将文件名添加到 .gitignore 来忽略它。

在应用程序中，现在我们可以通过 `os.getenv(key, default_value)`:

```python hl_lines="1 5"
import os

from apiflask import APIFlask

app = APIFlask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
```

任何 `flask` 命令都会读取 `.flaskenv` 和 `.env` 设置的环境变量。
现在当你运行 `flask run` 时，Flask 将读取 `.flaskenv` 文件中的 `FLASK_APP` 和 `FLASK_ENV` 的值，以从给定的导入路径中找到应用程序实例并启用调试模式：

```bash
$ flask run
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 101-750-099
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

查看 *[Environment Variables From dotenv][_dotenv]{target=_blank}* 获取更多细节.

[_dotenv]: https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv


## 交互式 API 文档

创建应用程序实例后，交互式 API 文档将在 <http://localhost:5000/docs> 和 <http://localhost:5000/redoc> 中提供。 最重要的是，OpenAPI 规范文件位于 <http://localhost:5000/openapi.json>。

如果要预览规范或将规范保存到本地文件，请使用 [`flask spec` 命令](/openapi/#the-flask-spec-command)。

你可以在以下部分中添加新路由或添加视图函数的输入和输出定义时刷新文档。


## 使用路由装饰器创建路由

要创建视图函数，你可以完全按照 Flask 所做的那样做：

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

但是，使用 APIFlask，你还可以使用以下快捷方式装饰器，而不是为每个路由设置 `methods` 参数：

- `app.get()`: 注册一个只接受 *GET* 请求的路由.
- `app.post()`: 注册一个只接受 *POST* 请求的路由.
- `app.put()`: 注册一个只接受 *PUT* 请求的路由.
- `app.patch()`: 注册一个只接受 *PATCH* 请求的路由.
- `app.delete()`: 注册一个只接受 *DELETE* 请求的路由.

这是与快捷路由相同的示例:

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

!!! 注意 "在一个视图函数中处理多个 HTTP 方法"

    您不能将 `methods` 参数传递给路由快捷方式。 
    如果希望视图函数接受多个 HTTP 方法，则需要使用 `app.route()` 装饰器来传递 methods` 参数:

    ```python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return {'message': 'hello'}
    ```

    Or you can do something like this:

    ```python
    @app.get('/')
    @app.post('/')
    def index():
        return {'message': 'hello'}
    ```

    顺便说一句，你可以在应用程序中将 `app.route()` 与快捷方式混合使用。


## 迁移到新的 API 装饰器

从 APIFlask 0.12 开始，四个独立的 API 装饰器（即 `@input`、`@output`、`@doc` 和 `@auth_required`）被移至 `APIFlask` 和 `APIBlueprint` 类。 
现在使用您的应用程序或蓝图实例访问它们:

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.get('/')
@app.input(FooSchema)
@app.output(BarSchema)
def hello():
    return {'message': 'Hello'}
```

替代为:

```python
from apiflask import APIFlask, input, output

app = APIFlask(__name__)

@app.get('/')
@input(FooSchema)
@output(BarSchema)
def hello():
    return {'message': 'Hello'}
```

旧的独立装饰器自 0.12 起已弃用，并将在 1.0 版本中删除。 
请注意文档中的所有用法都已更新，您可能需要 [升级 APIFlask](/changelog/) 来更新用法。


## 使用 `@app.input` 验证和反序列化请求数据

要验证和反序列化请求正文或请求查询参数，我们需要首先创建一个数据模式类。 
将其视为描述有效传入数据的一种方式。 
如果你已经熟悉 marshmallow，那么你已经知道如何编写数据模式。

下面是 Pet 输入资源的简单输入模式:

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! 提示

    有关如何编写模式的详细信息以及所有字段和验证器的示例，请参阅模式和字段章节 (WIP)。

schema 类应该继承 `apiflask.Schema` 类:

```python hl_lines="1 6"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

字段用`apiflask.fields`中的字段类表示:

```python hl_lines="2 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

要使用特定规则验证字段，你可以将验证器或验证器列表（从 `apiflask.validators` 导入）传递给字段类的 `validate` 参数:

```python hl_lines="3 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! 提示

    请注意，我们使用 `required` 参数将该字段标记为必填字段。 
    如果要在输入数据中缺少输入字段时为输入字段设置默认值，可以使用 `load_default` 参数:

    ```python
    name = String(load_default='default name')
    ```

使用此模式，我们声明输入请求正文应以以下格式显示:

```json
{
    "name": "the name of the pet",
    "category": "the category of the pet: one of dog and cat"
}
```
!!! 注意

    阅读 *[Data Schema](/schema)* 章节，了解有关数据模式的高级主题。

现在让我们将它添加到用于创建 pet 的视图函数中:

```python hl_lines="1 14"
from apiflask import APIFlask, Schema, input
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


@app.post('/pets')
@app.input(PetInSchema)
def create_pet(data):
    print(data)
    return {'message': 'created'}, 201
```

您只需要将模式类传递给 `@app.input` 装饰器。 
收到请求后，APIFlask 将根据架构验证请求正文。

如果验证通过，数据将作为 `dict` 形式的位置参数注入到视图函数中。 
否则，将返回带有验证结果详细信息的错误响应。

在上面的示例中，我使用名称 `data` 来接受输入数据字典。
你可以将参数名称更改为你喜欢的任何名称。 
由于这是一个字典，你可以这样做来创建一个 ORM 模型实例：

```python hl_lines="5"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema)
def create_pet(pet_id, data):
    pet = Pet(**data)
    return pet
```

或像这样更新 ORM 模型类实例:

```python hl_lines="6 7"
@app.patch('/pets/<int:pet_id>')
@app.input(PetInSchema)
@app.output(PetOutSchema)
def update_pet(pet_id, data):
    pet = Pet.query.get(pet_id)
    for attr, value in data.items():
        setattr(pet, attr, value)
    return pet
```

如果你想用不同的位置标记输入，你可以为 `@app.input()` 装饰器传递一个 `location` 参数，值可以是：

- Request JSON body: `'json'` (default)
- Upload files: `'files'`
- Form data: `'form'`
- Form data and files: `'form_and_files'`
- Cookies: `'cookies'`
- HTTP headers: `'headers'`
- Query string: `'query'` (same as `'querystring'`)

!!! 警告

    确保将 `@app.input` 装饰器放在路由装饰器下（即 `app.route`、`app.get`、`app.post` 等）。


阅读 *[Request Handling](/request)* 章节有关请求处理的高级主题。


## 使用 `@app.output` 格式化响应数据

同样，我们可以使用 `@app.output` 装饰器定义输出数据的模式。 
这是一个例子：

```python
from apiflask.fields import String, Integer


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()
```

由于 APIFlask 不会验证输出数据，我们只需要列出输出模式的所有字段。

!!! 提示

    你可以使用 `dump_default` 参数为输出字段设置默认值：

    ```python
    name = String(dump_default='default name')
    ```

现在将它添加到用于获取宠物资源的视图函数中：

```python hl_lines="1 14"
from apiflask import APIFlask, output
from apiflask.fields import String, Integer

app = APIFlask(__name__)


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    return {
        'name': 'Coco',
        'category': 'dog'
    }
```

输出响应的默认状态码是 `200`，你可以使用 `status_code` 参数设置不同的状态码：

```python hl_lines="3"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, status_code=201)
def create_pet(data):
    data['id'] = 2
    return data
```

Or just:

```python
@app.output(PetOutSchema, 201)
```

如果要返回 204 响应，可以使用 `apiflask.schemas` 中的 `EmptySchema`：

```python hl_lines="1 5"
from apiflask.schemas import EmptySchema


@app.delete('/pets/<int:pet_id>')
@app.output(EmptySchema, 204)
def delete_pet(pet_id):
    return ''
```

从 0.4.0 版本开始，您可以使用空 dict 来表示空模式：警告“`@app.output` 装饰器只能使用一次”

```python hl_lines="2"
@app.delete('/pets/<int:pet_id>')
@app.output({}, 204)
def delete_pet(pet_id):
    return ''
```

!!! 警告 “`@app.output` 装饰器只能使用一次”

    您只能为视图函数定义一个主要成功响应，这意味着您只能使用一个 `@app.output` 装饰器。 
    如果您想在 OpenAPI 规范中为视图添加更多替代响应，可以使用 `@app.doc` 装饰器并将列表传递给 `responses` 参数。
    例如：

    ```python hl_lines="4"
    @app.put('/pets/<int:pet_id>')
    @app.input(PetInSchema)
    @app.output(PetOutSchema)  # 200
    @app.doc(responses=[204, 404])
    def update_pet(pet_id, data):
        pass
    ```

!!! 警告

    确保将 `@app.output` 装饰器放在路由装饰器下方（即 `app.route`、`app.get`、`app.post` 等）。


阅读 *[Response Formatting](/response)* 章节有关请求格式的高级主题。


## 视图函数的返回值

当你使用 `@app.output(schema)` 装饰器时，你应该返回一个匹配你传递的模式的字典或对象。 
例如，这是你的架构：

```python
from apiflask import Schema
from apiflask.fields import String, Integer


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()
```

Now you can return a dict:

```python
@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    return {
        'id': 1,
        'name': 'Coco',
        'category': 'dog'
    }
```

或者你可以直接返回一个 ORM 模型实例：

```python hl_lines="5"
@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    return pet
```

请注意，你的 ORM 模型类应该具有在模式类中定义的字段：

```python
class Pet(Model):
    id = Integer()
    name = String()
    category = String()
```

!!! 提示 “如果我想使用不同的外部字段名称怎么办？”

    例如，在你的 ORM 模型类中，你有一个 `phone` 字段来存储用户的电话号码：

    ```python
    class User(Model):
        phone = String()
    ```

    现在你要输出名称为 `phone_number` 的字段，然后可以使用 `data_key` 声明要转储到的实际密钥名称：

    ```python
    class UserOutSchema(Schema):
        phone = String(data_key='phone_number')
    ```

    此模式将生成类似 `{'phone_number': ...}`.

    同样，您可以告诉 APIFlask 从输入模式中的不同 key 加载：

    ```python
    class UserInSchema(Schema):
        phone = String(data_key='phone_number')
    ```

    此模式期望用户输入类似于 `{'phone_number': ...}`.

默认状态码是`200`，如果你想使用不同的状态码，你可以在`@app.output`装饰器中传递一个`status_code`参数：

```python hl_lines="3"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, 201)
def create_pet(data):
    # ...
    return pet
```

你不需要在视图函数的末尾返回相同的状态码（即，`return data, 201`）：

```python hl_lines="8"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, 201)
def create_pet(data):
    # ...
    # equals to:
    # return pet, 201
    return pet
```

当你想传递一个头部字典时，你可以将字典作为返回元组的第二个元素传递：

```python hl_lines="8"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, 201)
def create_pet(data):
    # ...
    # equals to:
    # return pet, 201, {'FOO': 'bar'}
    return pet, {'FOO': 'bar'}
```

!!! 提示

    当您想使用非 200 状态代码时，请务必始终在 `@app.output` 中设置 `status_code` 参数。 
    如果不匹配，在 `@app.output` 中传递的 `status_code` 将在 OpenAPI 规范中使用，而实际响应将使用您在视图函数末尾返回的状态码。


## OpenAPI 生成支持和 `@app.doc` 装饰器

APIFlask 提供自动生成 OpenAPI 规范的支持，同时还允许您自定义规范：

- `info` 对象的大部分字段和 `OpenAPI` 对象的顶级字段都可以通过配置变量访问。
- `tag` 对象、Operation `summary` 和 `description` 将从蓝图名称、视图函数名称和文档字符串中生成。
- 你可以注册一个规范处理器函数来处理规范。
- `requestBody` 和 `responses` 字段可以使用 `input` 和 `output` 装饰器设置。
- 其他操作字段可以使用 `doc` 装饰器设置：

```python hl_lines="1 7"
from apiflask import APIFlask, doc

app = APIFlask(__name__)


@app.get('/hello')
@app.doc(summary='Say hello', description='Some description for the /hello')
def hello():
    return 'Hello'
```

查看 *[使用`doc` 装饰器](/openapi/#use-the-doc-decorator)* 了解有关 OpenAPI 生成和使用 `doc` 装饰器的更多详细信息。

!!! 警告

    确保将 `@app.doc` 装饰器放在路由装饰器下（即 `app.route`、`app.get`、`app.post` 等）。


## 使用 `@app.auth_required` 保护您的视图

APIFlask 基于 [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth), 提供三种认证方式：

### HTTP 基础

要实现 HTTP 基本身份验证，你需要：

- 使用 `HTTPBasicAuth` 创建一个 `auth` 对象。
- 用`@auth.verify_password`注册一个回调函数，该函数应该接受`username`和`password`，返回相应的用户对象或`None`。
- 使用 `@app.auth_required(auth)` 保护视图函数。
- 使用 `auth.current_user` 访问视图函数中的当前用户对象。

```python
from apiflask import APIFlask, HTTPBasicAuth

app = APIFlask(__name__)
auth = HTTPBasicAuth()  # create the auth object


@auth.verify_password
def verify_password(username, password):
    # get the user from the database, check the password
    # then return the user if the password matches
    # ...

@app.route('/')
@app.auth_required(auth)
def hello():
    return f'Hello, {auth.current_user}!'
```

### HTTP Bearer

要实现 HTTP Bearer 身份验证，你需要：

- 使用 `HTTPTokenAuth` 创建一个 `auth` 对象
- 使用`@auth.verify_password`注册一个回调函数，该函数应该接受`token`，返回相应的用户对象或`None`。
- 使用 `@app.auth_required(auth)` 保护视图函数。
- 使用 `auth.current_user` 访问视图函数中的当前用户对象。

```python
from apiflask import APIFlask, HTTPTokenAuth

app = APIFlask(__name__)
auth = HTTPTokenAuth()  # create the auth object
# or HTTPTokenAuth(scheme='Bearer')


@auth.verify_token  # register a callback to verify the token
def verify_token(token):
    # verify the token and get the user id
    # then query and return the corresponding user from the database
    # ...

@app.get('/')
@app.auth_required(auth)  # protect the view
def hello():
    # access the current user with auth.current_user
    return f'Hello, {auth.current_user}'!
```

### API 密钥（在头部中）

类似于 Bearer 类型，但在创建 auth 对象时将 `scheme` 设置为 `ApiKey`：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey')
```

或使用自定义头部：

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey', header='X-API-Key')

# ...
```

你可以使用 `HTTPBasicAuth` 和 `HTTPTokenAuth` 中的 `description` 参数设置 OpenAPI 安全描述。

请参阅 [Flask-HTTPAuth 的文档][_flask-httpauth]{target=_blank} 了解详细信息。 
但是，请记住从 APIFlask 导入 `HTTPBasicAuth` 和 `HTTPTokenAuth` 并使用 `@app.auth_required` 而不是 `@auth.login_required` 作为视图函数。

!!! 警告

    确保将 `@app.auth_required` 装饰器放在路由装饰器下（即 `app.route`、`app.get`、`app.post` 等）。

[_flask-httpauth]: https://flask-httpauth.readthedocs.io/

阅读 *[Authentication](/authentication)* ，了解有关身份验证的高级主题。


## 使用基于类的视图

!!! 警告 "Version >= 0.5.0"

    此功能已添加到 [version 0.5.0](/changelog/#version-050).

你可以使用 `MethodView` 类在相同的 URL 规则下创建一组路由。 这是一个简单的例子：

```python
from flask.views import MethodView
from apiflask import APIFlask

app = APIFlask(__name__)


@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):

    def get(self, pet_id):
        return {'message': 'OK'}

    def delete(self, pet_id):
        return '', 204
```

创建视图类时，需要从`MethodView`类继承，因为 APIFlask 只能为基于 `MethodView` 的视图类生成 OpenAPI 规范:

```python
from flask.views import MethodView

@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):
    # ...
```

APIFlask 支持在视图类上使用 `route` 装饰器作为 `add_url_rule` 的快捷方式：

```python
@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):
    # ...
```

!!! 提示

    如果未提供 `endpoint` 参数，则类名将用作端点。 
    你不需要传递 `methods` 参数，因为 Flask 会为你处理它。
    
现在，您可以为每个 HTTP 方法定义视图方法，使用 (HTTP) 方法名称作为方法名称：

```python
@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):

    def get(self, pet_id):  # triggered by GET request
        return {'message': 'OK'}

    def post(self, pet_id):  # triggered by POST request
        return {'message': 'OK'}

    def put(self, pet_id):  # triggered by PUT request
        return {'message': 'OK'}

    def delete(self, pet_id):  # triggered by DELETE request
        return '', 204

    def patch(self, pet_id):  # triggered by PATCH request
        return {'message': 'OK'}
```

对于上面的示例应用程序，当用户向 `/pets/<int:pet_id>` 发送 *GET* 请求时，将调用 `Pet` 类的 `get()` 方法，以此类推。

从 [version 0.10.0](/changelog/#version-0100)开始，您还可以使用 `add_url_rule` 方法注册视图类：

```python
class Pet(MethodView):
    # ...

app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

你仍然不需要设置`methods`，但是如果你想根据方法为一个视图类注册多个规则，你将需要，这只能通过 `add_url_rule` 来实现。
例如，您在上面创建的 `post` 方法通常具有与其他方法不同的 URL 规则：

```python
class Pet(MethodView):
    # ...

pet_view = Pet.as_view('pet')
app.add_url_rule('/pets/<int:pet_id>', view_func=pet_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])
app.add_url_rule('/pets', view_func=pet_view, methods=['POST'])
```

当你使用像`@app.input`，`@app.output`这样的装饰器时，一定要在方法而不是类上使用它：

```python hl_lines="4 5 9 10 11 15 16"
@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):

    @app.output(PetOutSchema)
    @app.doc(summary='Get a Pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetInSchema)
    @app.output(PetOutSchema)
    def put(self, pet_id, data):
        # ...

    @app.input(PetInSchema(partial=True))
    @app.output(PetOutSchema)
    def patch(self, pet_id, data):
        # ...
```

如果你想为所有方法应用一个装饰器，而不是重复自己，你可以将装饰器传递给类属性`decorators`，它接受一个装饰器列表：

```python hl_lines="4"
@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):

    decorators = [auth_required(auth), doc(responses=[404])]

    @app.output(PetOutSchema)
    @app.doc(summary='Get a Pet')
    def get(self, pet_id):
        # ...

    @app.auth_required(auth)
    @app.input(PetInSchema)
    @app.output(PetOutSchema)
    def put(self, pet_id, data):
        # ...

    @app.input(PetInSchema(partial=True))
    @app.output(PetOutSchema)
    def patch(self, pet_id, data):
        # ...
```


## 使用 `abort()` 返回错误响应

类似于 Flask 的 `abort`，但是来自 APIFlask 的 `abort` 会返回一个 JSON 响应。

例子:

```python hl_lines="1 8"
from apiflask import APIFlask, abort

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        abort(404, 'This man is missing.')
    return {'hello': name}
```

!!! 提示

    当 `app.json_errors` 为 `True`（默认）时，Flask 的 `abort` 也会返回 JSON 错误响应。

你还可以引发 `HTTPError` 异常以返回错误响应：

```python hl_lines="1 8"
from apiflask import APIFlask, HTTPError

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        raise HTTPError(404, 'This man is missing.')
    return {'hello': name}
```

`abort()` 和 `HTTPError` 接受以下参数：

- `status_code`: 错误的状态代码（4XX 和 5xx）。
- `message`: 错误的简单描述。 如果没有提供，将使用状态码的原因短语。
- `detail`: 错误的详细信息，可用于提供自定义错误代码、文档 URL 等附加信息。
- `headers`: 错误响应中使用的标头字典。

!!! 警告

    在 [version 0.4.0](/changelog/#version-040) 中，函数 `abort_json()` 被重命名为 `abort()`。


## `apiflask` 包概述

最后，让我们打开整个 `apiflask` 包，看看它附带了什么：

- `APIFlask`: 用于创建应用程序实例的类（Flask 的 `Flask` 类的包装器）。
- `APIBlueprint`: 用于创建蓝图实例的类（Flask 的 `Blueprint` 类的包装器）。
- `@app.input()`: 用于验证来自请求正文、查询字符串等的输入/请求数据的装饰器。
- `@app.output()`: 用于格式化响应的装饰器。
- `@app.auth_required()`: 用于保护视图免受未经身份验证的用户的装饰。
- `@app.doc()`: 用于设置视图函数的 OpenAPI 规范的装饰器。
- `abort()`: 用于中止请求处理过程并返回错误响应的函数。Flask 的 `flask.abort()` 函数的 JSON 版本。
- `HTTPError`: 用于返回错误响应的异常（由 `abort()` 使用）。
- `HTTPBasicAuth`: 用于创建身份验证实例的类。
- `HTTPTokenAuth`: 用于创建身份验证实例的类。
- `Schema`: 资源模式的基类（将是 marshmallow 的 `Schema` 的包装器）。
- `fields`: 一个模块包含所有字段 (来自 marshmallow).
- `validators`: 一个模块包含所有的字段验证器 (来自 marshmallow).
- `app.get()`: 用于注册只接受 *GET* 请求的路由的装饰器。
- `app.post()`: 用于注册只接受 *POST* 请求的路由的装饰器。
- `app.put()`: 用于注册只接受 *PUT* 请求的路由的装饰器。
- `app.patch()`: 用于注册只接受 *PATCH* 请求的路由的装饰器。
- `app.delete()`: 用于注册只接受 *DELETE* 请求的路由的装饰器。
- `app.route()`: 用于注册路由的装饰器。 它接受一个`methods`参数来指定一个接受的方法列表，默认为*GET*。 它也可以用于基于 `MethodView` 的视图类。
- `$ flask run`: 将规范输出到标准输出或文件的命令。

你可以在 [API reference](/api/app) 中了解这些API的详细信息，也可以继续阅读以下章节。
