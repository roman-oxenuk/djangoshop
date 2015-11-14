# django_project_template
Template for newborn django project. Use with django-admin.py startproject --template="https://github.com/roman-oxenuk/django_project_template/archive/master.zip" 

# New Django Project
* mkproject projectname
* pip install django
* cd ../
* django-admin startproject projectdir projectname --template="https://github.com/roman-oxenuk/django_project_template/archive/master.zip"
* cd projectdir 
* pip install -r project/requirements.txt
* chmod +x manage.py
* ./manage.py migrate
* ./manage.py createsuperuser
* pip freeze > project/requirements.txt

To check it:
* ./manage.py runserver
* localhost:8000/hello


# Deploy
login as myuser to project folder
make directories:
```
mkproject <project_name>
mkdir conf
mkdir logs
mkdir static_content
mkdir static_content/static
mkdir static_content/media
mkdir src
```
clone project source and install requirements and gunicorn
```
cd src
git clone <gitlab source> .
pip install -r project/requirements.txt
pip install gunicorn
```
configuring gunicorn
```
cd ..
touch conf/gunicorn_conf.py
```
gunicorn_conf.py content:
```
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

# bind = "127.0.0.1:8888"
bind = "unix:///home/roman/py_projects/<project_name>/<project_name>.sock"
# workers = 3
# loglevel = "warn"
# errorlog = "/home/roman/py_projects/<project_name>/logs/gunicorn_error.log"
# accesslog = "/home/roman/py_projects/<project_name>/logs/gunicorn_access.log"
```
configuring nginx
```touch conf/<project_name>.nginx.conf```
conf/<project_name>.nginx.conf content
```
upstream <project_name> {
   ip_hash;
   server unix:///home/roman/py_projects/<project_name>/<project_name>.sock;
   # server 127.0.0.1:8888;
}

server {
    listen 127.0.0.1:80;
    access_log /home/roman/py_projects/<project_name>/logs/nginx_access.log;
    error_log /home/roman/py_projects/<project_name>/logs/nginx_error.log;

    location /static {
        alias /home/roman/py_projects/<project_name>/static_content/static;
    }

    location /media {
        alias /home/roman/py_projects/<project_name>/static_content/media;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://<project_name>;
    }
}
```
link our config with nginx's sites-enabled folder
```
sudo ln -s <projects_path>/<project_name>/conf/<project_name>.nginx.conf /etc/nginx/sites-enabled/<project_name>.nginx.conf
```
and django commands
```
cd src
./manage.py collectstatic
./manage.py migrate
./manage.py createsuperuser
```
run gunicorn
```
gunicorn -c <projects_path>/<project_name>/conf/gunicorn_conf.py project.wsgi:application
```
run nginx
```
sudo service nginx start
```

add supervisor for keep gunicorn running
```
touch /etc/supervisor/<project_name>.conf
```
content on that file
```
[program:<project_name>]
command=/home/myuser/.virtualenvs/<project_name>/bin/gunicorn -c /home/myuser/www/<project_name>/conf/gunicorn_conf.py project.wsgi:application
directory=/home/myuser/www/<project_name>/src/
autostart=true
autorestart=true
user=myuser
```
run supervisor
```
sudo supervisorctl reload
```


## TODO:
* ~~supervisord~~
* PostgreSQL
* ~~Redis~~
* ~~New Relic~~
* Sentry
