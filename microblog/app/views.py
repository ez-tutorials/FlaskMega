from app import app

"""
The two route decorators above the function create the mappings from URLs / and /index to this function.
"""
@app.route('/')
def root():
    return "Hello ROOT!"
@app.route('/index')
def index():
    return "Hello INDEX!"
