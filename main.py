#!/usr/bin/env python

#import json
#import urllib2
#import re
#import sys
#import os
#import wsgiref.handlers
import logging

#from utils.jsonproperty import JSONProperty

from google.appengine.ext import webapp
#from google.appengine import users
#from google.appengine import db
from google.appengine.ext.webapp import util
#from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("Hello world!")

class AdminHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("Hello admin!")

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),('/admin', AdminHandler)
	], debug=True)

	util.run_wsgi_app(application)


if __name__ == '__main__':
	logger = logging.getLogger("main_logger")
	logger.setLevel(logging.DEBUG)

	main()