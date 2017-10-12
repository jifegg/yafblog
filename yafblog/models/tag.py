from ..orm import Model, IntegerField, StringField, BooleanField, TextField
from ..helpers import CacheFile
import time

class Tag(Model):
    __table__ = 'tag'

    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')
    num = IntegerField()
    addtime = IntegerField()

    @classmethod
    def inc_num(cls, tag_id):
        t = cls.findOne('id=?', [tag_id])
        tag = Tag(__data__=t)
        tag.num = tag.num + 1
        tag.update()

    @classmethod
    def dec_num(cls, tag_id):
        t = cls.findOne('id=?', [tag_id])
        tag = Tag(__data__=t)
        tag.num = tag.num - 1
        if tag.num == 0:
            tag.remove()
        else:
            tag.update()

    @classmethod
    def cache(cls):
        res = cls.findAll()
        tag_cache = CacheFile('tag', 'json')
        tag_cache.write(res)

    def save(self):
        has_one = Tag.findOne('name=?', [self.name])
        if has_one:
            return {'code':-1, 'msg':'标签已存在'}
        self.addtime = int(time.time())
        res = super().save()
        if res['code'] :
            Tag.cache()
        return res


    @classmethod
    def removeById(cls, tag_id):
        tag_info = Tag.findOne('id=?', [tag_id])
        if not tag_info:
            return {'code':-1, 'msg':'标签不存在或已删除'}

        if tag_info['num'] > 0:
            return {'code':-1, 'msg':'不能删除已使用的标签'}

        tag = Tag(__data__=tag_info)
        res = tag.remove()
        if res['code'] :
            Tag.cache()
        return res

    def update(self, old = None):
        if old and self.name != old['name']:
            has_one = Tag.findOne('name=?', [self.name])
            if has_one:
                return {'code':-1, 'msg':'标签已存在'}
        res = super().update()
        if res['code'] :
            Tag.cache()
        return res
