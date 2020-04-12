#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# update
apt-get update
# install nginx
apt-get install -y nginx

# create required directories
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# set index.html
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

# change owner and group
chown -R ubuntu /data/ && chgrp -R ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default
# restart nginx server
service nginx restart
