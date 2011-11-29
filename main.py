#!/usr/bin/env python

import json
import os.path
import logging

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

##########   /*     */   ##########


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/add", AddHandler),
            (r"/admin", AdminHandler),
            (r"/auth/login", AuthHandler),
            (r"/auth/logout", LogoutHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        else:
            return tornado.escape.json_decode(user_json)

##########   /*     */   ##########


class AuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


##########   /*     */   ##########


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class AdminHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("admin.html")

class AddHandler(tornado.web.RequestHandler):
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
				sleeve = self.request.get("sleeve")
				thumb = self.request.get("thumb")
				extra = self.request.get("extra")
				a = Album(data=album, sleeve=db.Blob(sleeve), thumb=db.Blob(thumb), extra=db.Blob(extra))
				a.put()
				#self.response.out.write( json.dumps({'msg': 'success'}) );
				self.redirect('/')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()