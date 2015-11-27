__author__ = 'Fujitsu'
from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    Posiljatelj = ndb.StringProperty()
    Naslovnik = ndb.StringProperty()
    Message = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
