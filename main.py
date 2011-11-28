#!/usr/bin/env python

import json
#import urllib2
#import re
#import sys
import os
#import wsgiref.handlers
import logging
import datetime

from utils.jsonproperty import JSONProperty

from google.appengine.ext import webapp
from google.appengine.ext import db

from google.appengine.api import users

from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


class Album(db.Model):
	#thumb = db.StringProperty(multiline=False)
	image = db.StringProperty(multiline=False)
	data = JSONProperty()
	#id_ref = db.StringProperty(multiline=False)
	#created = db.DateProperty(auto_now_add=True)

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
		user = users.get_current_user()
		if users.is_current_user_admin():
			logout_url = users.create_logout_url("/")
			a = Albums()
			albums = a.retreive( last_id_ref=0, max_return=500 )
			
			template_values = {
				'albums': albums,
				'logout_url': logout_url
			}

			path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
			self.response.out.write(template.render(path, template_values))

class UploadHandler(webapp.RequestHandler):
	def post(self):
		file_path = "/Users/chrisallick/Documents/PYTHON/AppEngine/sellmymusic/img/albums/"
		logger.info( self.request )
		# fileupload = self.request.POST.get("file", None)

		# if fileupload:
		# 	logger.info("got it")
		# 	file_name = fileupload.filename

		# 	try:
		# 		f = open( file_path+file_name, 'w' )
		# 		f.write( fileupload.file.read() )
		# 	except IOError:
		# 		print "IOError"
		# 	else:
		# 		f.close()
		self.response.out.write("success")

class AddHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		#if user.nickname() == "test@example.com":
		if users.is_current_user_admin():
			logout_url = users.create_logout_url("/")

			template_values = {
				'logout_url': logout_url
			}			

			path = os.path.join(os.path.dirname(__file__), 'templates/add.html')
			self.response.out.write(template.render(path, template_values))

	def post(self):
		if users.is_current_user_admin():
			logger.info( self.request )
			album = self.request.get('album', None)
			if album:
				album = json.loads(album)
				a = Album(data=album)
				a.put()
				albums = Album.all()
				albums = albums.fetch(10)
				for a in albums:
					logging.info( a.data )
				self.response.out.write( json.dumps({'msg': 'success'}) );
			else:
				self.response.out.write( json.dumps({'msg': 'error'}) );
		else:
			self.response.out.write( json.dumps({'msg': 'error'}) );

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/admin', AdminHandler),
		('/add', AddHandler),
		('/upload', UploadHandler)
	], debug=True)

	util.run_wsgi_app(application)


if __name__ == '__main__':
	logger = logging.getLogger("main_logger")
	logger.setLevel(logging.DEBUG)

	main()