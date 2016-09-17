sudo killall uwsgi nginx
sleep 1
uwsgi --ini $PWD/server_settings/uwsgi.ini --plugin python3 &
# sudo 
nginx -c $PWD/server_settings/nginx.conf &
