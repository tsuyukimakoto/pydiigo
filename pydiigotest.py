# -*- coding: utf-8 -*-

##
# License: bsd license. 
# See 'license.txt' for more informations.
#       

import unittest
from pydiigo import *
import time
import logging

class TestUtilityFunction(unittest.TestCase):

  def test_set_data_1(self):
    d = {'a': None, 'str': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assertEqual(False, 'a' in param)
    self.assertTrue('str' in param)
    self.assertEqual(False, 'empty_str' in param)
    self.assertTrue('lst' in param)
    self.assertEqual(False, 'empty_lst' in param)

  def test_set_data_self(self) :
    d = {'a': None, 'self': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assertEqual(False, 'a' in param)
    self.assertEqual(False, 'self' in param)
    self.assertTrue('lst' in param)

class TestApi(unittest.TestCase) :

  def setUp(self) :
    diigo_user = '' 
    diigo_password = ''
    diigo_apikey = ''  # https://www.diigo.com/api_keys/new/
    if not diigo_user:
      try :
        # http://pypi.python.org/pypi/pit/0.3
        # http://www.youtube.com/watch?v=VeqYJXCm3Dw&eurl=http://d.hatena.ne.jp/a2c/20081016/1224097042&feature=player_embedded
        from pit import Pit
        diigo_config = Pit.get('diigo.com',
            {'require' : {'username':'Your diigo username',
                        'password':'Your diigo password',
                        'apikey': 'Your diigo api key(https://www.diigo.com/api_keys/new/)'}})
        diigo_user, diigo_password, diigo_apikey = diigo_config['username'],diigo_config['password'],diigo_config['apikey']
      except ImportError: pass
    self.api = DiigoApi(diigo_user, diigo_password, diigo_apikey, debug=True)
    try:
      self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    except PyDiigoError:pass

  def test_crud(self):
    result = self.api.bookmark_add(title='tsuyukimakoto',description='some description.日本語', url='http://www.tsuyukimakoto.com/', tags='pydiigotest')
    self.assert_(result['message'] == 'Saved 1 bookmark(s)')
    bookmarks = self.api.bookmarks_find(users='tsuyukimakoto', rows=1)
    self.assertEqual(1, len(bookmarks))
    bookmark = bookmarks[0]
    self.assertEqual('tsuyukimakoto', bookmark.title)
    self.assertEqual('http://www.tsuyukimakoto.com', bookmark.url)
    self.assertEqual('pydiigotest', bookmark.tags)
    if sys.version_info[0] == 2:
        self.assertEqual('some description.日本語'.decode('utf8'), bookmark.desc)
    else:
        self.assertEqual('some description.日本語', bookmark.desc)
    time.sleep(5)
    bookmark = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')[0]
    self.assertEqual('pydiigotest', bookmark.tags)
    try:
      result = self.api.bookmark_update(title='testtest', url='http://www.tsuyukimakoto.com/', tags='test,django,python')
      fail()
    except DeprecationWarning:
      pass
    result = self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    self.assertEqual('deleted 1 bookmark(s)', result['message'])
    bookmarks = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')
    self.assertEqual(0, len(bookmarks))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
