#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
if ! dpkg -l nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
c="\\tlocation /hbnb_static {\n\\t\\talias /data/web_static/current/;\n\\t}"
if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
	sudo sed -i "/^server {/a $c" /etc/nginx/sites-available/default
fi
sudo service nginx restart
exit 0
