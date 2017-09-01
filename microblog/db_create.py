#!../flask/bin/python
"""
Creating the database

With the configuration and model in place we are now ready to create our database file. The SQLAlchemy-migrate package comes with command line tools and APIs to create databases in a way that allows easy updates in the future, so that is what we will use. I find the command line tools a bit awkward to use, so instead I have written my own set of little Python scripts that invoke the migration APIs.
"""
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

"""
Note how this script is completely generic. All the application specific pathnames are imported from the config file. When you start your own project you can just copy the script to the new app's directory and it will work right away.

To create the database you just need to execute this script (remember that if you are on Windows the command is slightly different):

./db_create.py

After you run the command you will have a new app.db file. This is an empty sqlite database, created from the start to support migrations. You will also have a db_repository directory with some files inside. This is the place where SQLAlchemy-migrate stores its data files. Note that we do not regenerate the repository if it already exists. This will allow us to recreate the database while leaving the existing repository if we need to.
"""
