from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm

"""
The two route decorators above the function create the mappings from URLs / and /index to this function.
"""
@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Nathan'}
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
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
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
