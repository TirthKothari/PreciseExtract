from flask import render_template, url_for, flash, redirect,request,jsonify,make_response
from Precise_extract import app,mail
from Precise_extract import mysql
from Precise_extract import bcrypt
from Precise_extract import session,socketio
from Precise_extract.forms import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm
import uuid,os,threading
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Message
from werkzeug.utils import secure_filename
import jwt,datetime
from jose import jwe
import json
import jsonpickle  
import google.generativeai as genai
genai.configure(api_key='AIzaSyBWDaWi8YWzLXijXfVMeY9DWptfrAjMJBs')


# -----------------functions-----------------
def get_reset_token(user):
    s = Serializer(app.config['SECRET_KEY'])
    return s.dumps({'user_id':user})
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token,max_age=60)['user_id']
    except:
        return None
    return user_id
def send_reset_email(user):
    token  = get_reset_token(int(user[0]))
    msg = Message("Password Reset",sender='noreply@precise_extract.com',recipients=[user[1]])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token',token=token, _external=True)}

if you did not  make this request then simply  ignore this email !
'''
    mail.send(msg)
    

def saving_file(file,filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

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
            userid = str(uuid.uuid4().int)
            curr.execute(f"INSERT INTO `user`(`userid`, `email`, `password`) VALUES ('{userid}','{form1.email.data}','{hashed_password}')")
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
                session.permanent = form.remember.data
                session['loggedin'] = True
                session['userid'] = int(user[0])
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
    try:
        if session['loggedin'] == True:
            return redirect(url_for('home'))
    except KeyError:
        pass
        user = verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token')
            return redirect(url_for('login'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            curr = mysql.connection.cursor()
            hashed_password = bcrypt.generate_password_hash(form.confirm_new_password.data).decode('utf-8')
            curr.execute(f"UPDATE `user` SET `password`='{hashed_password}' WHERE `userid`='{user}'")
            mysql.connection.commit()
            curr.close()
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
    if session['loggedin'] == False:
        flash("Login to continue")
        return redirect(url_for('login'))
    return render_template('main.html')

#---------------------------upload files------------------
# @app.route("/upload_files/<tablename>",methods=['POST'])
# def upload_files(tablename):
#     if session['loggedin'] == False:
#         flash("login to continue")
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         for _file in request.files:
#             print(_file)
#             file = request.files[str(_file)]
#             filename = secure_filename(file.filename)
#             path = os.path.join(app.config['UPLOAD_FOLDER'],str(session['userid']),tablename)
#             #task = threading.Thread(target=saving_file,args=(file,filename))
#             if not os.path.exists(path):
#                 os.makedirs(path)
#             file.save(os.path.join(path,filename))
#             #task.start()
#             print(file.filename)
#         return jsonify({'msg':'files revcived successfully'}),200
    #     if 'files[]' not in request.files:
    #         return jsonify({"msg":"No files"}),400
    # files = request.files.getlist('files[]')
    # for file in files:

#------------------------- JWT for FASTAPI server--------------------------
@app.route("/get_token",methods=['GET'])
def get_token():
    if session['loggedin'] == False:
        flash("login to continue")
        print("not loggedin")
        return redirect(url_for('login'))
    # dt = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=30)
    payload = {"userid":str(session['userid']),"iat":datetime.datetime.now(datetime.timezone.utc)}
    token = jwt.encode(payload,app.config['SECRET_KEY'])
    token = jwe.encrypt(token,app.config['AES_SECRET_KEY'],algorithm='A256KW',encryption='A256GCM')
    # print(token.decode('ascii'))
    return jsonify({"token":token.decode('ascii')}),200



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/service")
def service():
    return render_template("sevice.html")

@app.route("/showtable/<token>",methods=['GET'])
def show_table(token):
    if session['loggedin'] == False:
        flash("login to continue")
        print("not loggedin")
        return redirect(url_for('login'))
    
    curr = mysql.connection.cursor()
    curr.execute(f"SELECT * FROM {token}")
    data = curr.fetchall()
    print(data)
    # dict = json.loads({
    #     "data":f"{data}",
    #     "msg":"sucess"
    # })
    return jsonpickle.encode({"data":f"{data}","message":"success"})


@app.route('/query/<token>',methods=['GET'])
def query(token):
    myquery = f'''CREATE TABLE `result` (`Date` VARCHAR(100)  NULL , `Instrument_Id` VARCHAR(100)  NULL , `Amount` DOUBLE(100,0)  NULL , `Type` VARCHAR(100) NOT NULL , `Balance` DOUBLE(100,0)  NULL , `Remarks` VARCHAR(200)  NULL )

    {token}
    generate an sql query for the user promt for above table , only generate userquery and no explanation, give the query in json form key = query
      '''
    model = genai.GenerativeModel('gemini-pro')
    response = json.loads(model.generate_content("myquery"))

    curr = mysql.connection.cursor()
    curr.execute(f"{response['query']}")
    data = curr.fetchall()
    dict = json.loads({
        "data":f"{data}",
        "msg":"sucess"
    })
    return jsonify({f"data":{data},"msg":"sucess"}),200

