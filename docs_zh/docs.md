# 文档目录

欢迎阅读 APIFlask 的文档。


## 目录

你可以通过阅读以下章节来了解 APIFlask 的用法：

- **[引言](/)**：一个关于 APIFlask 的总体介绍。
- **[从 Flask 迁移](/migrating)**：迁移指南与注意事项。
- **[基本用法](/usage)**：开始使用 APIFlask。
- **[请求处理](/request)**：对 `@app.input` 装饰器的详细介绍。
- **[响应格式化](/response)**： 对 `@app.output` 装饰器的详细介绍。
- **[数据 Schema](/schema)**：如何编写输入数据与输出数据的 schema。
- **[OpenAPI 支持](/openapi)**：生成 OpenAPI spec 的原理，以及如何通过 `@app.doc` 装饰器和配置变量来进行自定义。
- **[安全认证](/authentication)**：给你的应用实现认证支持。
- **[Swagger UI 和 Redoc](/api-docs)**：API 文档工具的用法和配置
- **[配置](/configuration)**：内置的配置变量表。
- **[应用示例](/examples)**：应用示例集。

以下章节对贡献者和想要继续了解 APIFlask 的人有用。

- **[API 参考](/api/app)**：APIFlask 的 API 参考。
- **[比较与动机](/comparison)**：APIFlask 和类似项目的区别。
- **[作者](/authors)**：APIFlask 的作者。
- **[变更日志](/changelog)**：APIFlask 各个版本的变更日志。


## 外部文档

在 APIFlask 文档中，我将尝试覆盖所有的基本用法。然而，如果要使用一些高级用法，你可能需要
阅读一些 APIFlask 依赖的框架、工具的文档：

- **[Flask][_flask]{target=_blank}**：你有必要掌握 Flask 的知识。
- **[marshmallow][_marshmallow]{target=_blank}**：Schema 的高级用法参考。
- **[Flask-HTTPAuth][_flask_httpauth]{target=_blank}**：`HTTPBasicAuth` 和 `HTTPTokenAuth` 的高级用法参考。
- **[webargs][_webargs]{target=_blank}**：如果你是贡献者，这将会有用。
- **[apispec][_apispec]{target=_blank}**：如果你是贡献者，这将会有用。
- **[OpenAPI][_openapi]{target=_blank}**：这是 OpenAPI 的规范。
- **[JSON Schema][_jsonschema]{target=_blank}**：当你想要设定一个个性化的错误响应 schema 而且不想用 schema 类时，这将很有用。

[_flask]：https://flask.palletsprojects.com/
[_marshmallow]：https://marshmallow.readthedocs.io/
[_flask_httpauth]：https://flask-httpauth.readthedocs.io/
[_webargs]：https://webargs.readthedocs.io/
[_apispec]：https://apispec.readthedocs.io/
[_openapi]：https://github.com/OAI/OpenAPI-Specification/tree/main/versions
[_jsonschema]：https://json-schema.org/
