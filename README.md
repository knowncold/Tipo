# BackEnd of Tipo

## 部署

## 服务器信息

 - 地址:`http://127.0.0.1:5000`
 - 请求方式全部为POST

## 接口列表

### 新建博客
创建新博客

> /blog/new

### Request Data

```json
{
	"title" : "Test Title",
	"content" : "Lorem ipsizzle funky fresh i'm in the shizzle boom shackalack, consectetizzle adipiscing my shizz. Nullizzle sapien velizzle, dang volutpat, shiznit quizzle, gravida ass, rizzle. Pot get down get down tortor. Sed erizzle. Black go to hizzle dolizzle dapibizzle turpis fo shizzle my nizzle yo. Maurizzle pellentesque nibh et check it out. Bow wow wow check it out tortizzle. Pellentesque for sure rhoncizzle bow wow wow. In owned habitasse brizzle dictumst. Nizzle dapibizzle. Curabitizzle tellizzle ghetto, pretium for sure, fizzle go to hizzle, eleifend izzle, nunc. Dope suscipizzle. Integizzle boom shackalack velit ass purus.",
	"tag" : ["ctf", "web", "python"],
	"category" : "life",
	"creatDay" : "2017-11-11"
}
```

其中`category`非必需。

### Response Data

```json
{
	"status" : true,
	"msg" : ""
}
```

### 博客列表
分页每页五篇地获取博客内容

> /blog/list

### Request Data

### Response Data


### 最新博客
获得最新的五篇博客的标题

> /blog/latest

### Request Data

### Response Data


### 博客详情
获得单个博客地内容，通过创建日期和标题来唯一标识。

> /blog/get

### Request Data

```json
{
	"title":"test title",
	"createDay":"2017-11-19"
}
```

### Response Data

```json
{
    "status": true,
    "msg": {
        "category": "uncategoried",
        "pageview": 5,
        "title": "test yu",
        "tag": [
            "test",
            "yu"
        ],
        "content": "qwe",
        "createDay": "2017-11-19 00:00:00",
        "createTime": "2017-11-19 10:40:36.596000"
    }
}
```

### 归档计数
按月份或者分类来获得归档的数量

> /archive/count

### Request Data

```json
{
	"type" : "category | month"
}
```

### Response Data

```json
{
    "status": true,
    "msg": {
        "2017-09": 2,
        "2017-11": 1,
        "2017-10": 2
    }
}
```

```json
{
    "status": true,
    "msg": {
        "uncategoried": 6
    }
}
```

### 归档
通过月份、分类、标签来获得归档的列表

> /archive/all

### Request Data

### Response Data


### 获取标签
获取网站的标签列表

> /tag/get

### Request Data

### Response Data


