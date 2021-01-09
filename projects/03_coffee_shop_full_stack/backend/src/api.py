import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

AUTH0_DOMAIN = 'udacity-segel.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'udacity-fsnd.segelmark.com'

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE MUST BE UNCOMMENTED ON FIRST RUN
'''

# db_drop_and_create_all()


@app.route('/photo')
@requires_auth('view:photo')
def headers(payload):
    print(payload)
    return 'Access Granted'

## ROUTES
@app.route('/drinks')
def retrieve_drinks():
    """Endpoint to get a list of all drinks
    
        Public endpoint
        Contain only the drink.short() data representation
        
        Returns status code 200 and json {"success": True, "drinks": drinks}
        or appropriate status code indicating reason for failure
    """
    try:
      drinks = Drink.query.all()
    except:
      abort(422)
    
    print(drinks)

    #Make sure we got some categories
    if not drinks:
      abort(404)

    #Return the categories
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks],
        })  

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_details(payload):
    """Endpoint to get a list of all drinks

        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        
        Returns status code 200 and json {"success": True, "drinks": drinks}
        or appropriate status code indicating reason for failure

    """
    try:
      drinks = Drink.query.all()
    except:
      abort(422)
    
    print(drinks)

    #Make sure we got some categories
    if not drinks:
      abort(404)

    #Return the categories
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks],
        })  

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    """ Endpoint to create a new drink

        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation

        Returns status code 200 and json {"success": True, "drinks": drink}
        or appropriate status code indicating reason for failure
    """

    body = request.get_json()
    print(body)

    # Check that we are getting the required fields
    if not ('title' in body and 'recipe' in body):
        abort(422) 

    drink = Drink(title=body.get('title', None),
                  recipe=json.dumps(body.get('recipe', None)))
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [ drink.long() ],
        })  

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload,drink_id):
    """ Endpoint to update an exsiting drink 
        
        where <id> is the existing model id
        
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    
        Returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """

    body = request.get_json()
    
    # Check that we are getting the required fields
    if not ('title' in body and 'recipe' in body):
        abort(422) 

    try:
        drink = Drink.query.get(drink_id)
    except:
        abort(422)

    if not drink:
        abort(404)

    drink.title=body.get('title', None)
    drink.recipe=json.dumps(body.get('recipe', None))
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [ drink.long() ],
        })  

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_question(payload,drink_id):
    """ Endpoint to DELETE drink using a question ID.
        where <id> is the existing model id

        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission

        Returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    try:
      drink = Drink.query.get(drink_id)
    except:
      abort(422)
    #Make sure the question we want to delete exists
    if not drink:
      abort(404)
    try:
      drink.delete()
    except:
      abort(422)
    return jsonify({
      'success': True,
      'deleted': drink_id
    })

## Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(400)
def error_bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(404)
def error_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

@app.errorhandler(422)
def error_unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
    }), 422


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

