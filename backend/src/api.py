import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Controll-Allow-Headers',
                        'Content-Type, Authorization')
    response.headers.add('Access-Controll-Allow-Methods',
                        'GET, POST, PATCH, DELETE, OPTIONS')
    return response

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure

'''
@app.route('/drinks')
def getDrinks():
    result = {
        "success" : True,
        "drinks"  : [],
    }
    # nuevo = Drink(
    #     title = "New Drink",
    #     recipe =  '[{"color": "string", "name":"string", "parts":"1"}]'
    # )
    # nuevo.insert()
    # print(nuevo.title)
    try:
        drinks = Drink.query.all()
        for drink in drinks:
            result["drinks"].append(drink.short())

        return jsonify(result)
    except:
        abort(422)
        
    

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def getDrinksDetail(jwt):
    result = {
        "success" : True,
        "drinks"  : [],
    }

    try:
        drinks = Drink.query.all()
        for drink in drinks:
            result["drinks"].append(drink.long())
        return jsonify(result)
    except:
        abort(422)



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def addDrink(jwt):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    recipeStr = validateDrink(title, recipe)
    print(title, recipeStr)
    try:    
        newDrink = Drink(title=title, recipe=recipe)
        newDrink.insert()
        return jsonify({
            "status": 200,
            "success": True,
            "drinks" : [newDrink.long()]
        })
    except:
        abort(422)

'''
    Function to validate Drinks information
'''
def validateDrink(title, recipe):
    # Will return error if any of the required parameters is missing
    if title is None or recipe is None:
        abort(422)

    # Validate that the recipe is complete    
    if not isinstance(recipe,list) or len(recipe) == 0:
        abort(422)
    
    for ing in recipe:
        color = "color" not in ing
        name = "name" not in ing
        parts = "parts" not in ing

        if color and name and parts:
            abort(422)
    # Almost got crazy solving an error caused by having the wrong quotes :(
    return str(recipe).replace("'",'"')

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patchDrink(jwt, drink_id):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        
        if title is not None:
            drink.title = title
        if recipe is not None:
            recipeStr = validateDrink(title, recipe)
            drink.recipe = recipeStr
        drink.update()
        return jsonify({
            "success": True,
            "drinks" : [drink.long()]
        })

    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404) 
        drink.delete()
        return jsonify({
            "success": True,
            "delete" : drink_id
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@Completed implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def notFoundError(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "respurce not found"
                    }), 404


'''
@Completed implement error handler for AuthError
    error handler should conform to general task above 

    Reference for isinstance: https://stackoverflow.com/a/1303252
'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": error.description.error['description']
                    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": error.description.error['description']
                    }), 403
