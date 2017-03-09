from yafblog import logger,db

class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0, ddl='int'):
        super().__init__(name, ddl, primary_key, default)

class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

def create_return_val(rs, ret_type, ret_key):
    if (ret_type == 'dict'):
        d = {}
        for r in rs:
            d[r[ret_key]] = r
        return d
    return rs
    

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        #logger.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                #logger.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s) values (%s)' % (tableName, ', '.join(escaped_fields), create_args_string(len(escaped_fields)))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        __data__ = kw.get('__data__', None)
        if __data__:
            for k, v in __data__.items():
                setattr(self, k, v)
            self.pop('__data__')

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logger.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = db.select(' '.join(sql), args)
        ret_type =  kw.get('ret_type', None)
        ret_key =  kw.get('ret_key', 'id')
        return create_return_val(rs, ret_type, ret_key)

    @classmethod
    def count(cls, where=None, args=None):
        ' find number by select and where. '
        sql = ['SELECT COUNT(*) AS COUNT FROM `%s`' % (cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = db.select(' '.join(sql), args)
        return rs[0]['COUNT']

    @classmethod
    def findOne(cls, where=None, args=None, **kw):
        rs = cls.findAll(where, args, limit=1, **kw)
        if rs :
            return rs[0]
        return {}

    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        res = db.execute(self.__insert__, args)
        if not res['code']:
            logger.warn('failed to insert record')
        return res

    def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        res = db.execute(self.__update__, args)
        return res

    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        res = db.execute(self.__delete__, args)
        if not res['code']:
            logger.warn('failed to remove by primary key')
        return res
