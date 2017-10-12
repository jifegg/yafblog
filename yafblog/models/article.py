from ..orm import Model, IntegerField, StringField, BooleanField, TextField
import mistune
from ..lib.myrenderer import MyRenderer
import time
from ..models.category import Category
from ..models.tag import Tag
from ..models.archive import Archive
class Article(Model):
    __table__ = 'article'

    id = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    content = TextField()
    content_html = TextField()
    toc_html = TextField()
    category = IntegerField()
    tags = StringField(ddl='varchar(50)')
    archive = StringField(ddl='char(6)')
    addtime = IntegerField()

    @classmethod
    def findAllByTag(cls, tag, **kw):
        return cls.findAll('CONCAT(",",tags,",") LIKE ?', ['%,'+str(tag)+',%'], **kw)

    
    def save(self):
        article_info = Article.findOne('title=?', [self.title])
        if article_info:
            return {'code':-1, 'msg':'该文章标题已存在'}
        self.archive = time.strftime('%Y%m')
        self.addtime = int(time.time())
        my_render = MyRenderer()
        my_render.reset_toc()
        markdown = mistune.Markdown(renderer=my_render)
        self.content_html = markdown(self.content)
        self.toc_html = my_render.render_toc(level=3)

        # category
        Category.inc_num(self.category)

        # tag
        for tag_id in self.tags:
            Tag.inc_num(tag_id)
        if self.tags:
            self.tags = ','.join(self.tags)

        # archive
        archive = str(time.strftime('%Y%m'))
        Archive.inc_num(archive)
        return super().save()

    def update(self, old):
        if self.title != old['title']:
            article_info = Article.findOne('title=?', [self.title])
            if article_info:
                return {'code':-1, 'msg':'该文章标题已存在'}
        my_render = MyRenderer()
        my_render.reset_toc()
        markdown = mistune.Markdown(renderer=my_render)
        self.content_html = markdown(self.content)
        self.toc_html = my_render.render_toc(level=3)

        # category
        if (self.category != old['category']):
            Category.dec_num(old['category'])
            Category.inc_num(self.category)

        # tag
        old['tags'] = old['tags'].split(',');
        for tag_id in set(old['tags']) - set(self.tags):
            if tag_id:
                Tag.dec_num(tag_id)
        for tag_id in set(self.tags) - set(old['tags']):
            if tag_id:
                Tag.inc_num(tag_id)
        if self.tags:
            self.tags = ','.join(self.tags)
        else:
            self.tags = ''

        res = super().update()
        return res

    @classmethod
    def removeById(cls, article_id):
        article_info = Article.findOne('id=?', [article_id])
        if not article_info:
            return {'code':-1, 'msg':'文章不存在或已删除'}
        article = Article(__data__=article_info)

        # category
        Category.dec_num(article.category)

        # tag
        if article.tags:
            for tag_id in article.tags.split(','):
                Tag.dec_num(tag_id)

        # archive
        Archive.dec_num(article.archive)

        res = article.remove()
        return res
