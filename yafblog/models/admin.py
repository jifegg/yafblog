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
        if info and cls.check_pwd(password, info['password']):
            return {'code':1, 'info':info}
        return {'code':-1, 'msg':'用户不存在或密码错误'}

    @classmethod
    def check_pwd(cls, pwd, encrypt_pwd):
        return encrypt_pwd == cls.encrypt_pwd(pwd)

    @classmethod
    def encrypt_pwd(cls, pwd):
        return md5(pwd.encode('utf-8')).hexdigest()

