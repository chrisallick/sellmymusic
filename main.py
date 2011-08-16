#!/usr/bin/env python

#import json
#import urllib2
#import re
#import sys
import os
#import wsgiref.handlers
import logging
import datetime

#from utils.jsonproperty import JSONProperty

from google.appengine.ext import webapp
from google.appengine.ext import db

from google.appengine.api import users

from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


class Album(db.Model):
	thumb = db.StringProperty(multiline=False)
	image = db.StringProperty(multiline=False)
	description = db.TextProperty()
	title = db.StringProperty(multiline=False)
	sub_title = db.StringProperty(multiline=False)
	price = db.FloatProperty()
	tracks = db.StringListProperty()
	id_ref = db.StringProperty(multiline=False)
	created = db.DateProperty(auto_now_add=True)

	def save(self):
		try:
			obj_id = self.key().id()
			resave = False
		except db.NotSavedError:
			resave = True

		self.put()
		if resave:
			self.id_ref = self.key().id()
			self.put()

	def get(cls, id_ref):
		q = db.Query(Album)
		q.filter('id_ref = ', id_ref)
		return q.get()

class Albums(object):
	def retreive( self, last_id_ref=0, max_return=25):
		query = Album.all().filter("id_ref > ", last_id_ref).fetch(max_return)

		return query

	def remove( self, id_ref=None ):
		if id_ref:
			album = Album.get(id_ref)
			if album:
				db.delete(album)
				return True
			else:
				return False


class MainHandler(webapp.RequestHandler):
	def get(self):
		last_id_ref = self.request.get("last_id_ref")
		a = Albums()
		albums = a.retreive(last_id_ref=last_id_ref)

		template_values = {
			'albums': albums
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_values))

class AdminHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("Hello admin!")

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/admin', AdminHandler)
	], debug=True)

	util.run_wsgi_app(application)


if __name__ == '__main__':
	logger = logging.getLogger("main_logger")
	logger.setLevel(logging.DEBUG)

	main()