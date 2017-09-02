from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
"""
The g global is setup by Flask as a place to store and share data during the life of a request. As I'm sure you guessed by now, we will be storing the logged in user here.

The url_for function that we used in the redirect call is defined by Flask as a clean way to obtain the URL for a given view function. If you want to redirect to the index page you may very well use redirect('/index'), but there are very good reasons to let Flask build URLs for you.

The flask.session provides a much more complex service along those lines. Once data is stored in the session object it will be available during that request and any future requests made by the same client. Data remains in the session until explicitly removed. To be able to do this, Flask keeps a different session container for each client of our application.
"""
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app import oid, lm
from .forms import LoginForm, EditForm
from .models import User

"""
The two route decorators above the function create the mappings from URLs / and /index to this function.
"""
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )
"""
To render the template we had to import a new function from the Flask framework called render_template. 
This function takes a template filename and a variable list of template arguments and returns the rendered template, 
with all the arguments replaced.
Under the covers, the render_template function invokes the Jinja2 templating engine that is part of the Flask framework. 
Jinja2 substitutes {{...}}blocks with the corresponding values provided as template arguments.
"""

"""
Control statements in templates
The Jinja2 templates also support control statements, given inside {%...%} blocks. 
Let's add an if statement to our template (file app/templates/index.html)
"""

"""
Loops in templates
The logged in user in our microblog application will probably want to see recent posts from followed users in the home 
page, so let's see how we can do that.
To begin, we use our handy fake object trick to create some users and some posts to show (file app/views.py):
"""

"""
The list can have any number of elements, it will be up to the view function to decide how many posts need to be presented. 
The template cannot make any assumptions about the number of posts, so it needs to be prepared to render as many posts as the view sends.
"""

"""
Template inheritance
We can add a navigation bar to our index.html template, but as our application grows we will be needing to implement more pages, 
and this navigation bar will have to be copied to all of them. Then you will have to keep all these identical copies of the 
navigation bar in sync, and that could become a lot of work if you have a lot of pages and templates.

Instead, we can use Jinja2's template inheritance feature, which allows us to move the parts of the page layout that are common to 
all templates and put them in a base template from which all other templates are derived.
"""


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template(
        'login.html',
        title='Sign In',
        form=form,
        providers=app.config['OPENID_PROVIDERS']
    )
"""
So basically, we have imported our LoginForm class, instantiated an object from it, and sent it down to the template. This is all that is required to get form fields rendered.
The only other thing that is new here is the methods argument in the route decorator. This tells Flask that this view function accepts GET and POST requests. Without this the view will only accept GET requests. We will want to receive the POST requests, these are the ones that will bring in the form data entered by the user.
"""

"""
The validate_on_submit method does all the form processing work. If you call it when the form is being presented to the user (i.e. before the user got a chance to enter data on it) then it will return False, so in that case you know that you have to render the template.

When validate_on_submit is called as part of a form submission request, it will gather all the data, run all the validators attached to fields, and if everything is all right it will return True, indicating that the data is valid and can be processed. This is your indication that this data is safe to incorporate into the application.
If at least one field fails validation then the function will return False and that will cause the form to be rendered back to the user, and this will give the user a chance to correct any mistakes. We will see later how to show an error message when validation fails.
"""

"""
When validate_on_submit returns True our login view function calls two new functions, imported from Flask. The flash function is a quick way to show a message on the next page presented to the user. In this case we will use it for debugging, since we don't have all the infrastructure necessary to log in users yet, we will instead just display a message that shows the submitted data. The flash function is also extremely useful on production servers to provide feedback to the user regarding an action. 
"""

@lm.user_loader
def load_user(id):
    """
    user ids in Flask-Login are always unicode strings, so a conversion to an integer is necessary before we can send the id to Flask-SQLAlchemy.
    """
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    """
    The first if statement is just for validation. We require a valid email, so if an email was not provided we cannot log the user in.
    """
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    """
    If the email is not found we consider this a new user, so we add a new user to our database, pretty much as we have learned in the previous chapter. Note that we handle the case of a missing nickname, since some OpenID providers may not have that information.
    """
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    """
    The concept of the next page is simple. Let's say you navigate to a page that requires you to be logged in, but you aren't just yet. In Flask-Login you can protect views against non logged in users by adding the login_required decorator. If the user tries to access one of the affected URLs then it will be redirected to the login page automatically. Flask-Login will store the original URL as the next page, and it is up to us to return the user to this page once the login process completed.
    """
    return redirect(request.args.get('next') or url_for('index'))

"""
we check g.user to determine if a user is already logged in. To implement this we will use the before_request event from Flask. Any functions that are decorated with before_request will run before the view function each time a request is received. 
"""
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User Profile Page
"""
The @app.route decorator that we used to declare this view function looks a little bit different than the previous ones. In this case we have an argument in it, which is indicated as <nickname>. This translates into an argument of the same name added to the view function. When the client requests, say, URL /user/miguel the view function will be invoked with nickname set to 'miguel'.
The implementation of the view function should have no surprises. First we try to load the user from the database, using the nickname that we received as argument. If that doesn't work then we just redirect to the main page with an error message, as we have seen in the previous chapter.

Once we have our user, we just send it in the render_template call, along with some fake posts. Note that in the user profile page we will be displaying only posts by this user, so our fake posts have the author field correctly set.
"""
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


"""
Custom HTTP error handlers

Flask provides a mechanism for an application to install its own error pages. As an example, let's define custom error pages for the HTTP errors 404 and 500, the two most common ones. 
"""

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
