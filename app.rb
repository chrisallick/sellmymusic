require 'sinatra'
require 'redis'

$redis = Redis.new

assets_version = 1

allowed_video_upload_formats = [".png", ".gif", ".jpeg", ".jpg"]

##########   /*     */   ##########

get '/' do
    albums = $redis.smembers( "albums" )
    erb :home, :locals => {
        :av => assets_version,
        :albums => albums
    }
end

# ##########   /*     */   ##########


class Helpers
    @@S3_KEY='AKIAJNFVHNCXMSLWZOAA'
    @@S3_SECRET='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'

    def self.write_upload_to_disk(filename, file_data)
        File.open(filename, "wb") { |f| f.write(file_data) }
    end

    def self.s3_upload(img_data, extension, uuid)
        name = uuid + extension

        connection = Fog::Storage.new(
            :provider                 => 'AWS',
            :aws_secret_access_key    => @@S3_SECRET,
            :aws_access_key_id        => @@S3_KEY
        )

        directory = connection.directories.create(
            :key    => "smm-albumart",
            :public => true
        )
    
        content_type = case extension
        when ".gif"
            "image/gif"
        when ".png"
            "image/png"
        when ".jpeg" || ".jpg"
            "image/jpeg"
        else
            ""
        end

        file = directory.files.create(
            :key    => name,
            :body   => img_data,
            :content_type => content_type,
            :public => true
        )
    
        if extension == ".gif"
            return "https://s3.amazonaws.com/"+bucket+"/"+name
        else
            return "http://trash.imgix.net/#{name}"
        end
    end
end


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


get '/add' do
    erb :add, :locals => {
        :av => assets_version
    }
end

post '/add' do
    puts params[:album]
end

post '/delete' do

end

post '/uploadfile' do
    extension = File.extname(request.env['HTTP_X_FILENAME']).downcase

    if allowed_video_upload_formats.include? extension
        uuid = UUIDTools::UUID.random_create.to_s

        s3_url = Helpers.s3_upload( request.env["rack.input"].read, extension, uuid )

        return { :result => "success", :msg => s3_url }.to_json
    else
        return { :result => "fail", :msg => "invalid file" }.to_json
    end
end