from flask import render_template, url_for, flash, redirect
from Precise_extract import app
from Precise_extract import mysql
from Precise_extract import bcrypt
from Precise_extract import session,socketio
from Precise_extract.forms import RegistrationForm,LoginForm
import uuid

@socketio.on('disconnect')
def disconnect():
    session.pop('userid',None)
    session.pop('email',None)
    session.pop('loggedin', None)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login" ,methods=['GET' , 'POST'] )
def login():
    try:
        if session['loggedin'] == True:
            return redirect(url_for('browse'))
    except:
        pass
    form1 = RegistrationForm()
    form = LoginForm()
    if form1.validate_on_submit():
        curr = mysql.connection.cursor()
        curr.execute(f"SELECT email FROM user WHERE email='{form1.email.data}'")
        if len(curr.fetchall()) == 0:
            hashed_password = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
            curr.execute(f"INSERT INTO `user`(`userid`, `email`, `password`) VALUES ('{str(uuid.uuid4())}','{form1.email.data}','{hashed_password}')")
            mysql.connection.commit()
            curr.close()
            # flash(f'Registered Successfully !')
            return redirect(url_for('login'))
        else:
            print("Email is already registered !")
            flash('Email is already registered !','epopup1')
            curr.close()
            return redirect(url_for('login'))
    
    if form.validate_on_submit():
        curr = mysql.connection.cursor()
        curr.execute(f"SELECT `userid`, `email`, `password` FROM `user` WHERE email='{form.email.data}'")
        user = curr.fetchone()
        curr.close()
        if user:
            if bcrypt.check_password_hash(user[2],form.password.data):
                session.permanent=False
                session['loggedin'] = True
                session['userid'] = user[0]
                session['email'] = user[1]
                return redirect(url_for('browse'))
            else:
                flash('Invalid Email or Password !','epopup1')
                return redirect(url_for('login'))
        else:
            flash('Invalid Email or Password !','epopup1')
            return redirect(url_for('login'))

    return render_template("login.html",form=form,form1=form1)

@app.route("/browse")
def browse():
    try:
        if session['loggedin'] != True:
            flash("Please Login to continue !",'epopup1')
            return redirect(url_for('login'))
    except:
        flash("Please Login to continue !",'epopup1')
        return redirect(url_for('login'))
    return render_template('browse.html')

@app.route("/logout")
def logout():
    session['loggedin'] = False
    session.pop("userid",None)
    session.pop("email",None)
    return redirect(url_for('home'))
    