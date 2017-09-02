from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
"""
If you are wondering why the import statement is at the end and not at the beginning of the script as it is always done, 
the reason is to avoid circular references, because you are going to see that the views module needs to import the app 
variable defined in this script. Putting the import at the end avoids the circular import error.
"""
app.config.from_object('config')
# Initialize database
db = SQLAlchemy(app)

"""
The views are the handlers that respond to requests from web browsers or other clients. 
In Flask handlers are written as Python functions. Each view function is mapped to one or more request URLs.
"""
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    """
    The log file will go to our tmp directory, with name microblog.log. We are using the RotatingFileHandler so that there is a limit to the amount of logs that are generated. In this case we are limiting the size of a log file to one megabyte, and we will keep the last ten log files as backups.

    The logging.Formatter class provides custom formatting for the log messages. Since these messages are going to a file, we want them to have as much information as possible, so we write a timestamp, the logging level and the file and line number where the message originated in addition to the log message and the stack trace.

    To make the logging more useful, we are lowering the logging level, both in the app logger and the file logger handler, as this will give us the opportunity to write useful messages to the log without having to call them errors. As an example, we start by logging the application start up as an informational level. From now on, each time you start the application without debugging the log will record the event.
    """
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@', MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


from app import views, models
