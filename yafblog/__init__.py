import os
from flask import Flask, Blueprint, request, session, g, redirect, url_for, abort, render_template, flash
from .config import configure_app
from .helpers import datetimeformat, list_to_dict, CacheFile, num_to_date

app = Flask(__name__)
configure_app(app)
logger = app.logger;
if app.config['DEBUG'] :
    logger.setLevel('DEBUG')

from .db import DB
db = DB(app.config)

from .admin.views import admin
app.register_blueprint(admin)

from .home.views import home
app.register_blueprint(home)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['list_to_dict'] = list_to_dict
app.jinja_env.filters['split'] = lambda x,y:x.split(y)
app.jinja_env.filters['num_to_date'] = num_to_date

@app.before_request
def cache_file():
    cat_cache = CacheFile('category', 'json')
    g.categorys = cat_cache.read()

    tag_cache = CacheFile('tag', 'json')
    g.tags = tag_cache.read()
    g.page = int(request.args.get('page', 1))
    if g.page < 0 :
        g.page = 1
    g.per_page = 12

@app.teardown_appcontext
def close(error):
    db.close()

def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        db.execute(f.read(), [])

def close_test_db():
    db.execute('DROP DATABASE `'+app.config['DB']+'`;CREATE DATABASE `'+app.config['DB']+'` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;')

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('home/500.html'), 500

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('home/403.html'), 403
