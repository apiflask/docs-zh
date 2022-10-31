# 基础用法

本章节涵盖了 APIFlask 的基本用法

## 前置准备

- Python 3.7+
- Flask 1.1+

在此之前，你需要了解一下 Flask 的基础知识。下面是一些高质量且免费的 Flask 学习资源：


- [Flask's Documentation](https://flask.palletsprojects.com/){target=_blank}
- [Official Flask Tutorial](https://flask.palletsprojects.com/tutorial/#tutorial){target=_blank}
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world){target=_blank}
- [Flask for Beginners](https://github.com/greyli/flask-tutorial){target=_blank} (Chinese)


## 安装 APIFlask

=== "Linux/macOS"

    ```
    $ pip3 install apiflask
    ```

=== "Windows"

    ```
    > pip install apiflask
    ```


!!! tip "Python的包(依赖)管理工具"
    在终端（命令行）中使用 [pip][_pip]{target=_blank} 来安装 APIFlask，你也可以使用其他的依赖管理工具。比如：[Poetry][_poetry]{target=_blank}、
    [Pipenv][_pipenv]{target=_blank}、[PDM][_pdm]{target=_blank} 等等。

    [_pip]: https://pip.pypa.io/
    [_poetry]: https://python-poetry.org/
    [_pipenv]: https://pipenv.pypa.io/
    [_pdm]: https://pdm.fming.dev/


## 使用 `APIFlask` 创建一个 `app` 实例

与创建 Flask 的 `app` 实例操作类似，您需要导入 `apiflask` 包中的 `APIFlask` 类，然后使用
`APIFlask` 来实例化 `app`：

```python hl_lines="1 3"
from apiflask import APIFlask

app = APIFlask(__name__)


@app.get('/')
def index():
    return {'message': 'hello'}
```

API 项目的默认标题和版本是 `APIFlask` 和 `0.1.0`；你可以通过修改 `title` 和 `version` 参数来改变相应的内容。


**译者注：这里的意思是指可以通过 title 和 version 两个参数来配置项目名与管理迭代版本，同时这两个参数也会影响到交互式 API 文档页面的内容**

```python
app = APIFlask(__name__, title='Wonderful API', version='1.0')
```

想要运行这个应用程序，你需要先将其保存为 `app.py` 文件，然后运行 `flask run` 命令：

```bash
$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

如果你脚本的文件名不是 `app.py`，那么你需要在使用 `flask run` 命令启动应用程式前先向声明它。更多详情请见下面的说明。

??? note "Assign the specific application to run with `FLASK_APP`"

    默认情况下，Flask 将在名为 `app` 或 `wsgi` 的模块/包中寻找一个名为 `app` 或 `application` 的应用
    程序实例或者是名为 `create_app` 或 `make_app` 的工厂函数。这就是为什么我建议将文件命名为 `app.py`。
    如果使用不同的名称，则需要通过环境变量 `FLASK_APP` 告诉 Flask 应用程序模块路径。例如：如果你的程序实例
    存储在名为 `hello.py` 的文件中，则需要将 `FLASK_APP` 设置为模块的名称 `hello`：

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

    同样，如果你的程序实例或工厂函数存储在 `mypkg/__init__.py` 中，则可以将 `FLASK_APP` 设置为包名：

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

    但是，如果程序实例或工厂函数存储在 `mypkg/myapp.py` 中，则需要将 ·FLASK_APP` 设置为：

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

    See *[Application Discovery][_app_discovery]{target=_blank}* for more details.

    [_app_discovery]: https://flask.palletsprojects.com/cli/#application-discovery


如果你想在修改代码时应用也随之重新启动，可以添加 `--reload` 选项开启 reloader：

```bash
$ flask run --reload
```

!!! tip

    Install `watchdog` for a better performance for the application reloader:

    === "Linux/macOS"

        ```bash
        $ pip3 install watchdog
        ```

    === "Windows"

        ```
        > pip install watchdog
        ```


我们强烈建议在开发 Flask 应用的时候开启“调试模式”。更详细信息请看下面：

??? note "Enable the debug mode with `FLASK_ENV`"

    Flask can automatically restart and reload the application when code changes
    and display useful debug information for errors. To enable these features
    in your Flask application, we will need to set the environment variable
    `FLASK_ENV` to `development`:

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

    See *[Debug Mode][_debug_mode]{target=_blank}* for more details.

    [_debug_mode]: https://flask.palletsprojects.com/quickstart/#debug-mode


## Manage environment variables with python-dotenv(使用 python-dotenv 管理环境变量)

Manually setting environment is a bit inconvenient since the variable only lives in
the current terminal session. You have to set it every time you reopen the terminal
or reboot the computer. That's why we need to use python-dotenv, and Flask also
has special support for it.

由于环境变量只会存在于当前终端会话中，因此每次建立一个新的终端会话都需要重新手动设置一遍环境变量，这样太不方便了。所以我们需要用到 python-dotenv 包来帮我们自动加载环境变量，并且 Flask 也对它做了优化。

~~变量一般只会存在终端当前会话中，每次打开新终端会话都需要重新设计环境变量，因此手动设置环境变量是很麻烦的一件事情。~~


Install `python-dotenv` with pip:

=== "Linux/macOS"

    ```bash
    $ pip3 install python-dotenv
    ```

=== "Windows"

    ```
    > pip install python-dotenv
    ```

Now we can store environment variables in .env files. Flask-related environment
variables should keep in a file called `.flaskenv`:

现在，我们可以将环境变量写到一个名为 .env 的文件中，Flask 项目相关的环境变量则应该存储在 .flaskenv 中：
（后续翻阅《Flask开发实战》中的对应部分进行微调）

```ini
# save as .flaskenv
FLASK_APP=hello
FLASK_ENV=development
```

While the secrets values should save in the `.env` file:

```ini
# save as .env
SECRET_KEY=some-random-string
DATABASE_URL=your-database-url
FOO_APP_KEY=some-app-key
```

!!! warning

    Since the `.env` contains sensitive information, do not commit it into the
    Git history. Be sure to ignore it by adding the file name into `.gitignore`.

In the application, now we can read these variables via `os.getenv(key, default_value)`:
现在，在应用程序中我们可以使用 `os.getenv(key, default_value)` 来读取这些变量：

```python hl_lines="1 5"
import os

from apiflask import APIFlask

app = APIFlask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
```

Any `flask` command will read environment variables set by `.flaskenv` and `.env`.
Now when you run `flask run`, Flask will read the value of `FLASK_APP` and `FLASK_ENV`
in `.flaskenv` file to find the app instance from given import path and enable the
debug mode:

```bash
$ flask run
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 101-750-099
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

更多信息请浏览 *[Environment Variables From dotenv][_dotenv]{target=_blank}*。

[_dotenv]: https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv


## Interactive API documentation(交互式API文档)

当你创建应用程序后，你将可以在 <http://localhost:5000/docs> 和 <http://localhost:5000/redoc> 浏览交互式API文档。最重要的是，你可以访问 <http://localhost:5000/openapi.json> 获取 OpenAPI 规范文件。


如果你想预览规范文件或者将其保存到本地文件，[可以使用 `flask spec`
命令](/openapi/#the-flask-spec-command)。

当视图函数添加了新的路由或是 input 和 output 装饰器定义时，你可刷新文档页面来看到新增的内容。

## Create a route with route decorators(使用装饰器来创建路由/使用路由装饰器来创建路由)

你可以像 Flask 一样创建视图函数：

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

However, with APIFlask, instead of setting `methods` argument for each route, you can
also use the following shortcuts decorators:

- `app.get()`: register a route that only accepts *GET* request.
- `app.post()`: register a route that only accepts *POST* request.
- `app.put()`: register a route that only accepts *PUT* request.
- `app.patch()`: register a route that only accepts *PATCH* request.
- `app.delete()`: register a route that only accepts *DELETE* request.

Here is the same example with the route shortcuts:

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

!!! note "Handling multiple HTTP methods in one view function"

    You can't pass the `methods` argument to route shortcuts. If you want the
    view function to accept multiple HTTP methods, you will need to use the
    `app.route()` decorator to pass the `methods` argument:

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

    By the way, you can mix the use of `app.route()` with the shortcuts in your
    application.


## Move to new API decorators(转移到新的 API 装饰器/使用新的 API 装饰器)

从 APIFlask 0.12 版本开始，四个单独的 API 装饰器（`@input`，`@output`，`@doc`，和 `@auth_required`）被迁移到 `APIFlask` 和 `APIBlueprint` 中。你现在可以通过应用实例或蓝图实例来使用它们：

```python
from apiflask import APIFlask

app = APIFlask(__name__)

@app.get('/')
@app.input(FooSchema)
@app.output(BarSchema)
def hello():
    return {'message': 'Hello'}
```

上面的例子将代替下面的例子:

```python
from apiflask import APIFlask, input, output

app = APIFlask(__name__)

@app.get('/')
@input(FooSchema)
@output(BarSchema)
def hello():
    return {'message': 'Hello'}
```

旧的独立装饰器将在 0.12 版本弃用，并将在 1.0 版本被移除。请注意，文档中的所有用法都已更新，如有需要请阅读 [upgrade APIFlask](/changelog/) 以更新使用情况。

## Use `@app.input` to validate and deserialize request data(使用 `@app.input` 来校验与反序列化请求数据)

To validate and deserialize a request body or request query parameters, we need to
create a data schema class first. Think of it as a way to describe the valid
incoming data. If you already familiar with marshmallow, then you already know
how to write a data schema.

如果需要校验和反序列化请求体或请求查询参数，我们需要先创建一个 data schema 类。这个 schema 类将被视为传入数据的一种描述方式。如果你已经熟悉 marshmallow 这个库，那么相信你已经知道如何编写 data schema。

这是一个简单的 input schema 示例，用于接收 Pet 类传入的数据：

```python
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! tip

    See Schema and Fields chapter (WIP) for the details of how to write a schema and
    the examples for all the fields and validators.

schema 类应该继承自 `apiflask.Schema` 类：

```python hl_lines="1 6"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```


字段需要引用自 `apiflask.fields` 的字段类：


```python hl_lines="2 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

如果需要使用自定义的规则来验证字段，你可以通过 `validate` 参数来传递验证器或验证器列表（从 `apiflask.validators` 中导入）：

```python hl_lines="3 7 8"
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))
```

!!! tip

    Notice we mark the field as a required field with the `required` parameter.
    If you want to set a default value for an input field when is missing in
    the input data, you can use the `load_default` parameter:

    ```python
    name = String(load_default='default name')
    ```

通过使用这个 schema，我们规定了输入的请求体需要满足下面的格式：

```json
{
    "name": "the name of the pet",
    "category": "the category of the pet: one of dog and cat"
}
```
!!! notes

    Read the *[Data Schema](/schema)* chapter for the advanced topics on data schema.


现在让我们把它添加到一个用于创建新 pet 的视图函数中：


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


你只需要将 schema 类传递给 `@app.input` 装饰器即可。当接收到请求的时候，APIFlask会自动的根据 schema 类校验请求体。

如果验证通过，请求体的数据将会以 `dict` 的形式输出到视图函数的参数中。否则就把验证结果的详细信息以错误响应的形式返回出去。

在这个示例中，我使用了一个名为 `data` 的参数来接收输入的数据字典。你可以将参数名称更改为你喜欢的任何名称。同时因为这是一个字典，你可以像下面示例中一样创建一个 ORM 实例：

```python hl_lines="5"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema)
def create_pet(pet_id, data):
    pet = Pet(**data)
    return pet
