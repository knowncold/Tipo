from app import app
from flask import render_template, request
from models import Blog, Comment, ErrorMessage
import datetime

@app.route('/')
def index():
    return "HOME"

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
    return ''

@app.route('/blog/latest', methods=['POST'])
def latest_blog():
    return ''

@app.route('/blog/get', methods=['POST'])
def get_blog():
    get_json = request.get_json()
    title = get_json['title']
    createDay = datetime.datetime.strptime(get_json['createDay'], '%Y-%m-%d')
    blog = Blog.objects.get_or_404(title=title, createDay=createDay)
    blog.pageview += 1
    for post in Blog.objects(tag='yu'):
        print post.title
    blog.save()
    return str(ErrorMessage(True, blog.to_json()))

# @app.route('/comment/new', methods=['POST'])
# def new_comment():
    # return ''

# @app.route('/comment/list', methods=['POST'])
# def list_comment():
    # return ''

# @app.route('/comment/latest', methods=['POST'])
# def latest_comment():
    # return ''

@app.route('/archive/count', methods=['POST'])      # month category
def count_archive():
    return ''

@app.route('/archive/all', methods=['POST'])
def all_archive():
    return ''

@app.route('/tag/get', methods=['POST'])
def get_tag():
    return ''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

