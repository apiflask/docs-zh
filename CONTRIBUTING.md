# 贡献指南

感谢你为 APIFlask 做出贡献。


## 支持问题

请不要在问题追踪器中提交支持问题。问题追踪器是用于处理 APIFlask 本身的错误和功能请求的工具。对于使用 APIFlask 或你自己代码中的问题，请使用以下资源：

- 首先使用 Google 搜索：`site:stackoverflow.com apiflask {搜索词、异常信息等}`。
- 在我们的 [GitHub Discussion][_gh_discuss] 中提问，在 "Q&A" 分类下创建讨论。
- 在 [Stack Overflow][_so] 上提问。

在你的帖子中包含以下信息：

- 描述你期望的结果。
- 如果可能，请包含一个 [最小可复现示例][_mcve]，以帮助我们识别问题。这也有助于检查问题是否出在你的代码中。
- 描述实际发生的情况。如果有异常，请包含完整的回溯信息。
- 列出你的 Python、Flask 和 APIFlask 版本。如果可能，请检查此问题是否已在最新版本或代码库的最新代码中修复。

[_gh_discuss]: https://github.com/apiflask/apiflask/discussions
[_so]: https://stackoverflow.com/questions/tagged/apiflask?tab=Frequent


## 报告问题

如果你发现与 APIFlask 本身相关的错误，或者认为 APIFlask 应该提供新的功能/增强功能，请随时在我们的 [问题追踪器][_gh_issue] 中创建问题。

在你的帖子中包含以下信息：

- 描述你期望的结果。
- 如果可能，请包含一个 [最小可复现示例][_mcve]，以帮助我们识别问题。这也有助于检查问题是否出在你的代码中。
- 描述实际发生的情况。如果有异常，请包含完整的回溯信息。
- 列出你的 Python、Flask 和 APIFlask 版本。如果可能，请检查此问题是否已在最新版本或代码库的最新代码中修复。

[_gh_issue]: https://github.com/apiflask/apiflask/issues
[_mcve]: https://stackoverflow.com/help/minimal-reproducible-example


## 提交补丁

如果你想提交的内容没有对应的开放问题，建议先打开一个问题进行讨论，然后再开始处理 PR。你可以处理任何没有关联开放 PR 或分配给维护者的问题。这些问题会显示在侧边栏中。无需询问是否可以处理你感兴趣的问题。

在你的补丁中包含以下内容：

- 如果你的补丁添加或更改了代码，请包含测试。确保测试在没有你的补丁时会失败。
- 更新任何相关的文档页面和文档字符串。文档页面和文档字符串应限制在 72 个字符以内。
- 在 `CHANGES.md` 中添加一条条目。使用与其他条目相同的风格。在相关的文档字符串中也包括 `Version Changed` 或 `Version Added` 部分。


### 第一次设置

- 下载并安装最新版本的 Git。
- 使用你的用户名和电子邮件配置 Git。

```
$ git config --global user.name 'your name'
$ git config --global user.email 'your email'
```

- 确保你有一个 GitHub 账户。
- 点击 "[Fork][_fork]" 按钮在 GitHub 上 fork APIFlask。
- 将你的 fork 仓库克隆到本地（将 `{username}` 替换为你的用户名）：

```
$ git clone https://github.com/{username}/apiflask
$ cd apiflask
$ git remote add upstream https://github.com/apiflask/apiflask
```

- 创建虚拟环境并安装依赖项：

对于 Linux/macOS：

```
$ python3 -m venv env
$ source env/bin/activate
$ python -m pip install --upgrade pip setuptools
$ pip install -r requirements/dev.txt
$ pip install -e .
$ pre-commit install
```

对于 Windows：

```
> python -m venv env
> env\Scripts\activate
> python -m pip install --upgrade pip setuptools
> pip install -r .\requirements\dev.txt
> pip install -e .
> pre-commit install
```

[_fork]: https://github.com/apiflask/apiflask/fork


### 开始编码

- 创建一个新分支来处理你想要解决的问题（请确保更新示例分支名称）：

```
$ git fetch upstream
$ git checkout -b your-branch-name upstream/main
```

- 使用你喜欢的编辑器进行更改，[并随时提交][_commit]。
- 包括覆盖你所做代码更改的测试。确保测试在没有你的补丁时会失败。按照下面的描述运行测试。
- 将你的提交推送到 GitHub 上的 fork 仓库：

```
$ git push --set-upstream origin your-branch-name
```

- [创建一个拉取请求][_pr]。在拉取请求中使用 `fixes #123` 链接到正在解决的问题。

[_commit]: https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
[_pr]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request


### 运行测试

使用 pytest 运行基本测试套件：

```
$ pytest
```

这将运行当前环境的测试，通常已经足够。你可以使用 tox 运行完整的测试套件（包括单元测试、测试覆盖率、代码风格检查、mypy 检查）：

```
$ tox
```


### 构建文档

使用 MkDocs 提供实时文档服务：

```
$ mkdocs serve
```

你还可以构建 HTML 文档以进行预览：

```
$ mkdocs build
```

在浏览器中打开 ``site/index.html`` 查看文档。
