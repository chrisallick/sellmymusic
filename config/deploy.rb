set :application, "sellmusic"
set :repository,  "git@github.com:chrisallick/sellmymusic.git"
set :scm, :git
set :deploy_to, "/home/ec2-user/#{application}"
set :public_dir, "#{deploy_to}/current/public"
set :use_sudo, false

set :user, "ec2-user"
set :key_pair, "music"

ssh_options[:keys] = "~/.ssh/#{key_pair}.pem"
server "ec2-174-129-103-27.compute-1.amazonaws.com", :app, :primary => true




# set :normalize_asset_timestamps, false



# 


# set :rvm_type, :system

#after "deploy:restart", "deploy:cleanup"

# # If you are using Passenger mod_rails uncomment this:
# namespace :deploy do
#   task :start do ; end
#   task :stop do ; end
#   task :restart, :roles => :app, :except => { :no_release => true } do
#     run "touch #{File.join(current_path,'tmp','restart.txt')}"
#   end
# end