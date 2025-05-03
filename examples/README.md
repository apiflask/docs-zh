# 示例程序

- 基础示例：[/examples/basic/app.py][_basic]
- 基于类的视图示例：[/examples/cbv/app.py][_cbv]
- ORM 示例（使用 Flask-SQLAlchemy）：[/examples/orm/app.py][_orm]
- 分页示例（使用 Flask-SQLAlchemy）：[/examples/pagination/app.py][_pagination]
- OpenAPI 相关示例：[/examples/openapi][_openapi]
- 基础响应示例：[/examples/base_response/app.py][_base_response]
- Token 身份验证示例：[/examples/auth/token_auth/app.py][_token_auth]
- 基础身份验证示例：[/examples/auth/basic_auth/app.py][_basic_auth]
- 数据类示例（使用 marshmallow-dataclass）：[/examples/dataclass/app.py][_dataclass]
- 文件上传示例：[/examples/file_upload/app.py][_file_upload]

[_basic]: https://github.com/apiflask/apiflask/tree/main/examples/basic/app.py
[_cbv]: https://github.com/apiflask/apiflask/tree/main/examples/cbv/app.py
[_orm]: https://github.com/apiflask/apiflask/tree/main/examples/orm/app.py
[_pagination]: https://github.com/apiflask/apiflask/tree/main/examples/pagination/app.py
[_openapi]: https://github.com/apiflask/apiflask/tree/main/examples/openapi
[_base_response]: https://github.com/apiflask/apiflask/tree/main/examples/base_response/app.py
[_token_auth]: https://github.com/apiflask/apiflask/tree/main/examples/auth/token_auth/app.py
[_basic_auth]: https://github.com/apiflask/apiflask/tree/main/examples/auth/basic_auth/app.py
[_dataclass]: https://github.com/apiflask/apiflask/tree/main/examples/dataclass/app.py
[_file_upload]: https://github.com/apiflask/apiflask/tree/main/examples/file_upload/app.py

如果您使用 APIFlask 构建了一个应用程序，欢迎提交 Pull Request 将源码链接添加到此处。

- [Flog](https://github.com/flog-team/flog-api-v4)（正在积极开发中）

按照*安装*部分的命令在您的计算机上运行这些示例。


## 安装


### 构建环境

对于 macOS 和 Linux：

```bash
$ git clone https://github.com/apiflask/apiflask
$ cd apiflask/examples
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

对于 Windows：

```text
> git clone https://github.com/apiflask/apiflask
> cd apiflask\examples
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
```


### 选择应用程序

每个示例程序存储在一个子文件夹中：

- `/basic`：基础示例
- `/cbv`：基于类的视图示例
- `/orm`：ORM 示例（使用 Flask-SQLAlchemy）
- `/pagination`：分页示例（使用 Flask-SQLAlchemy）
- `/openapi/basic`：基础 OpenAPI 示例
- `/openapi/custom_decorators`：带有自定义装饰器的 OpenAPI 示例
- `/openapi/static_docs`：独立静态 HTML OpenAPI 文档示例
- `/base_response`：基础响应示例
- `/dataclass`：数据类示例（使用 marshmallow-dataclass）

要运行特定示例，您需要切换到相应的文件夹。
例如，如果您想运行基础示例：

```bash
$ cd basic
```


### 运行示例程序

切换到目标文件夹后，使用 `flask run` 命令运行示例程序：

```bash
$ flask run
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```


## 试一试

当应用程序运行后，您可以访问交互式 API 文档：<http://localhost:5000/docs>。在每个端点的详细选项卡中，您可以点击“Try it out”按钮测试 API：

![](https://apiflask.com/_assets/try-it-out.png)

然后点击“Execute”按钮，它会向相关端点发送请求并返回响应：

![](https://apiflask.com/_assets/execute.png)


## 做一些实验

如果您想对示例程序进行一些实验，只需用您喜欢的编辑器打开 `app.py` 文件。为了让应用程序在每次更改代码后自动重新加载，可以为 `flask run` 添加 `--reload` 选项：

```bash
$ flask run --reload
```

或者以调试模式运行：

```bash
$ flask run --debug
```

在调试模式下，它会默认启用重新加载器和调试器。有关更多详细信息，请参阅*[调试模式](https://flask.palletsprojects.com/en/main/quickstart/#debug-mode)*。
