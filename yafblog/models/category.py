from ..orm import Model, IntegerField, StringField, BooleanField, TextField
from ..helpers import CacheFile
import time

class Category(Model):
    __table__ = 'category'

    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')
    num = IntegerField()
    addtime = IntegerField()

    def update(self):
        res = super().update()
        if res['code'] :
            self.cache()
        return res

    @classmethod
    def inc_num(cls, category_id):
        t = cls.findOne('id=?', [category_id])
        category = Category(__data__=t)
        category.num = category.num + 1
        category.update()

    @classmethod
    def dec_num(cls, category_id):
        t = cls.findOne('id=?', [category_id])
        category = Category(__data__=t)
        category.num = category.num - 1
        if category.num == 0:
            category.remove()
        else:
            category.update()

    @classmethod
    def cache(cls):
        res = cls.findAll()
        cat_cache = CacheFile('category', 'json')
        cat_cache.write(res)

    def save(self):
        has_one = Category.findOne('name=?', [self.name])
        if has_one:
            return {'code':-1, 'msg':'类别已存在'}
        self.addtime = int(time.time())
        res = super().save()
        if res['code'] :
            Category.cache()
        return res
        
    def update(self, old = None):
        if old and self.name != old['name']:
            has_one = Category.findOne('name=?', [self.name])
            if has_one:
                return {'code':-1, 'msg':'类别已存在'}
        res = super().update()
        if res['code'] :
            Category.cache()
        return res
        
    @classmethod
    def removeById(cls, category_id):
        category_info = Category.findOne('id=?', [category_id])
        if not category_info:
            return {'code':-1, 'msg':'类别不存在或已删除'}

        if category_info['num'] > 0:
            return {'code':-1, 'msg':'不能删除已使用的类别'}

        category = Category(__data__=category_info)
        res = category.remove()
        if res['code'] :
            Category.cache()
        return res
