from flask import Blueprint, render_template, request, redirect, session
from werkzeug import secure_filename
import time
import random
import os


from bson import ObjectId

from settings import DATABASE

back = Blueprint("back", __name__, template_folder='backpage')

UPLOAD_FOLDER = '/static/uploadPhotos/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@back.route('/backpage')
def backpage():
    article_ret = DATABASE.article.find({})
    tag_ret = DATABASE.tag.find({})
    data = {'article_ret': article_ret, 'tag_ret': tag_ret}
    return render_template('backpage.html', data=data)


@back.route("/select/<tag>/<condition>")
def select_condition(tag, condition):
    tag_ret = DATABASE.tag.find({})
    ret = DATABASE.article.find({tag: condition})
    data = {'article_ret': ret, 'tag_ret': tag_ret}
    return render_template('backpage.html', data=data)


@back.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        ret = DATABASE.article.find_one({'_id': ObjectId(id)})
        return render_template('add_blog.html', ret=ret)
    elif request.method == 'POST':
        title = request.form.get('title')
        tag = request.form.get('tag')
        post_full = request.form.get('source_code')
        plain_text = request.form.get('plain_text')[0:150]

        article_ret = DATABASE.article.update_one({"_id": ObjectId(id)},
                                                  {'$set': {'title': title, 'tag': tag, 'author': session['username'],
                                                            'summary': plain_text, 'text': post_full,
                                                            'edittime': time.time()}})

        if DATABASE.tag.find_one({'tag': tag}):
            tag_ret = DATABASE.tag.update_one({"tag": tag}, {"$inc": {'count': 1}})
        else:
            tag_ret = DATABASE.tag.insert_one({"tag": tag, 'count': 1})

        return 'success'


@back.route('/del/<id>')
def delete(id):
    ret = DATABASE.article.find_one({'_id': ObjectId(id)})
    if ret:
        # print(dir(ret), ret.get("tag"))
        DATABASE.tag.update_one({'tag': ret.get("tag")}, {"$inc": {'count': -1}})
        DATABASE.article.remove({'_id': ObjectId(id)})
        return redirect('/backpage')
    else:
        return 'error'


@back.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('add_blog.html',ret='')
    else:
        title = request.form.get('title')
        tag = request.form.get('tag')
        post_full = request.form.get('source_code')
        plain_text = request.form.get('plain_text')[0:200]
        path = os.path.join(os.getcwd(), 'static')
        phpot_list = file_name(path)
        title_picture = random.choice(phpot_list)
        path,name = os.path.split(title_picture)

        # 'title_picture':title_picture,
        article_ret = DATABASE.article.insert_one(
            {'title': title, 'tag': tag,  'author': session['username'],'title_picture':name, 'summary': plain_text, 'text': post_full,
             'createtime': time.time(),
             'edittime': time.time()})

        if DATABASE.tag.find_one({'tag': tag}):
            tag_ret = DATABASE.tag.update_one({"tag": tag}, {"$inc": {'count': 1}})
        else:
            tag_ret = DATABASE.tag.insert_one({"tag": tag, 'count': 1})

        return 'success'


@back.route('/uploadPhoto/', methods=['POST'])
def uploadPhoto():
    '''
            the photo which I upload name 'file'
    '''

    if hasattr(request, 'files') and 'file' in request.files:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dotPos = filename.rindex('.')
            filename = str(int(time.time())) + '.' + filename[dotPos + 1:]
            file.save(back.root_path + UPLOAD_FOLDER + filename)

            return UPLOAD_FOLDER + filename

        else:
            return '您上传的而文件存在问题'

    else:
        return '文件名称不存在'



def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L