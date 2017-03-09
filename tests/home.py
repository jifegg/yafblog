import os
from yafblog import yafblog
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd,tmp = tempfile.mkstemp()
        yafblog.app.config['DB'] = yafblog.app.config['DB']+'_test'
        yafblog.app.config['TESTING'] = True
        self.app = yafblog.app.test_client()
        with yafblog.app.app_context():
            yafblog.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        #os.unlink(yafblog.app.config['DATABASE'])
        with yafblog.app.app_context():
            yafblog.close_test_db()

if __name__ == '__main__':
    unittest.main()
