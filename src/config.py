import os

SECRET_KEY = os.environ.get('SECRET_KEY') or str(os.urandom(32))
PORT = int(os.environ.get('PORT', 5000))

if os.environ.get('CLEARDB_DATABASE_URL'): # heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('CLEARDB_DATABASE_URL')
elif os.environ.get('UFABCHELPER_DATABASE_URL'): # localhost mariadb/mysql
    SQLALCHEMY_DATABASE_URI = os.environ.get('UFABCHELPER_DATABASE_URL')

# adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress warnings
SQLALCHEMY_TRACK_MODIFICATIONS = False 
# set to True to enable automatic commits of database changes at the end of each request
SQLALCHEMY_COMMIT_ON_TEARDOWN = True 
TEMPLATES_AUTO_RELOAD = True