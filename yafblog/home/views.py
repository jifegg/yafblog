from functools import wraps
from flask import Blueprint, render_template, g, url_for, abort,request, Response
from ..models.article import Article
from ..models.category import Category
from ..models.tag import Tag
from ..models.archive import Archive
from ..helpers import CacheFile,find_dict_in_list,pages
home = Blueprint('home', __name__, template_folder='templates',static_folder='static', static_url_path='/home/static')

def article_page(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.article_num = Article.count()
        g.limit = ((g.page - 1) * g.per_page, g.per_page)
        return f(*args, **kwargs)
    return decorated_function

@home.route('/')
@article_page
def index():
    archives = Archive.findAll()
    articles = Article.findAll(None,orderBy='addtime DESC',limit=g.limit)
    page_list = pages(g.page, g.article_num, g.per_page,  url_for('home.index'))
    return render_template('home/index.html',
                            articles=articles,
                            categorys=g.categorys,
                            tags=g.tags,
                            archives=archives,
                            page_name='home',
                            page_list=page_list)

@home.route('/category')
def category():
    return render_template('home/cloud.html', categorys=g.categorys, page_name='category')

@home.route('/category/<category_id>')
@article_page
def index_category(category_id):
    archives = Archive.findAll()
    category = find_dict_in_list(g.categorys, 'id', category_id)
    if not category:
        abort(404)
    articles = Article.findAll('category=?',[category_id],limit=g.limit)
    page_list = pages(g.page, g.article_num, g.per_page,  url_for('home.index_category', category_id=category_id))
    return render_template('home/index.html',
                            articles=articles,
                            categorys=g.categorys,
                            category_id=category_id,
                            tags=g.tags,
                            archives=archives,
                            page_list=page_list)

@home.route('/tag')
def tag():
    return render_template('home/cloud.html', tags=g.tags, page_name='tag')

@home.route('/tag/<tag_id>')
@article_page
def index_tag(tag_id):
    archives = Archive.findAll()
    tag = find_dict_in_list(g.tags, 'id', tag_id)
    if not tag:
        abort(404)
    articles = Article.findAllByTag(tag_id, limit=g.limit)
    page_list = pages(g.page, g.article_num, g.per_page,  url_for('home.index_tag', tag_id=tag_id))
    return render_template('home/index.html', 
                            articles=articles,
                            categorys=g.categorys, 
                            tag_id=tag_id,
                            tags=g.tags,
                            archives=archives,
                            page_list=page_list)

@home.route('/archive')
def archive():
    archives = Archive.findAll()
    return render_template('home/cloud.html', archives=archives)

@home.route('/archive/<month>')
@article_page
def index_archive(month):
    archives = Archive.findAll()
    archive = find_dict_in_list(archives, 'month', month)
    if not archive:
        abort(404)
    articles = Article.findAll('archive=?', [month], limit=g.limit)
    page_list = pages(g.page, g.article_num, g.per_page,  url_for('home.index_archive', month=month))
    return render_template('home/index.html', 
                            articles=articles,
                            categorys=g.categorys,
                            month=month,
                            tags=g.tags,
                            archives=archives,
                            page_list=page_list)

@home.route('/article/<article_id>')
def article(article_id):
    article = Article.findOne('id=?', [article_id])
    if not article :
        abort(404)

    article['tags'] = article['tags'].split(',')
    return render_template('home/article.html', article=article, categorys=g.categorys, tags=g.tags)

@home.route('/article/<article_id>/raw')
def article_raw(article_id):
    article = Article.findOne('id=?', [article_id])
    if not article :
        abort(404)
    return Response('##'+article['title']+'\n\n'+article['content'], content_type='text/plain; charset=utf-8')

@home.route('/search/<keyword>')
def search(keyword):
    if not keyword:
         redirect(url_for('home.index'))
    articles = Article.findAll('title LIKE ?', ['%'+keyword+'%'])
    return render_template('home/index.html', articles=articles,keyword=keyword, categorys=g.categorys, tags=g.tags)

@home.route('/test')
def test():
    Tag.cache()
    Category.cache()
    return 'ok'



