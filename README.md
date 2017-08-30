# FlaskMega

This is a tutorial series at [The Flask Mega Tutoiral](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
This project will enventually create a microblog application, which will have the following functionalities:

* User management, including managing logins, sessions, user roles, profiles and user avatars.
* Database management, including migration handling.
* Web form support, including field validation.
* Pagination of long lists of items.
* Full text search.
* Email notifications to users.
* HTML templates.
* Support for multiple languages.
* Caching and other performance optimizations.
* Debugging techniques for development and production servers.
* Installation on a production server.

## Create virtual environment

Because I'm using the anaconda python package, also I'd like to use *Python 3.6* as used in the tutorial. I have to install *virtualen* with *cond* as follow:
```
$ conda install virtualenv
```
Then to create the virtual envirment:

```
$ cd ~/Projects/FlaskMega/microblog
$ virtualenv flask
```

## Install Requirments

I've copied the required packge list from the tutorial website and saved them in the *requirements.txt*. So I can just intall all of them at once after activate my envirment:
```
$ source flask/bin/activate
(flask)$ pip install -r requirements.txt --no-index
```

## Project Directory Structure
```
microblog/app
├── __init__.py
├── static
└── templates
```
**app/** is where the main application is.

**static/** is where static files, such as images, javascripts, and cascading style sheets, are stored.

**templates** contains all tempalted *html* files.

## Run Application
There is a *run.py* in the root of the application directory, i.e. *microblog/*.
Give it a executable permission by:
```
(flask)$ chmod a+x run.py
(flask)$ ./run.py
```
Then, in the browser open [127.0.0.1:5000](127.0.0.1:5000).
