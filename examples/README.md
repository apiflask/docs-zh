# 示例程序

- 基础示例：[/examples/basic/app.py][_basic]
- 类视图示例：[/examples/cbv/app.py][_cbv]
- ORM 示例 (基于 Flask-SQLAlchemy)：[/examples/orm/app.py][_orm]
- 分页示例 (基于 Flask-SQLAlchemy)：[/examples/pagination/app.py][_pagination]
- OpenAPI 示例：[/examples/openapi/app.py][_openapi]
- 基础响应示例：[/examples/base_response/app.py][_base_response]
- Token 认证示例：[/examples/auth/token_auth/app.py][_token_auth]
- Basic 认证示例：[/examples/auth/basic_auth/app.py][_basic_auth]
- Dataclass 示例（基于 marshmallow-dataclass）：[/examples/dataclass/app.py][_dataclass]

[_basic]: https://github.com/apiflask/apiflask/tree/main/examples/basic/app.py
[_cbv]: https://github.com/apiflask/apiflask/tree/main/examples/cbv/app.py
[_orm]: https://github.com/apiflask/apiflask/tree/main/examples/orm/app.py
[_pagination]: https://github.com/apiflask/apiflask/tree/main/examples/pagination/app.py
[_openapi]: https://github.com/apiflask/apiflask/tree/main/examples/openapi/app.py
[_base_response]: https://github.com/apiflask/apiflask/tree/main/examples/base_response/app.py
[_token_auth]: https://github.com/apiflask/apiflask/tree/main/examples/auth/token_auth/app.py
[_basic_auth]: https://github.com/apiflask/apiflask/tree/main/examples/auth/basic_auth/app.py
[_dataclass]: https://github.com/apiflask/apiflask/tree/main/examples/dataclass/app.py

如果你已经使用 APIFlask 开发了一个程序，可以提交 PR 在这里添加链接：

- [Flog](https://github.com/flog-team/flog-api-v4)（WIP）

按照 *安装* 部分中的命令在计算机上运行这些示例。


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


### 选择程序

每个示例程序存储在一个子文件夹中：

- `/basic`：基础示例
- `/cbv`：类视图示例
- `/orm`：ORM 示例 (基于 Flask-SQLAlchemy)
- `/pagination`：分页示例 (基于 Flask-SQLAlchemy)
- `/openapi`：OpenAPI 示例
- `/base_response`：基础响应示例
- `/auth/token_auth`：Token 认证示例
- `/auth/basic_auth`：Basic 认证示例
- `/dataclass`：Dataclass 示例（基于 marshmallow-dataclass）

要运行特定示例，必须更改为相应的文件夹。例如，如果你想运行基本示例：

```bash
$ cd basic
```


### 运行程序

切换到所需文件夹后，使用 `flask run` 命令运行示例程序：

```bash
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```


## 试试看

当程序运行时，你可以访问位于 <http://localhost:5000/docs> 的交互式 API 文档。在每个端点的详细信息选项卡中，你可以点击“试用”按钮来测试这些 API：

![](https://apiflask.com/_assets/try-it-out.png)

然后点击“执行”按钮，它将向相关端点发送请求：

![](https://apiflask.com/_assets/execute.png)


## 做一些实验

如果你想对示例程序进行一些实验，只需使用你喜欢的编辑器修改 `app.py`。如果想要在每次更改代码后自动重载程序，使用 `flask run` 的 `--reload` 选项：

```bash
$ flask run --reload
```

此外，你也可以在调试模式下运行程序，它将默认启用重新加载器和调试器。要启用调试模式，需要在执行 `flask run` 之前将环境变量 `FLASK_ENV` 设置为 `development`，详情见 [调试模式](https://flask.palletsprojects.com/en/main/quickstart/#debug-mode)。
