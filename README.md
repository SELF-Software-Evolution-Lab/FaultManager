
     ,-----.,--.                  ,--. ,---.   ,--.,------.  ,------.
    '  .--./|  | ,---. ,--.,--. ,-|  || o   \  |  ||  .-.  \ |  .---'
    |  |    |  || .-. ||  ||  |' .-. |`..'  |  |  ||  |  \  :|  `--, 
    '  '--'\|  |' '-' ''  ''  '\ `-' | .'  /   |  ||  '--'  /|  `---.
     `-----'`--' `---'  `----'  `---'  `--'    `--'`-------' `------'
    ----------------------------------------------------------------- 


Welcome to your Django project on Cloud9 IDE!

Your Django project is already fully setup. Just click the "Run" button to start
the application. On first run you will be asked to create an admin user. You can
access your application from 'https://django-iot-apeream.c9users.io/' and the admin page from 
'https://django-iot-apeream.c9users.io/admin'.

## Starting from the Terminal

In case you want to run your Django application from the terminal just run:

1) Run syncdb command to sync models to database and create Django's default superuser and auth system

    $ python manage.py migrate

2) Run Django

    $ python manage.py runserver $IP:$PORT
    
## Configuration

You can configure your Python version and `PYTHONPATH` used in
Cloud9 > Preferences > Project Settings > Language Support.

## Support & Documentation

Django docs can be found at https://www.djangoproject.com/

You may also want to follow the Django tutorial to create your first application:
https://docs.djangoproject.com/en/1.9/intro/tutorial01/

Visit http://docs.c9.io for support, or to learn more about using Cloud9 IDE.
To watch some training videos, visit http://www.youtube.com/user/c9ide

## Installed
Python 3.6.3: https://gist.github.com/espozbob/b86bbfbbdc78a47461037036d365ebfb
DJango 2.1.2: pip install Django
MySQL 5.7.23: https://wpkb.org/install-mysql-5-7-at-cloud9-workspace/

# For Django REST Documentation
sudo pip install coreapi
pip install -U drf-yasg

# Requirements
pip install pipreqs
~/workspace (master) $ pipreqs . --force
    
# Virtual Environment
source ~/.virtualenvs/test/bin/activate

# Python Interactive Shell
python manage.py shell
Exit: Ctrl-D

# C9 MySql Database
Start: mysql-ctl start
Client: mysql-ctl cli

# C9 Redis
Start: sudo service redis-server start
Client: redis-cli
Prameters: Hostname - $IP (The same local IP as the application you run on Cloud9)
           Port - 6379 (The default Redis port number)
           Password - “” (No password since you can only access the DB from within the workspace)

# DumpData
Dump: python manage.py dumpdata > ./iotfaults/fixtures/db.json
Load: python manage.py loaddata ./iotfaults/fixtures/type.json
Info: https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata

# Run Python server
python manage.py runserver $IP:$PORT

# Mozilla Firefox Websokets
Mozilla doen't allow WebSockets by default: about:config, network.websocket.allowInsecureFromHTTPS=True

# View all valid URLs
https://django-iot-apeream.c9users.io/iotfaults/api/x

admin
abcd4321