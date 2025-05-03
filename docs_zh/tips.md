# Tips

## 在反向代理后运行应用程序

如果你在反向代理（例如 Nginx）后运行应用程序，需要像下面这样设置配置文件：

```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /;
    }
}
```

如果你的应用程序运行在不同的 URL 前缀下，需要同时更改 `location` 和 `X-Forwarded-Prefix` 头：

```hl_lines="5 10"
server {
    listen 80;
    server_name _;

    location /api {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /api;
    }
}
```

!!! warning

    从 1.2.1 版本开始，APIFlask 会自动更新 OpenAPI 的 `servers` 字段。
    如果你将 `AUTO_SERVERS` 配置设置为 `False`，则需要手动更新 `servers` 字段以指定 URL 前缀：

    ```python
    app.config['SERVERS'] = [{'url': '/api'}]
    ```

然后为你的应用程序应用代理修复中间件：

```python
from werkzeug.middleware.proxy_fix import ProxyFix
from apiflask import APIFlask


app = APIFlask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
```

另请参阅：

- [使用 Nginx 部署](https://flask.palletsprojects.com/deploying/nginx/)
- [告诉 Flask 它位于代理后](https://flask.palletsprojects.com/deploying/proxy_fix/)
