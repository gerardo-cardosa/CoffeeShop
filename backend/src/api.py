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
def getDrinksDetail():
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
def addDrink():
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

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
    # try:
    
    recipeStr = str(recipe).replace("'",'"')
    print('New ====================================== ',recipeStr)
    newDrink = Drink(title=title, recipe=recipeStr)
    newDrink.insert()
    return jsonify({
        "success": True,
        "drinks" : [newDrink.long()]
    })
    # except:
    #     abort(422)



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
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "respurce not found"
                    }), 404


'''
@Completed implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401
