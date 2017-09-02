#!../flask/bin/python

"""
Discussing the unittest module is outside the scope of this article. Let's just say that class TestCase holds our tests. The setUp and tearDown methods are special, these are run before and after each test respectively. A more complex setup could include several groups of tests each represented by a unittest.TestCase subclass, and each group then would have independent setUp and tearDown methods.

These particular setUp and tearDown methods are pretty generic. In setUp the configuration is edited a bit. For instance, we want the testing database to be different that the main database. In tearDown we just reset the database contents.

Tests are implemented as methods. A test is supposed to run some function of the application that has a known outcome, and should assert if the result is different than the expected one.

So far we have two tests in the testing framework. The first one verifies that the Gravatar avatar URLs from the previous article are generated correctly. Note how the expected avatar is hardcoded in the test and checked against the one returned by the User class.

The second test verifies the make_unique_nickname method we just wrote, also in the User class. This test is a bit more elaborate, it creates a new user and writes it to the database, then ensures the same name is not allowed as a unique name. It then creates a second user with the suggested unique name and tries one more time to request the first nickname. The expected result for this second part is to get a suggested nickname that is different from the previous two.
"""

import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_avatar(self):
        u = User(nickname='join', email='nathan@email.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/9d4806832c56ee86c6aae26889c53c67?d=mm&s=128'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname


if __name__ == '__main__':
    unittest.main()
