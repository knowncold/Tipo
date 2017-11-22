from app import app
from flask import render_template, request
from models import Blog, Comment, ErrorMessage
import datetime, json

@app.route('/')
@app.route('/index')
def index():
    blog = Blog.objects().order_by("-createTime")
    paged = blog.paginate(1, per_page=5)
    return render_template('index.html', blog=paged.items)

@app.route('/index/page/<page>')
def paged(page):
    blog = Blog.objects().order_by("-createTime")
    paged = blog.paginate(page=int(page), per_page=5)
    latest = Blog.objects().order_by('-createTime')[:5]
    latest_list = []
    tags = Blog.objects().distinct(field="tag")
    for i in latest:
        latest_list.append({"title":i.title, "createDay": str(i.createDay)[:10]})
    return render_template('index.html', blog_list=paged.items, latest_blog=latest_list, tag_cloud=tags)

@app.route('/blog/new', methods=['POST'])
def new_blog():
    get_json = request.get_json()
    if get_json.has_key('title'):
        title = get_json['title']
    else:
        return str(ErrorMessage(False, 'NO TITLE'))

    if get_json.has_key('content'):
        content = get_json['content']
    else:
        return str(ErrorMessage(False, 'NO CONTENT'))
    tags = ['test','yu']
    blog = Blog(title=title, content=content, tag=tags)
    blog.save()
    return str(ErrorMessage(True, ''))

@app.route('/blog/list', methods=['POST'])
def list_blog():
    get_json = request.get_json()
    page = get_json['page']
    blog = Blog.objects().order_by("-createTime")
    paged = blog.paginate(page=page, per_page=5)
    x = lambda a: a.to_json()
    b = map(x, paged.items)
    return str(ErrorMessage(True, b))

@app.route('/blog/latest', methods=['POST'])
def latest_blog():
    latest = Blog.objects().order_by('-createTime')[:5]
    latest_list = []
    for i in latest:
        latest_list.append({"title":i.title, "createDay": str(i.createDay)[:10]})
    return str(ErrorMessage(True, latest_list))

@app.route('/blog/get', methods=['POST'])
def get_blog():
    get_json = request.get_json()
    title = get_json['title']
    createDay = datetime.datetime.strptime(get_json['createDay'], '%Y-%m-%d')
    blog = Blog.objects.get_or_404(title=title, createDay=createDay)    # TODO change method
    blog.pageview += 1
    for post in Blog.objects(tag='yu'):
        print post.title
    blog.save()
    return str(ErrorMessage(True, blog.to_json()))

@app.route('/archive/count', methods=['POST'])      # month category
def count_archive():
    get_json = request.get_json()
    archive_type = get_json['type']
    num_count = {}
    if archive_type == 'category':
        for catgr in Blog.objects().distinct(field="category"):
            num = Blog.objects(category=catgr).count()
            num_count[catgr] = num
    elif archive_type == 'month':
        for mon in Blog.objects().distinct(field="month"):
            num = Blog.objects(month=mon).count()
            num_count[mon] = num
    return str(ErrorMessage(True, num_count))

@app.route('/archive/all', methods=['POST'])
def all_archive():
    get_json = request.get_json()
    archive_type = get_json["type"]
    key = get_json["key"]
    page = get_json["page"]
    if archive_type == "tag":
        blog = Blog.objects(tag=key)
    elif archive_type == "month":
        blog = Blog.objects(month=key)
    elif archive_type == "category":
        blog = Blog.objects(category=key)

    paged = blog.paginate(page=page, per_page=5)
    x = lambda a: a.to_json()
    b = map(x, paged.items)
    return str(ErrorMessage(True, b))

@app.route('/tag/get', methods=['POST'])
def get_tag():
    return str(ErrorMessage(True, Blog.objects().distinct(field="tag")))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

