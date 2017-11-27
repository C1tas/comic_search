from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from comic_web.db.backends import db

app = Flask(__name__)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
app.debug = True

@app.route('/')
def display_comic():
    deault_comic_id = 'Xiaopaiqiu'
    comic_list = db.get_comic_list()

    return render_template('comic.pug', temp_comic_list=comic_list)

@app.route('/<comic_id>')
def display_menu(comic_id):
    deault_comic_id = 'Xiaopaiqiu'
    current_comic_id = comic_id if comic_id else deault_comic_id
    chapter_list = db.get_comic_chapters(current_comic_id)

    return render_template('index.pug', temp_chapter_list=chapter_list, temp_cur_comic_id=current_comic_id)
    # return str(chapter_list)


@app.route('/reader/<comic_id>/<comic_hui>')
def display_hui(comic_id, comic_hui):
    current_img_list, current_hash_list = db.get_comic_imgs(comic_id, comic_hui)

    return render_template('reader.pug', temp_img_list=current_img_list, temp_hash_list=current_hash_list)


@app.route('/api/more', methods=['GET', 'POST'])
def get_more():
    # print(request.form['a'])
    if request.form['comic_id'] and request.form['comic_hui'] and request.form['cur_img_order']:
        
        return request.form['b']
