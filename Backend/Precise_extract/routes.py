from flask import render_template, url_for, flash, redirect
from Precise_extract import app
from Precise_extract import mysql
from Precise_extract import bcrypt
from Precise_extract.forms import RegistrationForm,LoginForm
import uuid


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login" ,methods=['GET' , 'POST'] )
def login():
    form1 = RegistrationForm()
    form = LoginForm()
    if form1.validate_on_submit() and form1.submit.data:
        curr = mysql.connection.cursor()
        curr.execute(f"SELECT email FROM user WHERE email='{form1.email.data}'")
        if len(curr.fetchall()) == 0:
            hashed_password = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
            curr.execute(f"INSERT INTO `user`(`userid`, `email`, `password`) VALUES ('{str(uuid.uuid4())}','{form1.email.data}','{hashed_password}')")
            mysql.connection.commit()
            curr.close()
            # flash(f'Registered Successfully !')
            return redirect(url_for('browse'))
        else:
            print("Email is already registered !")
            flash('Email is already registered !','epopup1')
        curr.close()
    
    return render_template("login.html",form=form,form1=form1)

@app.route("/browse")
def browse():
    return render_template('browse.html')