```

或者像这样更新一个 ORM 模型实例：

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

如果你想获取不同请求位置的输入请求数据，你可通过改变 `@app.input()` 装饰器的 `location` 参数来从下面的这些地方获取请求数据：

- Request JSON body: `'json'` (default)
- Upload files: `'files'`
- Form data: `'form'`
- Form data and files: `'form_and_files'`
- Cookies: `'cookies'`
- HTTP headers: `'headers'`
- Query string: `'query'` (same as `'querystring'`)

!!! warning

    Be sure to put the `@app.input` decorator under the routes decorators
    (i.e., `app.route`, `app.get`, `app.post`, etc.).


阅读 *[请求处理](/request)* 章节，了解更多有关请求处理的进阶用法。

## Use `@app.output` to format response data(使用 `@app.output` 来格式化响应数据)

同样的，我们可以使用 `@app.output` 装饰器配合定义好的 schema 来对响应的数据进行格式化，下面是一个简易的示例：

```python
from apiflask.fields import String, Integer


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()
```

由于 APIFlask 不会对响应的数据内容进行校验，因此我们只需要列出响应体的结构即可。


!!! tip

    You can set a default value for output field with the `dump_default` argument:

    ```python
    name = String(dump_default='default name')
    ```

Now add it to the view function which used to get a pet resource:

~~现在让我们将它添加到视图函数中，并利用它来获取 Pet 资源：~~

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

默认的状态码是 `200`，你可以通过 `status_code` 参数来设置不同的默认值：

```python hl_lines="3"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, status_code=201)
def create_pet(data):
    data['id'] = 2
    return data
