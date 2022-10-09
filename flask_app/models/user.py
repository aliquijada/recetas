from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'receta'
class User:
    
    
    def __init__(self,data):
        self.id = data["id"]
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.gen=data['gen']
        self.birthday = data["birthday"]
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls,data):
        query ="INSERT INTO users (first_name, last_name, email, password, gen, birthday) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(gen)s, %(birthday)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * from users WHERE email = (%(email)s)"
        results= connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):        
        query = "SELECT * from users WHERE id = (%(user_id)s)"
        results= connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validation(data, conf_pw):
        #validacion de mail y apellido
        is_valid=True

        #no necesario si se utiliza requested en input de formulario
        # if (len(data['first_name'])==0) or (len(data['last_name'])==0) or (len(data['password'])==0) or (len(data['email'])==0) :
        #     flash("Por favor complete los campos obligatorios")
        #     is_valid=False 
        if len(data['first_name'])<2:
            flash("El nombre debe tener al menos 2 caracteres")
            is_valid=False
        if len(data['last_name'])<2:
            flash("El apellido debe tener al menos 2 caracteres")
            is_valid=False
        if not conf_pw:
            flash("Las constrasenas deben coincidir")
            is_valid=False
        ## validacion de mail
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        ## formato de mail
        if not EMAIL_REGEX.match(data["email"]):
            flash("Mail no valido")
            is_valid=False 
        ## mail existente en BBDD
        if len(results)>1:
            flash("Mail ya se encuentra registrado")
            is_valid=False
        #################################################
        ##          OTRAS VALIDACIONES                 ##
        #################################################
        # if not (name['first_name'].isalpha()):
        #     flash("El nombre debe tener solo letras")
        #     is_valid=False
        # if not (name['last_name'].isalpha()):
        #     flash("El apellido debe tener solo letras")
        #     is_valid=False
        
        return is_valid

    @staticmethod
    def login_mail_valid(email):
        is_valid = True
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,email)
        ## formato de mail
        if not EMAIL_REGEX.match(email["email"]):
            flash("Mail no valido")
            is_valid=False 
        ## mail existente en BBDD
        if len(results)<1:
            flash("No se encuentra mail, por favor registrar")
            is_valid=False
        return is_valid

    @staticmethod
    def pw_login_error():
        flash("Contrasena incorrecta")
        return 

    @staticmethod
    def login_validation():
        is_valid = True
        booleano = "user_id" in session
        print("#"*15)
        print(booleano)
        if not "user_id" in session:
            print("No esta la clave")
            is_valid=False
            flash("Por favor ingresa a tu cuenta o registrate")
        return is_valid

    # @staticmethod
    # def pw_validation(pw):
    #     #primero validaremos la contrasena
    #     is_valid = True
    #     if len(pw)<8:
    #         flash("La contrasena debe tener al menos 8 caracteres")
    #         is_valid=False
    #     if not any(char.isdigit() for char in pw):
    #         flash("La constrasena debe contener al menos un numero")
    #         is_valid=False
    #     if not any(char.isupper() for char in pw):
    #         flash("La constrasena debe contener al menos una mayuscula")
    #         is_valid=False
    #     return is_valid