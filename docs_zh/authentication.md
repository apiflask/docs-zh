# 安全认证

首先阅读基本用法中的 [这一部分](/usage/#use-appauth_required-to-protect-your-views)
来了解安全认证支持的基础知识。

安全认证支持的基本概念：

- APIFlask 使用 Flask-HTTPAuth 来实现认证支持。
- 使用 [`apiflask.HTTPBasicAuth`](/api/security/#apiflask.security.HTTPBasicAuth) 来进行 HTTP 基本身份验证（HTTP Basic Auth）。
- 使用 [`apiflask.HTTPTokenAuth`](/api/security/#apiflask.security.HTTPTokenAuth) 来进行 HTTP Bearer 或 API 密钥认证。
- 阅读 [Flask-HTTPAuth 的文档](https://flask-httpauth.readthedocs.io/) 来实现各种安全认证方式。
- 请确保从 APIFlask 导入 `HTTPBasicAuth` 和 `HTTPTokenAuth` 并使用 `app.auth_required` 装饰器来保护视图。
- `auth.current_user` 的工作方式与 `auth.current_user()` 类似，但长度更短。

## 使用外部安全认证库

!!! warning "Version >= 1.0.0"

    这个特性在 [1.0.0 版本](/changelog/#version-100) 中添加。

使用 `HTTPBasicAuth`、`HTTPTokenAuth` 和 `app.auth_required` 实现安全认证时，APIFlask 可以自动生成 OpenAPI 安全规范。当你使用外部安全认证库，APIFlask 仍然提供手动设置 OpenAPI 规范的方式。

你可以使用 `SECURITY_SCHEMES` 配置或 `app.security_schemes` 属性来设置 OpenAPI security scheme：

```python
app = APIFlask(__name__)
app.security_schemes = {  # 等同于 SECURITY_SCHEMES 配置
    'ApiKeyAuth': {
      'type': 'apiKey',
      'in': 'header',
      'name': 'X-API-Key',
    }
}
```
然后你可以在 `app.doc()` 装饰器中使用 `security` 参数设置 security scheme：

```python hl_lines="5"
@app.post('/pets')
@my_auth_lib.protect  # 使用外部安全认证库提供的装饰器保护路由
@app.input(PetInSchema)
@app.output(PetOutSchema, 201)
@app.doc(security='ApiKeyAuth')
def create_pet(data):
    pet_id = len(pets)
    data['id'] = pet_id
    pets.append(data)
    return pets[pet_id]
```


## 处理安全认证错误

请参见错误处理章节中的 [这一部分](/error-handling/#handling-authentication-errors) 来处理安全认证错误。