```

或者像下面这样：

```python
@app.output(PetOutSchema, 201)
```

如果你想返回一个204响应，你可以使用 `apiflask.schemas` 中的 `EmptySchema`：

```python hl_lines="1 5"
from apiflask.schemas import EmptySchema


@app.delete('/pets/<int:pet_id>')
@app.output(EmptySchema, 204)
def delete_pet(pet_id):
    return ''
```

从 0.4.0 版本开始，你可以在 input 中使用空字典来表示返回**空的响应体**：


```python hl_lines="2"
@app.delete('/pets/<int:pet_id>')
@app.output({}, 204)
def delete_pet(pet_id):
    return ''
```

!!! warning "The `@app.output` decorator can only use once"

    You can only define one main success response for your view function,
    which means you can only use one `@app.output` decorator. If you want to
    add more alternative responses for a view in the OpenAPI spec, you can
    use the `@app.doc` decorator and pass a list to the `responses` parameter.
    For example:

    ```python hl_lines="4"
    @app.put('/pets/<int:pet_id>')
    @app.input(PetInSchema)
    @app.output(PetOutSchema)  # 200
    @app.doc(responses=[204, 404])
    def update_pet(pet_id, data):
        pass
    ```

!!! warning

    Be sure to put the `@app.output` decorator under the routes decorators
    (i.e., `app.route`, `app.get`, `app.post`, etc.).


阅读 *[响应格式化](/response)* 一章，了解关于请求格式化的高级主题。

## The return value of the view function(视图函数返回的内容)

当你使用 `@app.output(schema)` 装饰器的时候，你应该返回一个与你定义的 schema 匹配的字典或对象。
举个例子，加入你的 schema 类是这样：

```python
from apiflask import Schema
from apiflask.fields import String, Integer


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()
```

现在要返回一个字典：

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

或者返回一个 ORM 模型实例：

```python hl_lines="5"
@app.get('/pets/<int:pet_id>')
@app.output(PetOutSchema)
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    return pet
```

注意！你的 ORM 模型类应该有 schema 类中定义的字段。


```python
class Pet(Model):
    id = Integer()
    name = String()
    category = String()
