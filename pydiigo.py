# -*- coding: utf8 -*-

import urllib
import httplib
import simplejson
from base64 import b64encode

DEBUG = True

def parametalize(params_candidate={}) :
  if params_candidate.has_key('self') :
    del params_candidate['self']
  return set_data(params_candidate)

def set_data(params_candidate) :
  param = {}
  for key, value in params_candidate.iteritems() :
    if value == None or value == '' or value == []:
      pass
    else:
        param[key] = value
  return param

class DiigoBookmark(dict) :
  """
  Diigo Bookmark model.
  "title":"Diigo API Help",
  "url":"http:\/\/www.diigo.com\/help\/api.html",
  "user":"foo",
  "desc":"",
  "tags":"test,diigo help",
  "shared":"yes",
  "created_at":"2008/04/30 06:28:54 +0800",
  "updated_at":"2008/04/30 06:28:54 +0800",
  "comments":[],
  "annotations":[]
  """
  def __init__(self, d) :
    for key, value in d.iteritems() :
      self[key] = value

  def __getattr__(self, name):
    try: return self[name]
    except: object.__getattribute__(self, name)

class DiigoApi(object) :
  """
  Requirements
  =======================
  * `simplejson`_
  * `pit`_ **optional**. See diigotest.py. You might love it ;)

  .. _`simplejson`: http://pypi.python.org/pypi?:action=display&name=simplejson
  .. _`pit`: http://pypi.python.org/pypi?:action=display&name=pit

  instllation
  =======================
  $ sudo easy_install pydiigo

    or 

  Download pydiigo and extract it, then

  $ sudo python setup.py install

  Notes
  =======================
  You might get 503 Error, because of Diigo's API limit.

  Usage
  =======================

  Initialize API 
  --------------------
  ::

    >>> from pydiigo import DiigoApi
    >>> api = DiigoApi(user='YOUR_DIIGO_USERNAME', password='YOUR_DIIGO_PASSWORD')

  Search Bookmarks
  --------------------
  ::

    >>> bookmarks = api.bookmarks_find(users='DIIGO_USER_NAME')
    >>> for bookmark in bookmarks:
    ...   print bookmark.title
    ...   print bookmark.url
    ...   print bookmark.tags
    ...   print bookmark.desc
    ...   print '-' * 10

  * Bookmark Structure

    * title (string)

    * url (string)

    * user (string)

    * desc (string: description)

    * tags (string: Seperated by comma with multiple tags.)

    * shared (string: yes or no)

    * created_at (string: eg.2009/03/04 02:57:09 +0000)

    * updated_at (string: eg.2009/03/04 02:57:09 +0000)

    * comments (string array)

    * annotations (string array)

  Add Bookmark
  --------------------
  ::

    >>> result = api.bookmark_add(title='', description='',url='', shared='yes', tags='')
    >>> print result['message']
    added 1 bookmark

  * required arguments

    * url

  Update Bookmark
  --------------------
  ::

    >>> result = api.bookmark_update(title='', description='',url='', shared='yes', tags='')
    >>> print result['message']
    updated 1 bookmark

  * required arguments

    * url

  Delete Bookmark
  --------------------
  ::

    >>> result = api.bookmark_delete(url='')
    >>> print result['message']
    updated 1 bookmark

  * required arguments

    * url

  """
  user = ''
  password = ''
  server = 'api2.diigo.com:80'
  
  def __init__(self, user='', password='') :
    self.user = user
    self.password = password
    if not self.user:
      raise ValueError, 'You must pass your username and password.'
    self.headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept"      : "text/plain",
               "Authorization": "Basic %s==" % b64encode("%s:%s" % (self.user, self.password)),
               "User-agent"  : "pydiigo/%s" % (VERSION)}

  def bookmarks_find(self, start=0, rows=50, sort=0,
                           users=None, tags='', filter='public',
                           list=None, site=None,
                           ft=None, url=None) :
    return self._handle_bookmark(parametalize(locals()), 'GET')

  def bookmark_add(self, title='', description='',url='',
                         shared='yes', tags=''):
    if url == None or len(url) == 0:
      raise ValueError, 'url must specified'
    return self._handle_bookmark(parametalize(locals()), 'POST')

  def bookmark_update(self, title='', description='',url='',
                         shared='yes', tags=''):
    if url == None or len(url) == 0:
      raise ValueError, 'url must specified'
    return self._handle_bookmark(parametalize(locals()), 'PUT')

  def bookmark_delete(self, url=''):
    if url == None or len(url) == 0:
      raise ValueError, 'url must specified'
    return self._handle_bookmark(parametalize(locals()), 'DELETE')
  
  def _handle_bookmark(self, param={}, method='GET') :
    if DEBUG :
      print 'DEBUG: %s._handle_bookmark->%s' % (self.__class__, method)
      print '     :%s' % (param)
      print ''
    params = urllib.urlencode(param)
    conn = httplib.HTTPConnection(self.server)
    try:
      if method == 'GET':
        conn.request(method, "/bookmarks?%s" % params, {}, self.headers)
        response = conn.getresponse()
        bookmarks = [DiigoBookmark(d) for d in simplejson.load(response)]
        return bookmarks
      else :
        conn.request(method, "/bookmarks" , params, self.headers)
        response = conn.getresponse()
        if response.status >= 400:
          if DEBUG:
            print response.read()
          raise PyDiigoError(response.status,
                            '',
                            method,
                            params)
        result = simplejson.load(response)
        if DEBUG:
            print result
        return result
    finally:
      conn.close()

class PyDiigoError(Exception) :
  STATUS = {'301':'Not Modified',
                '400':'Bad Request',
                '401':'Not Authorized',
                '403':'Forbidden',
                '404':'Not Found',
                '500':'Internal Server Error',
                '502':'Bad Gateway',
                '503':'Service Unavailable'}
  def __init__(self, status, message, method='', param={}):
    self.status = status
    self.message = message
    self.method = method
    self.param = param

  def __str__(self) :
    return self.__repr__()

  def __repr__(self) :
    return '[%s:%s] %s when %s called with %s' % (self.status, PyDiigoError.STATUS[str(self.status)],
                                                  self.message, self.method, self.param)


VERSION = '0.1'
AUTHOR = 'makoto tsuyuki'
AUTHOR_EMAIL = 'mtsuyuki_at_gmail_dot_com'
PROJECT_URL = 'http://www.tsuyukimakoto.com/project/pydiigo/'

CONTACT = '%s or %s' % (PROJECT_URL, AUTHOR_EMAIL)
DESCRIPTION = '''Python wrapper for www.diigo.com's API'''
LONG_DESCRIPTION = DiigoApi.__doc__



