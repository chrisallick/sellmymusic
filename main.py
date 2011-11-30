#!/usr/bin/env python

import json
import os
import logging

import pymongo

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
            (r"/upload", UploadHandler),
            (r"/admin", AdminHandler),
            (r"/edit/(\d+)?/?", EditHandler),
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
        self.redirect("/")


##########   /*     */   ##########


class MainHandler(BaseHandler):
    def get(self):
        c = pymongo.Connection('localhost')
        db = c.albums
        albums = list()
        for a in db.albums.find().limit(10):
            albums.append( a )

        self.render("index.html", albums=albums )


##########   /*     */   ##########


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin.html")


##########   /*     */   ##########


class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, catnum):
        if catnum:
            c = pymongo.Connection('localhost')
            db = c.albums
            album = db.albums.find_one({'catnum':catnum})
            if album:
                self.render("edit.html", album=album )
            else:
                self.redirect("/")
        else:
            self.redirect("/")

class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user['email'] == "chrisallick@gmail.com":
            self.render("add.html")

    @tornado.web.authenticated
    def post(self):
        if self.current_user['email'] == "chrisallick@gmail.com":
            album = self.get_argument('album', None)
            catnum = self.get_argument('remove', None)
            if album:
                temp = json.loads(album)
                c = pymongo.Connection('localhost')
                db = c.albums
                albums = db.albums
                old = albums.find_one({'catnum':str(temp['catnum'])})
                if old:
                    old.update(json.loads(album))
                    albums.save(old)
                else:
                    albums.insert( json.loads(album) )
                self.write( json.dumps({'msg': 'success'}) )
            elif catnum:
                c = pymongo.Connection('localhost')
                db = c.albums
                db.albums.remove({'catnum': catnum})
                self.redirect("/")
        else:
            self.write( json.dumps({'msg': 'error'}) )


##########   /*     */   ##########


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        if "X-File-Name" in self.request.headers:
            file_name   = self.request.headers['X-File-Name']
            print "receiving: " + file_name
            try:
                f = open( './static/img/albums/'+file_name, 'w' )
                f.write( self.request.body )
            except IOError:
                print "IOError"
            else:
                f.close()


##########   /*     */   ##########


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()