```

!!! tip "What if I want to use a different external field name?"

    For example, in your ORM model class, you have a `phone` field that
    store the user's phone number:

    ```python
    class User(Model):
        phone = String()
    ```

    Now you want to output the field with the name `phone_number`, then you can use
    `data_key` to declare the actual key name to dump to:

    ```python
    class UserOutSchema(Schema):
        phone = String(data_key='phone_number')
    ```

    This schema will generate something like `{'phone_number': ...}`.

    Similarly, you can tell APIFlask to load from different key in input schema:

    ```python
    class UserInSchema(Schema):
        phone = String(data_key='phone_number')
    ```

    This schema expects the user input is something like `{'phone_number': ...}`.

The default status code is `200`, if you want to use a different status code,
you can pass a `status_code` argument in the `@app.output` decorator:


默认的状态码是 `200`，如果你想使用


```python hl_lines="3"
@app.post('/pets')
@app.input(PetInSchema)
@app.output(PetOutSchema, 201)
def create_pet(data):
    # ...
    return pet
```

你不需要在视图函数的末尾返回相同的 HTTP 状态码（即：`return data, 201`）：

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

当你想返回一个 HTTP header 字典时，你可以像下面的例子一样将其作为返回元组的第二个元素：

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

!!! tips

    Be sure to always set the `status_code` argument in `@app.output` when you want
    to use a non-200 status code. If there is a mismatch, the `status_code`
    passed in `@app.output` will be used in OpenAPI spec, while the actual response
    will use the status code you returned at the end of the view function.
    当你想使用非 200 的状态码时，请确保在 `@app.output` 中设置了 `status_code` 参数。如果参数中使用了一个非 200 的状态码并且与返回值不匹配时，那么`@app.output`中的 `status_code` 将被用于OpenAPI规范，而实际响应的状态码将是你在视图函数结束时返回的状态码。

## The OpenAPI generating support and the `@app.doc` decorator(OpenAPI 生成与 `@app.doc` 装饰器使用方法)

APIFlask 提供自动生成 OpenAPI 规范的支持，同时也允许你自定义规范。

- Most of the fields of the `info` object and top-level field of `OpenAPI`
objct are accessible with configuration variables.
- `info` 对象的大部分字段和 `OpenAPI` 对象的顶级字段可通过配置变量访问。
- The `tag` object, Operation `summary` and `description` will generated from
the blueprint name, the view function name and docstring.
- `标签对象`、`操作摘要` 和 `描述` 将根据蓝图名称、视图函数名称和文档字符串生成。
- You can register a spec processor function to process the spec.
- `requestBody` and `responses` fields can be set with the `input` and `output`
decorator.
- `requestBody` 和 `responses` 字段可以使用 `input` 和 `output` 装饰器来设置。
- Other operation fields can be set with the `doc` decorator:
- 其他操作字段可以用 `doc` 装饰器来设置。

```python hl_lines="1 7"
from apiflask import APIFlask, doc

