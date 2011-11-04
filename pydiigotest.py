# -*- coding: utf-8 -*-

##
# License: bsd license. 
# See 'license.txt' for more informations.
#       

import unittest
from pydiigo import *
import time

class TestUtilityFunction(unittest.TestCase):

  def test_set_data_1(self):
    d = {'a': None, 'str': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assert_(param.has_key('a') == False)
    self.assert_(param.has_key('str'))
    self.assert_(param.has_key('empty_str') == False)
    self.assert_(param.has_key('lst'))
    self.assert_(param.has_key('empty_lst') == False)

  def test_set_data_self(self) :
    d = {'a': None, 'self': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assert_(param.has_key('a') == False)
    self.assert_(param.has_key('self') == False)
    self.assert_(param.has_key('lst'))

class TestApi(unittest.TestCase) :

  def setUp(self) :
    diigo_user = None 
    diigo_password = None
    if not diigo_user:
      try :
        # http://pypi.python.org/pypi/pit/0.3
        # http://www.youtube.com/watch?v=VeqYJXCm3Dw&eurl=http://d.hatena.ne.jp/a2c/20081016/1224097042&feature=player_embedded
        from pit import Pit
        diigo_config = Pit.get('diigo.com',{'require' : {'username':'Your diigo username','password':'Your diigo password'}})
        diigo_user, diigo_password = diigo_config['username'],diigo_config['password']
      except ImportError: pass
    self.api = DiigoApi(diigo_user, diigo_password, debug=True)
    try:
      self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    except PyDiigoError:pass

  def test_crud(self):
    result = self.api.bookmark_add(title='tsuyukimakoto',description='some description', url='http://www.tsuyukimakoto.com/', tags='pydiigotest')
    self.assert_(result['message'] == 'Saved 1 bookmark(s)')
    bookmark = self.api.bookmarks_find(url='http://www.tsuyukimakoto.com', users='tsuyukimakoto')[0]
    self.assert_(bookmark.title == 'tsuyukimakoto')
    self.assert_(bookmark.url == 'http://www.tsuyukimakoto.com')
    self.assert_(bookmark.tags == 'pydiigotest')
    self.assert_(bookmark.desc == 'some description')
    time.sleep(5)
    bookmark = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')[0]
    self.assert_(bookmark.tags == 'pydiigotest')
    try:
      result = self.api.bookmark_update(title='testtest', url='http://www.tsuyukimakoto.com/', tags='test,django,python')
      fail()
    except DeprecationWarning:
      pass
    result = self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    self.assert_(result['message'] == 'deleted 1 bookmark(s)')
    bookmarks = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')
    self.assert_(len(bookmarks) == 0)

if __name__ == '__main__':
    unittest.main()
