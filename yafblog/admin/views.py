from functools import wraps
from urllib.parse import quote,unquote
from flask import Blueprint, render_template, g, url_for, request,abort,jsonify,g,session,flash,redirect
from datetime import date,time,timedelta
from ..models.article import Article
from ..models.category import Category
from ..models.tag import Tag
from ..models.admin import Admin
from ..helpers import CacheFile, search_list, pages, month_range, week_range
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('您需要登录，才能继续操作！', 'warning')
            return redirect(url_for('admin.login')+'?jump='+quote(request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@require_login
def index():
    week_range()
    article_all = Article.count()
    article_week = Article.count("addtime BETWEEN ? AND ?", week_range())
    article_month = Article.count("addtime BETWEEN ? AND ?", month_range())

    category_all = Category.count()
    category_week = Category.count("addtime BETWEEN ? AND ?", week_range())
    category_month = Category.count("addtime BETWEEN ? AND ?", month_range())

    tag_all = Tag.count()
    tag_week = Tag.count("addtime BETWEEN ? AND ?", week_range())
    tag_month = Tag.count("addtime BETWEEN ? AND ?", month_range())
    return render_template('admin/index.html',
                            article_week = article_week,
                            article_month = article_month,
                            article_all = article_all,
                            category_week = category_week,
                            category_month = category_month,
                            category_all = category_all,
                            tag_week = tag_week,
                            tag_month = tag_month,
                            tag_all = tag_all,

                            username=session['admin']['username'])

@admin.route('/login', methods=['GET','POST'])
def login():
    if 'admin' in session:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form.get('username', '', type=str)
        if not username:
            return jsonify({'code':-1, 'msg':'请输入用户名'})
        password = request.form.get('password', '', type=str)
        if not password:
            return jsonify({'code':-1, 'msg':'请输入密码'})
        jump = request.form.get('jump', url_for('admin.index'))
        res = Admin.login(username, password)
        if res['code'] > 0:
            session['admin'] = res['info']
            return jsonify({'code':1, 'jump':jump})
        return jsonify({'code':-1, 'msg':res['msg']})
    jump = request.args.get('jump', '')
    return render_template('admin/login.html', jump=jump)

@admin.route('/logout')
@require_login
def logout():
    session.pop('admin', None)
    flash('您已经退出了系统', 'warning')
    return redirect(url_for('admin.login'))

@admin.route('/article', methods=['GET'])
@require_login
def article():
    article_num = Article.count()
    limit = ((g.page - 1) * g.per_page, g.per_page)
    articles = Article.findAll(None,orderBy='addtime DESC',limit=limit)
    page_list = pages(g.page, article_num, g.per_page,  url_for('admin.article'))
    return render_template('admin/article.html',
                            articles=articles,
                            categorys=g.categorys,
                            tags=g.tags,
                            username=session['admin']['username'],
                            page_list=page_list)



@admin.route('/article/add', methods=['GET','POST'])
@require_login
def article_add():
    if request.method == 'POST':
        tag = request.form.getlist('tag')
        title = request.form.get('title', '', type=str)
        if not title:
            return jsonify({'code':-1, 'msg':'请填写标题'})
        category = request.form.get('category', '', type=int)
        if not category:
            return jsonify({'code':-1, 'msg':'请选择类别'})
        content = request.form.get('content', '', type=str)
        if not content:
            return jsonify({'code':-1, 'msg':'请填写内容'})
        article = Article( tags = tag, title=title, category=category, content=content)
        res = article.save()
        return jsonify(res);
    return render_template('admin/article_add.html',
                            username=session['admin']['username'],
                            categorys=g.categorys,
                            tags=g.tags)

@admin.route('/article/<article_id>/edit', methods=['GET','POST'])
@require_login
def article_edit(article_id):
    article_info = Article.findOne('id=?', [article_id])
    if not article_info:
        abort(404)
    article = Article(__data__=article_info)
    if request.method == 'POST':
        tag = request.form.getlist('tag')
        article.tags = tag
        title = request.form.get('title', '', type=str)
        if title:
            article.title = title
        else:
            return jsonify({'code':-1, 'msg':'请填写标题'})
        category = request.form.get('category', '', type=int)
        if category:
            article.category = category
        else:
            return jsonify({'code':-1, 'msg':'请选择类别'})
        content = request.form.get('content', '', type=str)
        if content:
            article.content = content
        else:
            return jsonify({'code':-1, 'msg':'请填写内容'})
        res = article.update(article_info)
        return jsonify(res);
    if article_info['tags']:
        article_info['tags'] = article_info['tags'].split(',')
    return render_template('admin/article_add.html',
                            username=session['admin']['username'],
                            categorys=g.categorys,
                            tags=g.tags,
                            article=article_info)

@admin.route('/article/<article_id>/del', methods=['GET','POST'])
@require_login
def article_del(article_id):
    if request.method == 'POST':
        res = Article.removeById(article_id)
        return jsonify(res)
    return render_template('admin/modal.html',
                            title='删除文章',
                            forms=[ {'type':'msg','content':'确定要删除文章吗？', 'class':'text-danger'}],
                            action=url_for('admin.article_del', article_id=article_id));

# Category
@admin.route('/category', methods=['GET'])
@require_login
def category():
    category_num = Category.count()
    limit = ((g.page - 1) * g.per_page, g.per_page)
    categorys = Category.findAll(None,None,limit=limit)
    page_list = pages(g.page, category_num, g.per_page,  url_for('admin.category'))
    return render_template('admin/category.html',
                            categorys=categorys,
                            username=session['admin']['username'],
                            page_list=page_list)

@admin.route('/category/add', methods=['POST'])
@require_login
def category_add():
    name = request.form.get('name', '', type=str)
    if not name:
        return jsonify({'code':-1, 'msg':'请填写标题'})
    category = Category(name=name)
    res = category.save()
    return jsonify(res)

@admin.route('/category/<category_id>/edit', methods=['GET','POST'])
@require_login
def category_edit(category_id):
    category_info = Category.findOne('id=?', [category_id])
    if request.method == 'POST':
        category = Category(__data__=category_info)
        name = request.form.get('name', '', type=str)
        if name:
            category.name = name
        else:
            return jsonify({'code':-1, 'msg':'请填写标题'})
        res = category.update(category_info)
        return jsonify(res);
    return render_template('admin/modal.html',
                            title='编辑类别',
                            forms=[ {'type':'text','name':'name', 'value':category_info['name']}, ],
                            action=url_for('admin.category_edit', category_id=category_id));

@admin.route('/category/del/<category_id>', methods=['GET','POST'])
@require_login
def category_del(category_id):
    if request.method == 'POST':
        res = Category.removeById(category_id)
        return jsonify(res)
    return render_template('admin/modal.html',
                            title='删除类别',
                            forms=[ {'type':'msg','content':'确定要删除类别吗？', 'class':'text-danger'}],
                            action=url_for('admin.category_del', category_id=category_id));

# Tag
@admin.route('/tag', methods=['GET'])
@require_login
def tag():
    tag_num = Tag.count()
    limit = ((g.page - 1) * g.per_page, g.per_page)
    tags = Tag.findAll(None,None,limit=limit)
    page_list = pages(g.page, tag_num, g.per_page,  url_for('admin.tag'))
    return render_template('admin/tag.html',
                            tags=tags,
                            username=session['admin']['username'],
                            page_list=page_list)

@admin.route('/tag/add', methods=['POST'])
@require_login
def tag_add():
    name = request.form.get('name', '', type=str)
    if not name:
        return jsonify({'code':-1, 'msg':'请填写标题'})
    tag = Tag(name=name)
    res = tag.save()
    return jsonify(res)

@admin.route('/tag/<tag_id>/edit', methods=['GET','POST'])
@require_login
def tag_edit(tag_id):
    tag_info = Tag.findOne('id=?', [tag_id])
    if request.method == 'POST':
        tag = Tag(__data__=tag_info)
        name = request.form.get('name', '', type=str)
        if name:
            tag.name = name
        else:
            return jsonify({'code':-1, 'msg':'请填写标题'})
        res = tag.update(tag_info)
        return jsonify(res);
    return render_template('admin/modal.html',
                            title='编辑标签',
                            forms=[ {'type':'text','name':'name', 'value':tag_info['name']}, ],
                            action=url_for('admin.tag_edit', tag_id=tag_id));

@admin.route('/tag/del/<tag_id>', methods=['GET','POST'])
@require_login
def tag_del(tag_id):
    if request.method == 'POST':
        res = Tag.removeById(tag_id)
        return jsonify(res)
    return render_template('admin/modal.html',
                            title='删除标签',
                            forms=[ {'type':'msg','content':'确定要删除标签吗？', 'class':'text-danger'}],
                            action=url_for('admin.tag_del', tag_id=tag_id));


@admin.route('/tag/search/<keyword>')
@require_login
def tag_search(keyword):
    res = search_list(g.tags, 'name', keyword)
    if res:
        return jsonify({'code':1, 'data':res})
    return jsonify({'code':-1})


# Account
@admin.route('/account', methods=['GET', 'POST'])
@require_login
def account():
    if request.method == 'POST':
        admin = Admin(__data__=session['admin'])
        print(admin)
        old_password = request.form.get('old_password', '', type=str)
        if not old_password:
            return jsonify({'code':-1, 'msg':'请填写原密码'})
        elif not Admin.check_pwd(old_password, admin['password']):
            return jsonify({'code':-1, 'msg':'原密码不正确'})

        new_password = request.form.get('new_password', '', type=str)
        if not new_password:
            return jsonify({'code':-1, 'msg':'请填写新密码'})

        new_password_2 = request.form.get('new_password_2', '', type=str)
        if not new_password_2:
            return jsonify({'code':-1, 'msg':'请确认新密码'})

        if new_password != new_password_2:
            return jsonify({'code':-1, 'msg':'两次输入的密码不一致！'})
        else:
            admin.password = Admin.encrypt_pwd(new_password)
        res = admin.update()
        session.pop('admin', None)
        return jsonify(res)
    return render_template('admin/account.html',
                            username=session['admin']['username'])


