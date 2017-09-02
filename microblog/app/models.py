from app import db

"""
Relational databases are good at storing relations between data items. Consider the case of a user writing a blog post. The user will have a record in the users table, and the post will have a record in the posts table. The most efficient way to record who wrote a given post is to link the two related records.

Once a link between a user and a post is established there are two types of queries that we may need to use. The most trivial one is when you have a blog post and need to know what user wrote it. A more complex query is the reverse of this one. If you have a user, you may want to know all the posts that the user wrote. Flask-SQLAlchemy will help us with both types of queries.

Our posts table will have the required id, the body of the post and a timestamp. Not much new there. But the user_id field deserves an explanation.

We said we wanted to link users to the posts that they write. The way to do that is by adding a field to the post that contains the id of the user that wrote it. This id is called a foreign key. Our database design tool shows foreign keys as a link between the foreign key and the id field of the table it refers to. This kind of link is called a one-to-many relationship, one user writes many posts.
"""

class User(db.Model):
    """
    The User class that we just created contains several fields, defined as class variables. Fields are created as instances of the db.Column class, which takes the field type as an argument, plus other optional arguments that allow us, for example, to indicate which fields are unique and indexed.
    """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        """
        The __repr__ method tells Python how to print objects of this class. We will use this for debugging.
        """
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

"""
We have added the Post class, which will represent blog posts written by users. The user_id field in the Post class was initialized as a foreign key, so that Flask-SQLAlchemy knows that this field will link to a user.

Note that we have also added a new field to the User class called posts, that is constructed as a db.relationship field. This is not an actual database field, so it isn't in our database diagram. For a one-to-many relationship a db.relationship field is normally defined on the "one" side. With this relationship we get a user.posts member that gets us the list of posts from the user. The first argument to db.relationship indicates the "many" class of this relationship. The backref argument defines a field that will be added to the objects of the "many" class that points back at the "one" object. In our case this means that we can use post.author to get the User instance that created a post.
"""
