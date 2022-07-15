# Where we define our routes!
from flask_app import app # Needed for @app.route() among other things
from flask_app.models import animal, zoo # Import models
from flask import render_template, redirect, request, session # Import methods from Flask
import datetime

# Visible Routes - ZOOS
@app.route('/')
def zoos_root_redirect():
    return redirect('/zoos')

@app.route('/zoos')
def view_all_zoos():
    all_zoos = zoo.Zoo.get_all_zoos()
    return render_template('all_zoos.html', all_zoos=all_zoos)

@app.route('/zoos/new')
def add_zoo():
    return render_template('add_zoo_page.html')

@app.route('/zoos/<int:id>/view')
def view_one_zoo(id):
    data = {
        "id": id
    }
    one_zoo = zoo.Zoo.get_one_zoo(data)
    return render_template('/view_one_zoo.html', id=id, one_zoo=one_zoo)

@app.route('/zoos/<int:id>/edit')
def edit_zoo_page(id):
    data = {
        "id": id
    }
    one_zoo = zoo.Zoo.get_one_zoo(data)
    return render_template('/edit_zoo_page.html', id=id, one_zoo=one_zoo)




# Hidden Routes
@app.route('/process_add_zoo', methods=['POST'])
def process_add_zoo():
    data = {
        "name": request.form['name'],
        "city": request.form['city'],
        "size_acres": request.form['size_acres'],
        "visitor_capacity": request.form['visitor_capacity'],
        "opening_date": request.form['opening_date']
    }

    # Call on model file to send DB query
    zoo.Zoo.add_zoo(data)
    return redirect('/zoos')

@app.route('/zoos/<int:id>/process_edit_zoo', methods=['POST'])
def process_edit_zoo(id):
    data = {
        "id": id,
        "name": request.form['name'],
        "city": request.form['city'],
        "size_acres": request.form['size_acres'],
        "visitor_capacity": request.form['visitor_capacity'],
        "opening_date": request.form['opening_date']
    }

    zoo.Zoo.edit_zoo(data)
    return redirect(f"/zoos/{id}/view")

@app.route('/zoos/<int:id>/delete')
def delete_zoo(id):
    data = {
        "id": id
    }
    # Add function in zoo model to delete zoo w/ given ID; call that function here
    zoo.Zoo.delete_zoo(data)
    # zoo.Zoo.reset_ids()
    return redirect('/zoos')