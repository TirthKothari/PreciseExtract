from flask import render_template, url_for, flash, redirect
from Precise_extract import app,mail
from Precise_extract import mysql
from Precise_extract import bcrypt
from Precise_extract import session,socketio
from Precise_extract.forms import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm
import uuid
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Message

# -----------------functions-----------------
def get_reset_token(user):
    s = Serializer(app.config['SECRET_KEY'])
    return s.dumps({'user_id':user})
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token,max_age=30)['user_id']
    except:
        return None
    return user_id
def send_reset_email(user):
    token  = get_reset_token(user[0])
    session['reset_email'] = user[1]
    msg = Message("Password Reset",sender='noreply@precise_extract.com',recipients=[user[1]])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token',token=token, _external=True)}

if you did not  make this request then simply  ignore this email !
'''
    mail.send(msg)
    
# -----------------------------functions end--------------------------


# ------------------home-------------------

@app.route("/")
@app.route("/home" ,methods=['GET','POST'])
def home():
    try:
        return render_template("home.html",session=session['loggedin'])
    except KeyError:
        return render_template("home.html",session=False)



# --------------------login------------------------    

@app.route("/login" ,methods=['GET' , 'POST'] )
def login():
    try:
        if session['loggedin'] == True:
            return redirect(url_for('home'))
    except:
        pass
    form1 = RegistrationForm()
    form = LoginForm()
    resetform = RequestResetForm()

    if form1.validate_on_submit():
        curr = mysql.connection.cursor()
        curr.execute(f"SELECT email FROM user WHERE email='{form1.email.data}'")
        if len(curr.fetchall()) == 0:
            hashed_password = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
            curr.execute(f"INSERT INTO `user`(`userid`, `email`, `password`) VALUES ('{(uuid.uuid4().int)}','{form1.email.data}','{hashed_password}')")
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
                session['loggedin'] = True
                session['userid'] = user[0]
                session['email'] = user[1]
                return redirect(url_for('home'))
            else:
                flash('Invalid Email or Password !','epopup1')
                return redirect(url_for('login'))
        else:
            flash('Invalid Email or Password !','epopup1')
            return redirect(url_for('login'))
        
    if resetform.validate_on_submit():
        curr = mysql.connection.cursor()
        curr.execute(f"SELECT `userid`, `email`, `password` FROM `user` WHERE email='{resetform.email.data}'")
        user = curr.fetchone()
        curr.close()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset password.')
            return redirect(url_for('login'))
        else:
            flash("No account regeistered on this email, Regeister first. !")
            return redirect(url_for("login"))

    return render_template("login.html",form=form,form1=form1,resetform = resetform)


# -----------------------resetpass-------------------

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if session['loggedin'] == True:
        return redirect(url_for('home'))
    else:
        user = verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token')
            return redirect(url_for('login'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            curr = mysql.connection.cursor()
            hashed_password = bcrypt.generate_password_hash(form.confirm_new_password.data).decode('utf-8')
            curr.execute(f"UPDATE `user` SET `password`='{hashed_password}' WHERE `email`='{session['reset_email']}'")
            mysql.connection.commit()
            curr.close()
            session.pop('reset_email',None)
            flash("Your password has been updated")
            return redirect(url_for('login'))
        return render_template("reset.html",form=form)
     
# --------------------logout-----------------

@app.route("/logout")
def logout():
    session['loggedin'] = False
    session.pop("userid",None)
    session.pop("email",None)
    return redirect(url_for('home'))
    

#-----------------------------main page---------------------------
@app.route("/main")
def main():
    return render_template('main.html')