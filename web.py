from flask import Flask, render_template, request, session, redirect
import settings
import re
import time
import backofpage
from settings import DATABASE
from bson import ObjectId

import pagination

app = Flask(__name__)
app.register_blueprint(backofpage.back)

# session 秘钥
app.secret_key = "succe$ss_login/$@#@$$^%%^%&**&^FDDSGGsdgsdgerwe3?0"
app.config['PERMANENT_SSESSION_LIFETIME'] = 3600  # session过期时间


@app.before_request
def permission():
    white_list = ['^/index', '^/readmore', '/login', '/uploadPhoto/', '^/static', '/link']

    if session.get('username'):
        return
    for item in white_list:
        if re.match(item, request.path):
            return
    else:
        return redirect('/login')


@app.route('/index/', methods=['GET', 'POST'])
@app.route('/index/page=<int:pk>')
@app.route('/index/tg=<tag>')
@app.route('/index/page=<pk>tg=<tag>')
def index(pk=None, tag=None):
    if request.method == 'GET':
        if tag:
            article_ret = DATABASE.article.find({"tag": tag})
        else:
            article_ret = DATABASE.article.find({})
        pager_obj = pagination.Pagination(pk, article_ret.count(), request.path)

        article_ret = article_ret[pager_obj.start:pager_obj.end]
        page = pager_obj.page_html()
        tag_ret = DATABASE.tag.find({})

        data = {'article_ret': article_ret, 'tag_ret': tag_ret}

        return render_template('index.html', data=data, page=page)

    if request.method == 'POST':
        wd = request.form.get('wd')
        ret = DATABASE.article.find({"title": {'$regex': wd}})

        pager_obj = pagination.Pagination(pk, ret.count(), request.path)

        article_ret = ret[pager_obj.start:pager_obj.end]
        page = pager_obj.page_html()
        tag_ret = DATABASE.tag.find({})
        data = {'article_ret': article_ret, 'tag_ret': tag_ret}

        return render_template('index.html', data=data, page=page)


@app.route('/readmore/<id>')
def readmore(id):
    ret = DATABASE.article.find_one({'_id': ObjectId(id)})
    tag_ret = DATABASE.tag.find({})

    data = {'data': ret, 'tag_ret': tag_ret}
    return render_template('readmore.html', data=data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        ret = settings.DATABASE.userinfo.find_one({'username': username, 'password': password})

        if ret:
            session['username'] = username
            return redirect('/index')

        return render_template('login.html', msg='您输入的用户名或密码错误')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404


@app.route('/link')
def link():
    return render_template('link.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/index')


def format_date(timestamp):
    timeStruct = time.localtime(timestamp)
    res = time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    return res


def search_date(timestamp):
    timeStruct = time.localtime(timestamp)
    res = time.strftime('%Y-%m-%d', timeStruct)

    return res


app.add_template_filter(format_date, 'format_time')
app.add_template_filter(format_date, 'search_date')

if __name__ == '__main__':
    app.run('0.0.0.0', 10086, debug=True)
