import pymysql
from yafblog import logger

class DB(object):
    def __init__(self, config):
        self.config = config
        self.con = None

    def connect(self):
        self.con = pymysql.connect(host=self.config['HOST'],
                                     user=self.config['USER'],
                                     password=self.config['PASSWORD'],
                                     db=self.config['DB'],
                                     charset=self.config['CHARSET'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql, args):
        if self.con == None :
            self.connect()
            logger.info('connect db')
        try:
            logger.info('sql: %s\nargs: %s',sql,args)
            with self.con.cursor() as cursor:
                cursor.execute(sql.replace('?', '%s'), args)
            #self.con.commit()
            return cursor
        except Exception as err:
            logger.debug(err)
        finally:
            logger.info('finish sql')

    def select(self, sql, args):
        cursor = self.query(sql, args)
        if cursor :
            result = cursor.fetchall()
        else :
            result = []
        return result

    def execute(self, sql, args):
        cursor = self.query(sql, args)
        if cursor :
            return {'code':1, 'num':cursor.rowcount, 'last_id':cursor.lastrowid}
        return {'code':0}

    def close(self):
        if self.con != None:
            self.con.close()
            self.con = None