app = APIFlask(__name__)


@app.get('/hello')
@app.doc(summary='Say hello', description='Some description for the /hello')
def hello():
    return 'Hello'
```

参见*[使用 `doc` 装饰器](/openapi/#use-the-doc-decorator)* 以了解更多关于 OpenAPI 生成和 `doc` 装饰器的用法。

!!! warning

    Be sure to put the `@app.doc` decorator under the routes decorators
    (i.e., `app.route`, `app.get`, `app.post`, etc.).
    请确保将`@app.doc`装饰器放在路由装饰器的下面（即`app.route`，`app.get`，`app.post`，等等）。


## Use `@app.auth_required` to protect your views(使用 `@app.auth_required` 保护你的接口/为你的接口添加鉴权)

Based on [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth), APIFlask
provides three types of authentication:

### HTTP Basic (HTTP Basic 认证)

To implement an HTTP Basic authentication, you will need to:

- Create an `auth` object with `HTTPBasicAuth`
- Register a callback function with `@auth.verify_password`, the function
  should accept `username` and `password`, return the corresponding user object
  or `None`.
- Protect the view function with `@app.auth_required(auth)`.
- Access the current user object in your view function with `auth.current_user`.

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

### HTTP Bearer(HTTP Bearer 认证)

To implement an HTTP Bearer authentication, you will need to:

- Create an `auth` object with `HTTPTokenAuth`
- Register a callback function with `@auth.verify_password`, the function
  should accept `token`, return the corresponding user object or `None`.
- Protect the view function with `@app.auth_required(auth)`.
- Access the current user object in your view function with `auth.current_user`.

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

### API Keys (in header) (不会翻译)

Similar to the Bearer type, but set the `scheme` to `ApiKey` when creating the
auth object:

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey')
```

or with a custom header:

```python
from apiflask import HTTPTokenAuth

HTTPTokenAuth(scheme='ApiKey', header='X-API-Key')

# ...
```

You can set the OpenAPI security description with the `description` parameter
in `HTTPBasicAuth` and `HTTPTokenAuth`.

