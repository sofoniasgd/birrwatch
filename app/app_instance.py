# app_instance.py
from flask import Flask
from app.db import db, init_db

app = Flask(__name__)

# Configure the MySQL database
db_uri = "mysql+pymysql://at_dev_usr:at_dev_pwd@localhost/birrwatch_db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app context
init_db(app)