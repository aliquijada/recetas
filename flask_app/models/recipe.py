from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models.user import User

db = 'receta'
class Recipe:

    def __init__(self, data):
        self.id=data["id"]
        self.user_id=data["user_id"]
        self.name = data["name"]
        self.under = data["under"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.date_cooked = data["date_cooked"]
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.usuario = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recetas (user_id, name, under, description, instruction, date_cooked) VALUES (%(user_id)s, %(name)s, %(under)s, %(description)s, %(instruction)s, %(date_cooked)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * from recetas;"
        results = connectToMySQL(db).query_db(query)
        recetas =[]
        for row in results:
            recetas.append(cls(row))
        return recetas

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from recetas WHERE id = (%(id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_recipes_with_user(cls):
        query="SELECT * from recetas LEFT JOIN users on users.id = recetas.user_id"
        results = connectToMySQL(db).query_db(query)
        todas_las_recetas = []
        for receta in results:
            objeto_receta = cls(receta)
            objeto_receta.usuario.append(User(receta))
            todas_las_recetas.append(objeto_receta)

        #print(type(todas_las_recetas[0].usuario[0]))
        #print(todas_las_recetas[1].usuario[0].__dict__)
        return todas_las_recetas

    @classmethod
    def delete(cls, data):
        query="DELETE from recetas WHERE id = (%(id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def val_rec(cls,data):
        is_valid=True
        #Nombre de al menos 3 caracteres
        if (len(data["name"])<2):
            flash("El nombre debe tener al menos 3 letras")
            is_valid=False
        if(len(data["description"])<2):
            flash("La descripcion debe tener al menos 3 letras")
            is_valid=False
        if(len(data["instruction"])<2):
            flash("La instruccion debe tener al menos 3 letras")
            is_valid=False
        if(len(data["date_cooked"])==0):
            flash("Debe ingresar una fecha de cocina")
            is_valid=False
        return is_valid

    @classmethod
    def editar_receta(cls,data):
        query = "UPDATE recetas SET name = %(name)s, description=%(description)s, instruction=%(instruction)s, date_cooked=%(date_cooked)s, under = %(under)s WHERE id=%(id)s"
        return connectToMySQL(db).query_db(query, data)

    # @classmethod
    # def get_by_user(cls,data):
    #     query="SELECT * from users LEFT JOIN recetas on recetas.users_id = users.id WHERE users.id= %(id)s;"
    #     results =connectToMySQL(db).query_db(query, data) 
    #     user = cls(results[0])
    #     for row in results:
    #         receta_data ={
    #             "id": row["recetas.id"],
    #             "name":row["name"],
    #             "under":row["under"],
    #             "description":row["description"],
    #             "instruction": row["instruction"],
    #             "created_at":row["recetas.created_at"],
    #             "updated_at":row["recetas.updated_at"]
    #         }
    #         user.recetas.append(recipe.Recipe)