See [Flask-HTTPAuth's documentation][_flask-httpauth]{target=_blank} to learn
the details. However, remember to
import `HTTPBasicAuth` and `HTTPTokenAuth` from APIFlask and use `@app.auth_required`
instead of `@auth.login_required` for your view functions.

!!! warning

    Be sure to put the `@app.auth_required` decorator under the routes decorators
    (i.e., `app.route`, `app.get`, `app.post`, etc.).

[_flask-httpauth]: https://flask-httpauth.readthedocs.io/

Read the *[Authentication](/authentication)* chapter for the advanced topics on authentication.


## Use class-based views(使用基于类的视图)

!!! warning "Version >= 0.5.0"

    This feature was added in the [version 0.5.0](/changelog/#version-050).

You can create a group of routes under the same URL rule with the `MethodView` class.
Here is a simple example:

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

When creating a view class, it needs to inherit from the `MethodView` class, since APIFlask
can only generate OpenAPI spec for `MethodView`-based view classes.:

```python
from flask.views import MethodView

@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):
    # ...
```

APIFlask supports to use the `route` decorator on view classes as a shortcut for `add_url_rule`:

```python
@app.route('/pets/<int:pet_id>', endpoint='pet')
class Pet(MethodView):
    # ...
```

!!! tips

    If the `endpoint` argument isn't provided, the class name will be used as
    endpoint. You don't need to pass a `methods` argument, since Flask will handle
    it for you.

Now, you can define view methods for each HTTP method, use the (HTTP) method name as method name:

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

With the example application above, when the user sends a *GET* request to
`/pets/<int:pet_id>`, the `get()` method of the `Pet` class will be called,
and so on for the others.

From [version 0.10.0](/changelog/#version-0100), you can also use the `add_url_rule` method to register
view classes:

```python
class Pet(MethodView):
    # ...

app.add_url_rule('/pets/<int:pet_id>', view_func=Pet.as_view('pet'))
```

You still don't need to set the `methods`, but you will need if you want to register multiple rules
for one view classes based on the methods, this can only be achieved with `add_url_rule`. For
example, the `post` method you created above normally has a different URL rule than the others:

```python
class Pet(MethodView):
    # ...

pet_view = Pet.as_view('pet')
app.add_url_rule('/pets/<int:pet_id>', view_func=pet_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])
app.add_url_rule('/pets', view_func=pet_view, methods=['POST'])
```

When you use decorators like `@app.input`, `@app.output`, be sure to use it on method
instead of class:

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

If you want to apply a decorator for all methods, instead of repeat yourself,
you can pass the decorator to the class attribute `decorators`, it accepts
a list of decorators:

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


## Use `abort()` to return an error response(使用)

Similar to Flask's `abort`, but `abort` from APIFlask will return a JSON response.

Example:

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

    When `app.json_errors` is `True` (default), Flask's `abort` will also return
    JSON error response.

You can also raise an `HTTPError` exception to return an error response:

```python hl_lines="1 8"
from apiflask import APIFlask, HTTPError

app = APIFlask(__name__)

@app.get('/<name>')
def hello(name):
    if name == 'Foo':
        raise HTTPError(404, 'This man is missing.')
    return {'hello': name}
```

The `abort()` and `HTTPError` accept the following arguments:

- `status_code`: The status code of the error (4XX and 5xx).
- `message`: The simple description of the error. If not provided,
    the reason phrase of the status code will be used.
- `detail`: The detailed information of the error, it can be used to
    provide additional information such as custom error code, documentation
    URL, etc.
- `headers`: A dict of headers used in the error response.

!!! warning

    The function `abort_json()` was renamed to `abort()` in
    the [version 0.4.0](/changelog/#version-040).


## Overview of the `apiflask` package(APIFlask总览/概述)

In the end, let's unpack the whole `apiflask` package to check out what it shipped with:

- `APIFlask`: A class used to create an application instance (A wrapper for Flask's `Flask` class).
- `APIBlueprint`: A class used to create a blueprint instance (A wrapper for Flask's `Blueprint` class)..
- `@app.input()`: A decorator used to validate the input/request data from request body, query string, etc.
- `@app.output()`: A decorator used to format the response.
- `@app.auth_required()`: A decorator used to protect a view from unauthenticated users.
- `@app.doc()`: A decorator used to set up the OpenAPI spec for view functions.
- `abort()`: A function used to abort the request handling process and return an error response. The JSON version of Flask's `flask.abort()` function.
- `HTTPError`: An exception used to return error response (used by `abort()`).
- `HTTPBasicAuth`: A class used to create an auth instance.
- `HTTPTokenAuth`: A class used to create an auth instance.
- `Schema`: A base class for resource schemas (Will be a wrapper for marshmallow's `Schema`).
- `fields`: A module contains all the fields (from marshmallow).
- `validators`: A module contains all the field validators (from marshmallow).
- `app.get()`: A decorator used to register a route that only accepts *GET* request.
- `app.post()`: A decorator used to register a route that only accepts *POST* request.
- `app.put()`: A decorator used to register a route that only accepts *PUT* request.
- `app.patch()`: A decorator used to register a route that only accepts *PATCH* request.
- `app.delete()`: A decorator used to register a route that only accepts *DELETE* request.
- `app.route()`: A decorator used to register a route. It accepts a `methods`
parameter to specify a list of accepted methods, default to *GET* only. It can also
be used on the `MethodView`-based view class.
- `$ flask run`: A command to output the spec to stdout or a file.

You can learn the details of these APIs in the [API reference](/api/app), or you can
continue to read the following chapters.
