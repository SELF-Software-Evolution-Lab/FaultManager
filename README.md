Welcome to IoT Fault Monitoring Application

# Configuration

## How to install Python 3.6 in Cloud9

This application is configured to run in Python 3.6. Next is the procedure to configure Python 3.6 in Colud9 Ide

Download required version of Python 3.6:

    $ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
    
Decompress:

    $ tar xvf Python-3.6.3.tgz
    
Install:

    $ cd Python-3.6.3
    $ ./configure --enable-optimizations
    $ make -j8
    $ sudo make altinstall
    $ which python3.6
    /usr/local/bin/python3.6
    $ sudo ln -fs /usr/local/bin/python3.6 /usr/bin/python
    $ python --version
    python 3.6
    
Upgrade Setup Tools and Pip:

    $ pip install setuptools --upgrade  
    $ pip install pip --upgrade

Install Virtual Environment:

    $ pip install virtualenv
    
Configure Virtual Environment:

    $ virtualenv --python $(which python3.6) ~/.virtualenvs/test
    $ source ~/.virtualenvs/test/bin/activate

## Requirements

This application needs several components. See requirements.txt to see which components relates on.
To create requirements.txt automatizated follow the next instructions

Install Pip Requirements:

    $ pip install pipreqs
    
Generate requirements.txt:

    $ ~/workspace (master) $ pipreqs . --force
    

## Some tips to install

To install Python 3.6.3 check https://gist.github.com/espozbob/b86bbfbbdc78a47461037036d365ebfb
To install DJango 2.1.2 run next command:

    $ pip install Django
    
To install MySQL 5.7.23 check https://wpkb.org/install-mysql-5-7-at-cloud9-workspace/

To Django REST Documentation run next commands:

    $ sudo pip install coreapi
    $ pip install -U drf-yasg


# Running the application

Create Django's default superuser and auth system

    e.g:
    $ python manage.py createsuperuser
    Username: admin
    Email address: admin@example.com
    Password: abcd4321
    Password (again): abcd4321
    Superuser created successfully.
    
## Starting from the Terminal

Change to correct virtual environment:

    $ source ~/.virtualenvs/test/bin/activate

If neccesary run syncdb command to sync models to database and create Django's default superuser and auth system:

    $ python manage.py migrate
    
Start (C9 MySql) Database:   

    $ mysql-ctl start

Start (C9 Redis) Database:

    $ sudo service redis-server start

Run Django:

    $ python manage.py runserver $IP:$PORT
    
## Running tests

To tests server run following command:

    $ python manage.py test iotfaults.tests

# Utilities

To run Python Interactive Shell:

    $ python manage.py shell
    
To Exit Python Interactive Shell:

    $ Ctrl-D

To run (C9) MySql Database Client:

    $ mysql-ctl cli

To run (C9) Redis Client:

    $ redis-cli
    
This are some Redis Configuration in C9:    

    Parameters: 
        Hostname - $IP (The same local IP as the application you run on Cloud9)
        Port - 6379 (The default Redis port number)
        Password - “” (No password since you can only access the DB from within the workspace)

To Dump Data:

    $ python manage.py dumpdata > ./iotfaults/fixtures/db.json
    
To Load Data:

    $ python manage.py loaddata ./iotfaults/fixtures/type.json
    
For info in data load and dump see https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata

Take in to account that Mozilla doesn't allow WebSockets by default to config it go to about:config and configure parameter as network.websocket.allowInsecureFromHTTPS=True

To check all avalaible URLs type https://django-iot-apeream.c9users.io/iotfaults/api/x

