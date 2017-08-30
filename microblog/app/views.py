from app import app
from flask import render_template
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
