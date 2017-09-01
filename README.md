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
microblog/
├── app
│   ├── forms.py
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── forms.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── static
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── login.html
│   └── views.py
├── app.db
├── config.py
├── db_create.py
├── db_downgrade.py
├── db_migrate.py
├── db_repository
│   ├── __init__.py
│   ├── manage.py
│   ├── migrate.cfg
│   ├── __pycache__
│   │   └── __init__.cpython-36.pyc
│   ├── README
│   └── versions
│       ├── 001_migration.py
│       ├── __init__.py
│       └── __pycache__
│           ├── 001_migration.cpython-36.pyc
│           └── __init__.cpython-36.pyc
├── db_upgrade.py
├── __pycache__
│   └── config.cpython-36.pyc
├── requirements.txt
├── run.py
└── tmp
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


## Tutorial Links
* [Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

* [Part II: Templates](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)

* [Part III: Web Forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms)

* [Part IV: Database](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)

    * create a new user:
    ```python
    >>> u = models.User(nickname='john', email='john@email.com')
    >>> db.session.add(u)
    >>> db.session.commit()
    >>>
    ```
    * Query users
    ```python
    >>> users = models.User.query.all()
    >>> users
    [<User u'john'>, <User u'susan'>]
    >>> for u in users:
    ...     print(u.id,u.nickname)
    ...
    1 john
    2 susan
    >>>
    ```
    * Query by user_id
    ```python
    >>> u = models.User.query.get(1)
    >>> u
    <User u'john'>
    >>>
    ```
    * Add a blog post:
    ```python
    >>> import datetime
    >>> u = models.User.query.get(1)
    >>> p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
    >>> db.session.add(p)
    >>> db.session.commit()
    ```
    * More database query
    ```python
    # get all posts from a user
    >>> u = models.User.query.get(1)
    >>> u
    <User u'john'>
    >>> posts = u.posts.all()
    >>> posts
    [<Post u'my first post!'>]

    # obtain author of each post
    >>> for p in posts:
    ...     print(p.id,p.author.nickname,p.body)
    ...
    1 john my first post!

    # a user that has no posts
    >>> u = models.User.query.get(2)
    >>> u
    <User u'susan'>
    >>> u.posts.all()
    []

    # get all users in reverse alphabetical order
    >>> models.User.query.order_by('nickname desc').all()
    [<User u'susan'>, <User u'john'>]
    >>>
    ```
    The [Flask-SQLAlchemy](http://packages.python.org/Flask-SQLAlchemy/index.html) documentation is the best place to learn about the many options that are available to query the database.

    * Delete the created users
    ```python
    >>> users = models.User.query.all()
    >>> for u in users:
    ...     db.session.delete(u)
    ...
    >>> posts = models.Post.query.all()
    >>> for p in posts:
    ...     db.session.delete(p)
    ...
    >>> db.session.commit()
    >>>
    ```


* [Part V: User Logins](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins)

* [Part VI: Profile Page And Avatars](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars)

* [Part VII: Unit Testing](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)

* [Part VIII: Followers, Contacts And Friends](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends)

* [Part IX: Pagination](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination)

* [Part X: Full Text Search](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-full-text-search)

* [Part XI: Email Support](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support)

* [Part XII: Facelift](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xii-facelift)

* [Part XIII: Dates and Times](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-dates-and-times)

* [Part XIV: I18n and L10n](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n)

* [Part XV: Ajax](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-ajax)

* [Part XVI: Debugging, Testing and Profiling](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-debugging-testing-and-profiling)

* [Part XVII: Deployment on Linux (even on the Raspberry Pi!)](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux-even-on-the-raspberry-pi)

* [Part XVIII: Deployment on the Heroku Cloud](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-the-heroku-cloud)