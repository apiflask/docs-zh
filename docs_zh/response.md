# 响应格式化

首先阅读“基本用法”章节中的以下部分，了解有关响应格式化的基础知识：

- [使用 `@app.output` 格式化响应数据](/usage/#use-appoutput-to-format-response-data)
- [视图函数的返回值](/usage/#the-return-value-of-the-view-function)

响应格式化的基本概念：

- APIFlask 使用 [marshmallow](https://github.com/marshmallow-code/marshmallow) 来处理响应格式化。
- 视图函数返回的响应数据只会根据你的 schema 进行格式化，不会进行验证。
- 你只能为 JSON 响应体声明一个输出（使用一个 `app.output` 装饰器）。
- 视图的错误响应可以使用 `app.doc(response=...)` 来声明。

## 分页支持

APIFlask 提供了两个用于分页的工具：

- [apiflask.PaginationSchema](/api/schemas/#apiflask.schemas.PaginationSchema)
- [apiflask.pagination_builder](/api/helpers/#apiflask.helpers.pagination_builder)

`PaginationSchema` 是一个 schema 类，其中包含用于分页数据的常用字段。

`pagination_builder` 是一个用来为 `PaginationSchema` 生成分页数据的辅助函数。

下面为我们的宠物商店示例添加分页支持。首先，我们创建一个 PetQuerySchema 类：

```python
from apiflask import Schema
from apiflask.fields import Integer
from apiflask.validators import Range


class PetQuerySchema(Schema):
    page = Integer(load_default=1)  # 设置默认页面为 1
    # 将默认值设置为 20，并确保该值不超过 30
    per_page = Integer(load_default=20, validate=Range(max=30))
```

然后我们创建 PetOutSchema 类，与嵌套了 “PetOutSchema” 和 “PaginationSchema” 的
PetsOutSchema 类。

```python
from apiflask import Schema, PaginationSchema
from apiflask.fields import Integer, String, List, Nested


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


class PetsOutSchema(Schema):
    pets = List(Nested(PetOutSchema))
    pagination = Nested(PaginationSchema)
```

现在我们在 `get_pets` 视图中使用这些 schema：

```python
from apiflask import APIFlask, pagination_builder


@app.get('/pets')
@app.input(PetQuerySchema, 'query')
@app.output(PetsOutSchema)
def get_pets(query):
    pagination = PetModel.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    pets = pagination.items
    return {
        'pets': pets,
        'pagination': pagination_builder(pagination)
    }
```

在视图函数的返回值中，我们使用 `pagination_builder` 来构建分页数据，并通过 Flask-SQLAlchemy 传递 `pagination` 对象。

`pagination_builder` 函数是基于 Flask-SQLAlchemy 的 `Pagination` 类设计的。
如果你想使用自定义的分页类，请确保传递的 `pagination` 对象具有以下属性：

- `page`
- `per_page`
- `pages`
- `total`
- `next_num`
- `has_next`
- `prev_num`
- `has_prev`

你还可以编写自定义构建器函数和分页 schema 来构建你的自定义分页数据。

具体细节请参阅 [完整示例](https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py)

## 响应示例

你可以通过 `example` 和 `examples` 参数来为 OpenAPI spec 设置响应示例，请参阅 OpenAPI 支持章节中 [响应与请求示例](/openapi/#response-and-request-example)
来了解更多详情。

## 字典 schema

将 schema 传递给 `app.output` 时，你可以使用字典来代替 schema 类：

```python
from apiflask.fields import Integer


@app.get('/')
@app.output({'answer': Integer(dump_default=42)})
def get_answer():
    return {'answer': 'Nothing'}
```

字典 schema 的名称类似 `"Generated"`，可以用 `schema_name` 参数来指定 schema 名称：

```python
from apiflask.fields import Integer


@app.get('/')
@app.output({'answer': Integer(dump_default=42)}, schema_name='AnswerSchema')
def get_answer():
    return {'answer': 'Nothing'}
```

但是，我们建议尽可能创建一个 schema 类，这样会使代码易于阅读和复用。
