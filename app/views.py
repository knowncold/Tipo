from app import app
from flask import render_template, request
from models import Blog, Comment, ErrorMessage
import datetime, json

def latest_blog():
    return Blog.objects().order_by('-createTime')[:5]

def tag_cloud():
    return Blog.objects().distinct(field="tag")

@app.route('/')
@app.route('/index')
@app.route('/index/<page>')
def paged(page=1):
    blog = Blog.objects().order_by("-createTime")
    paged = blog.paginate(page=int(page), per_page=5)
    count = blog.count()
    return render_template('index.html', blog_list=paged.items, latest_blog = latest_blog(), tags=tag_cloud(), current_page=int(page), count=count, archive='index', month=month_archive())

@app.route('/search')
@app.route('/search/<page>')
def serach(page=1):
    keyword = request.args.get("value")
    blog = Blog.objects(content__contains=keyword).order_by("-createTime")
    paged = blog.paginate(page=int(page), per_page=5)
    count = blog.count()
    return render_template('index.html', blog_list=paged.items, latest_blog = latest_blog(), tags=tag_cloud(), current_page=int(page), count=count, archive='search', month=month_archive())

@app.route('/archive')
def archive():
    archive_list = {}
    month = Blog.objects().order_by("month").distinct(field="month")[::-1]
    for m in month:
        archive_list[datetime.datetime.strftime(datetime.datetime.strptime(m, "%Y-%m"), "%B")]=(Blog.objects(month=m).order_by("-createTime"))
    return render_template('archive.html', latest_blog=latest_blog(), tags=tag_cloud(), month=month_archive(), blog_list=archive_list)

@app.route('/about')
def about():
    return render_template('about.html', latest_blog=latest_blog(), tags=tag_cloud(), month=month_archive())

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
        createTime = createDay
        month = createDay[:7]
    else:
        createDay = None
    if get_json.has_key('tags'):
        tags = get_json['tags']
    else:
        tags = None
    category = get_json['category']

    blog = Blog(title=title, createTime=createTime, content=content, tag=tags, createDay=createDay, category=category, month=month)
    blog.save()
    return str(ErrorMessage(True, ''))

@app.route('/post/<year>/<month>/<day>/<title>')
def get_blog(year, month, day, title):
    createDay = datetime.datetime.strptime(year+'-'+month+'-'+day, '%Y-%m-%d')
    blog = Blog.objects.get_or_404(title=title, createDay=createDay)
    blog.pageview += 1
    blog.save()
    return render_template('post.html', blog=blog, latest_blog=latest_blog(), tags=tag_cloud(), month=month_archive())

def month_archive():
    num_count = {}
    for mon in Blog.objects().distinct(field="month"):
        num_count[mon+datetime.datetime.strftime(datetime.datetime.strptime(mon, "%Y-%m"), "%Y%b")] = Blog.objects(month=mon).count()
    num_count = sorted(num_count.items(), reverse=True)
    return num_count

@app.route('/category/<category>')
@app.route('/category/<category>/<page>')
def archive_category(category, page=1):
    blog = Blog.objects(category=category).order_by("-createtime")
    paged = blog.paginate(page=int(page), per_page=5)
    count = blog.count()
    return render_template('index.html', blog_list=paged.items, latest_blog = latest_blog(), tags=tag_cloud(), current_page=int(page), count=count, archive='category/'+category)

@app.route('/tag/<tag>')
@app.route('/tag/<tag>/<page>')
def archive_tag(tag, page=1):
    blog = Blog.objects(tag=tag).order_by("-createtime")
    paged = blog.paginate(page=int(page), per_page=5)
    count = blog.count()
    return render_template('index.html', blog_list=paged.items, latest_blog = latest_blog(), tags=tag_cloud(), current_page=int(page), count=count, archive='tag/'+tag, month=month_archive())

@app.route('/month/<year>/<month>')
@app.route('/month/<year>/<month>/<page>')
def archive_month(year, month, page=1):
    blog = Blog.objects(month=year+'-'+month).order_by("-createtime")
    paged = blog.paginate(page=int(page), per_page=5)
    count = blog.count()
    return render_template('index.html', blog_list=paged.items, latest_blog = latest_blog(), tags=tag_cloud(), current_page=int(page), count=count, archive='tag/', month=month_archive())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', latest_blog = latest_blog(), tags=tag_cloud(), month = month_archive()), 404

