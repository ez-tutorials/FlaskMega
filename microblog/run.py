#!flask/bin/python

"""
The script simply imports the app variable from our app package and invokes its run method to start the server. 
Remember that the app variable holds the Flask instance that we created it above.
"""
from app import app
app.run(debug=True)
