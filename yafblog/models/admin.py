from ..orm import Model, IntegerField, StringField, BooleanField, TextField
import time
from hashlib import md5

class Admin(Model):
    __table__ = 'admin'

    id = IntegerField(primary_key=True)
    username = StringField(ddl='varchar(50)')
    password = StringField(ddl='char(32)')
    addtime = IntegerField(default=int(time.time()))

    @classmethod
    def login(cls, username, password):
        info = Admin.findOne('username=?', [username])
        if  info :
            password = md5(password.encode('utf-8')).hexdigest()
            if password == info['password']:
                return {'code':1, 'info':info}
        return {'code':-1, 'msg':'用户不存在或密码错误'}

