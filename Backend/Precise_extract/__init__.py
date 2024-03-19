from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '8a27dc7b112ed8e70ca02fa3778e04b6'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'precise_extract'

bcrypt = Bcrypt(app)

mysql = MySQL(app)



# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db=SQLAlchemy(app)

from Precise_extract import routes
