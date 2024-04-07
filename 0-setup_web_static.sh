#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
# check if Nginx installed
if ! dpkg -l nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi
# create directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
# HTML file for testing
sudo tee /data/web_static/releases/test/index.html > /dev/null <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF
# create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current
# set ownership
sudo chown -R ubuntu:ubuntu /data/
# configure Nginx
c="location /hbnb_static {\n\\t\\talias /data/web_static/current/;\n\\t}"
if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
	sudo sed -i "/^server {/a $c" /etc/nginx/sites-available/default
fi
# check configuration and start
sudo nginx -t && sudo service nginx restart
exit 0
