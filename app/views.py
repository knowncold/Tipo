from app import app
from flask import render_template, request
from models import Blog, Comment, ErrorMessage
import datetime, json

def latest_blog():
    latest = Blog.objects().order_by('-createTime')[:5]
    return latest

def tag_cloud():
    return Blog.objects().distinct(field="tag")

@app.route('/')
@app.route('/index')
@app.route('/index/page/<page>')
def paged(page=1):
    blog = Blog.objects().order_by("-createTime")
    paged = blog.paginate(page=int(page), per_page=5)
    return render_template('index.html', blog_list=paged.items, latest_blog=latest_blog(), tags=tag_cloud())

@app.route('/archive')
def archive():
    return render_template('archive.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

    if get_json.has_key('createDay'):
        createDay = get_json['createDay']
    else:
        createDay = None
    if get_json.has_key('tags'):
        tags = get_json['tags']
    else:
        tags = None

    blog = Blog(title=title, content=content, tag=tags, createDay=createDay)
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

@app.route('/post/<year>/<month>/<day>/<title>')
def get_blog(year, month, day, title):
    createDay = datetime.datetime.strptime(year+'-'+month+'-'+day, '%Y-%m-%d')
    blog = Blog.objects.get_or_404(title=title, createDay=createDay)    # TODO change method
    blog.pageview += 1
    blog.save()
    return render_template('blog_detail.html')

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

@app.route('/archive/all')
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

