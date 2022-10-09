from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/exit')
def logout():
    session.clear()
    return redirect('/')
    

@app.route('/register', methods=["POST"])
def register_user():
    #generar hash de pw ingresada
    if request.form["password"]!='':
        pw_hash=bcrypt.generate_password_hash(request.form["password"])
        #guardar booleano de si las pw y su confirmacion son iguales
        conf_pw =bcrypt.check_password_hash(pw_hash, request.form["conf_pw"])
    else:
        pw_hash=''
        conf_pw =''

    data = { "gen":''}
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash, #contrasena hasheada
        "gen":request.form["gen"],
        "birthday":request.form["birthday"]
    }

    #Realizar las dos validaciones, nombre y mail, no se solicito pw
    if (User.validation(data, conf_pw)):
        user_id = User.save(data)
        #siempre iniciar sesion despues de registrar
        session["user_id"] = user_id
        print("session", session)
        return redirect("/recipes")
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    pw_hash = bcrypt.generate_password_hash(request.form["log_password"])
    data={
        "email":request.form["log_email"],
        "password":pw_hash
    }
    if(User.login_mail_valid(data)):
        user = User.get_one(data)
        #booleano de validacion contrasenas
        saved_pw=user.password
        conf_pw = bcrypt.check_password_hash(saved_pw,request.form["log_password"])
        if conf_pw:        
            session['user_id']=user.id
            
            return redirect('/recipes')
        else:
            User.pw_login_error()   
    return redirect('/')

