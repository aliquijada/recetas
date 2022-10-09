from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def recipes():
    if "user_id" not in session:
        return redirect('/')
    data={
        "user_id":session["user_id"]
        }
    return render_template("recipes.html", user = User.get_by_id(data), recetas = Recipe.get_recipes_with_user())


@app.route('/recipes/new')
def new_recipe():
    if "user_id" not in session:
        return redirect('/')
    return render_template("new_recipe.html")

@app.route('/recipe/val', methods=["POST"])
def recipe_validation():
    data = {
        "user_id":request.form["user_id"],
        "name":request.form["name"],
        "description":request.form["description"],
        "instruction":request.form["instruction"],
        "date_cooked":request.form["date_cooked"],
        "under":request.form["under"]
    }
    print("#"*15)
    print(data)
    if Recipe.val_rec(data):
        receta = Recipe.save(data)
        return redirect('/recipes')
    return redirect('/recipes/new')

@app.route('/recipes/<int:id>')
def show_info_recipe(id):
    data ={
        "id":id,
        "user_id":session["user_id"]
    }
    receta = Recipe.get_by_id(data)
    user_data = {
        "user_id":receta.user_id
    }
    post_user = User.get_by_id(user_data)
    return render_template("receta_info.html",user =User.get_by_id(data), receta=receta, post_user = post_user)

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data ={
        "id":id
    }
    Recipe.delete(data)
    return redirect('/recipes')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    data={
        "id":id
    }
    receta = Recipe.get_by_id(data)
    return render_template("edit_recipe.html", receta=receta)
    Recipe.edit(data)

@app.route('/recipe/update' , methods=["POST"])
def editar():
    data = {
        "id": request.form["recipe_id"],
        "name":request.form["name"],
        "description":request.form["description"],
        "instruction":request.form["instruction"],
        "date_cooked":request.form["date_cooked"],
        "under":request.form["under"]
    }
    Recipe.editar_receta(data)
    return redirect('/recipes')
