from flask import Flask,session
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit
from flask_mail import Mail
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = '8a27dc7b112ed8e70ca02fa3778e04b6'
app.config['AES_SECRET_KEY'] = b'1!\x14\xd8?\x03\xefm\xa0*1\xaf\xd8\xe7\x9b\xdcb\xed\xeek\xf8?\\:@\xed,\x06*\xcbYL'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'precise_extract'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['UPLOAD_FOLDER'] = 'UPLOADED_FILES'
mail = Mail(app)

bcrypt = Bcrypt(app)

mysql = MySQL(app)

socketio = SocketIO(app)



# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db=SQLAlchemy(app)

from Precise_extract import routes
