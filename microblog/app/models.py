from app import db
from hashlib import md5

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
    
    """
    Every time we modify the database we have to generate a new migration. Remember that in the database chapter we went through the pain of setting up a database migration system. We can see the fruits of that effort now. To add these two new fields to our database we just do this:
    $ ./db_migrate.py

    PS: close SQLit client before run the above command
    """
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

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

    def avatar(self, size):
        """
        The avatar method of User returns the URL of the user's avatar image, scaled to the requested size in pixels.
        
        Turns out with the Gravatar service this is really easy to do. You just need to create an md5 hash of the user email and then incorporate it into the specially crafted URL that you see above. After the md5 of the email you can provide a number of options to customize the avatar. The d=mm determines what placeholder image is returned when a user does not have an Gravatar account. The mm option returns the "mystery man" image, a gray silhouette of a person. The s=N option requests the avatar scaled to the given size in pixels.

        The nice thing about making the User class responsible for returning avatars is that if some day we decide Gravatar avatars are not what we want, we just rewrite the avatar method to return different URLs (even ones that points to our own web server, if we decide we want to host our own avatars), and all our templates will start showing the new avatars automatically.
        """
        email = self.email
        # https: // en.gravatar.com / userimage / 76305420 / e795a415c4e6e3415c961787136428ef.jpg?size = 200
        # this line is to replace zhouen.nathan@yahoo.com with nathanzhou@qq.com so that Gravatar can work for this email address
        if email == "zhouen.nathan@yahoo.com":
            email = "nathanzhou@qq.com"
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(email.encode('utf-8')).hexdigest(), size)
    
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
