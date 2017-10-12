from ..orm import Model, IntegerField, StringField, BooleanField, TextField
from ..helpers import CacheFile
import time

class Archive(Model):
    __table__ = 'archive'

    id = IntegerField(primary_key=True)
    month = StringField(ddl='char(6)')
    num = IntegerField()
    addtime = IntegerField(default=int(time.time()))

    @classmethod
    def inc_num(cls, month):
        t = cls.findOne('month=?', [month])
        if t:
            archive = Archive(__data__=t)
            archive.num = archive.num + 1
            archive.update()
        else: 
            archive = Archive(month=month, num=1)
            archive.save()

    @classmethod
    def dec_num(cls, month):
        t = cls.findOne('month=?', [month])
        archive = Archive(__data__=t)
        archive.num = archive.num - 1
        if archive.num == 0:
            archive.remove()
        else:
            archive.update()


