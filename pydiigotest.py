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
        # http://pypi.python.org/pypi/pit/0.2
        # http://www.youtube.com/watch?v=VeqYJXCm3Dw&eurl=http://d.hatena.ne.jp/a2c/20081016/1224097042&feature=player_embedded
        from pit import Pit
        diigo_config = Pit.get('diigo.com',{'require' : {'username':'Your diigo username','password':'Your diigo password'}})
        diigo_user, diigo_password = diigo_config['username'],diigo_config['password']
      except ImportError: pass
    self.api = DiigoApi(diigo_user, diigo_password)
    try:
      self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    except PyDiigoError:pass

  def test_crud(self):
    time.sleep(60)
    result = self.api.bookmark_add(title='tsuyukimakoto.com',url='http://www.tsuyukimakoto.com/', tags='pydiigotest')
    self.assert_(result['message'] == 'added 1 bookmarks')
    time.sleep(60)
    bookmark = self.api.bookmarks_find(url='http://www.tsuyukimakoto.com', users='tsuyukimakoto')[0]
    self.assert_(bookmark.title == 'tsuyukimakoto.com')
    self.assert_(bookmark.url == 'http://www.tsuyukimakoto.com')
    self.assert_(bookmark.tags == 'pydiigotest')
    time.sleep(60)
    bookmark = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')[0]
    self.assert_(bookmark.tags == 'pydiigotest')
    time.sleep(60)
    result = self.api.bookmark_update(title='was spam-ish', url='http://www.tsuyukimakoto.com/', tags='test,django,python')
    self.assert_(result['message'] == 'updated 1 bookmarks')
    time.sleep(60)
    bookmark = self.api.bookmarks_find(url='http://www.tsuyukimakoto.com/', users='tsuyukimakoto')[0]
    self.assert_(bookmark.title == 'was spam-ish')
    self.assert_(bookmark.url == 'http://www.tsuyukimakoto.com')
    self.assert_(bookmark.tags == 'test,django,python')
    time.sleep(60)
    result = self.api.bookmark_delete(url='http://www.tsuyukimakoto.com/')
    self.assert_(result['message'] == 'deleted 1 bookmarks')
    time.sleep(60)
    bookmarks = self.api.bookmarks_find(tags='pydiigotest', users='tsuyukimakoto')
    print 'length:%s' % len(bookmarks)
    for b in bookmarks:
        print b
    self.assert_(len(bookmarks) == 0)

if __name__ == '__main__':
    unittest.main()
