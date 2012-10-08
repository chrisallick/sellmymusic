ENV['GOOGLE_AUTH_URL'] = '/openid'

require 'sinatra'
require 'sinatra/partial'
require 'sinatra/reloader' if development?
require 'sinatra/google-auth'

require 'redis'

$redis = Redis.new

assets_version = 1

admins = ["chrisallick@gmail.com", "allick@gmail.com"]


##########   /*     */   ##########


# def on_user(info)
# 	puts info.inspect
# end

##########   /*     */   ##########


get '/' do
	authenticate
	'hello'
  # albums = $redis.smembers( "albums" )

  # erb :home, :locals => {
  #   :assets_version => assets_version,
  #   :albums => albums
  # }
end


# ##########   /*     */   ##########


# class AdminHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.render("admin.html")


# ##########   /*     */   ##########


# class EditHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self, catnum):
#         if catnum:
#             c = pymongo.Connection('localhost')
#             db = c.albums
#             album = db.albums.find_one({'catnum':catnum})
#             if album:
#                 self.render("edit.html", album=album )
#             else:
#                 self.redirect("/")
#         else:
#             self.redirect("/")

# class AddHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         global admins
#         if self.current_user['email'] in admins:
#             self.render("add.html")

#     @tornado.web.authenticated
#     def post(self):
#         global admins
#         if self.current_user['email'] in admins:
#             album = self.get_argument('album', None)
#             print album
#             catnum = self.get_argument('remove', None)
#             if album:
#                 temp = json.loads(album)
#                 c = pymongo.Connection('localhost')
#                 db = c.albums
#                 albums = db.albums
#                 old = albums.find_one({'catnum':str(temp['catnum'])})
#                 if old:
#                     old.update(json.loads(album))
#                     albums.save(old)
#                 else:
#                     albums.insert( json.loads(album) )
#                 self.write( json.dumps({'msg': 'success'}) )
#             elif catnum:
#                 c = pymongo.Connection('localhost')
#                 db = c.albums
#                 db.albums.remove({'catnum': catnum})
#                 self.redirect("/")
#         else:
#             self.write( json.dumps({'msg': 'error'}) )


# ##########   /*     */   ##########


# class UploadHandler(BaseHandler):
#     @tornado.web.authenticated
#     def post(self):
#         if "X-File-Name" in self.request.headers:
#             file_name   = self.request.headers['X-File-Name']
#             print "receiving: " + file_name
#             try:
#                 f = open( './static/img/albums/'+file_name, 'w' )
#                 f.write( self.request.body )
#             except IOError:
#                 print "IOError"
#             else:
#                 f.close()