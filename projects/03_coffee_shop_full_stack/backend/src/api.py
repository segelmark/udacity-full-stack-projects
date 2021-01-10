import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# import requests

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

# ROUTES


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
    except Exception:
        abort(422)

    print(drinks)

    # Make sure we got some categories
    if not drinks:
        abort(404)

    # Return the categories
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks],
        })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_details(payload):
    """
        Endpoint to get a list of all drinks

        Requires the 'get:drinks-detail' permission
        Contains the drink.long() data representation

        Returns status code 200 and json {"success": True, "drinks": drinks}
        or appropriate status code indicating reason for failure

    """
    try:
        drinks = Drink.query.all()
    except Exception:
        abort(422)

    print(drinks)

    # Make sure we got some categories
    if not drinks:
        abort(404)

    # Return the categories
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks],
        })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    """
        Endpoint to create a new drink

        Creates a new row in the drinks table
        Requires the 'post:drinks' permission
        Contains the drink.long() data representation

        Returns status code 200 and json {"success": True, "drinks": drink}
        or appropriate status code indicating reason for failure
    """

    body = request.get_json()
    print(body)

    # Check that we are getting the required fields
    if not ('title' in body and 'recipe' in body):
        abort(422)

    recipe = body.get('recipe', None)
    if not isinstance(recipe, list):
        recipe = [recipe]

    drink = Drink(title=body.get('title', None),
                  recipe=json.dumps(recipe))
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [drink.long()],
        })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    """
        Endpoint to update an exsiting drink
        where <id> is the existing model id

        Responds with a 404 error if <id> is not found
        Updates the corresponding row for <id>
        Requires the 'patch:drinks' permission
        Contains the drink.long() data representation

        Returns status code 200 and json {"success": True, "drinks": drink}
        or appropriate status code indicating reason for failure
    """

    body = request.get_json()

    # Check that we are getting the required fields
    if not ('title' in body or 'recipe' in body):
        abort(422)

    try:
        drink = Drink.query.get(drink_id)
    except Exception:
        abort(422)

    if not drink:
        abort(404)

    if 'title' in body:
        drink.title = body.get('title', None)
    if 'recipe' in body:
        drink.recipe = json.dumps(body.get('recipe', None))
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long()],
        })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_question(payload, drink_id):
    """
        Endpoint to DELETE drink using a question ID.
        where <id> is the existing model id

        Responds with a 404 error if <id> is not found
        Deletes the corresponding row for <id>
        Requires the 'delete:drinks' permission

        Returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    try:
        drink = Drink.query.get(drink_id)
    except Exception:
        abort(422)
    # Make sure the question we want to delete exists
    if not drink:
        abort(404)
    try:
        drink.delete()
    except Exception:
        abort(422)
    return jsonify({
      'success': True,
      'deleted': drink_id
    })


# User management

@app.route('/users/')
@requires_auth('get:users')
def get_users(payload):
    """
        Endpoint see all users

        Requires the 'users:view' permission

        Returns status code 200 and json {"success": True, "users": users}
        or appropriate status code indicating reason for failure
    """
    # r = requests.get('https://udacity-segel.eu.auth0.com/api/v2/users', headers={'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkV0dGFDa0h4dUFXaUI0UlBoejJKTyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktc2VnZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6InVndTRZUzE3SVJoNVdOMEozNGl0aE1CbDBPN1pYRXVOQGNsaWVudHMiLCJhdWQiOiJodHRwczovL3VkYWNpdHktc2VnZWwuZXUuYXV0aDAuY29tL2FwaS92Mi8iLCJpYXQiOjE2MTAyNjk3NzYsImV4cCI6MTYxMDM1NjE3NiwiYXpwIjoidWd1NFlTMTdJUmg1V04wSjM0aXRoTUJsME83WlhFdU4iLCJzY29wZSI6InJlYWQ6Y2xpZW50X2dyYW50cyBjcmVhdGU6Y2xpZW50X2dyYW50cyBkZWxldGU6Y2xpZW50X2dyYW50cyB1cGRhdGU6Y2xpZW50X2dyYW50cyByZWFkOnVzZXJzIHVwZGF0ZTp1c2VycyBkZWxldGU6dXNlcnMgY3JlYXRlOnVzZXJzIHJlYWQ6dXNlcnNfYXBwX21ldGFkYXRhIHVwZGF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgZGVsZXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBjcmVhdGU6dXNlcnNfYXBwX21ldGFkYXRhIHJlYWQ6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX2N1c3RvbV9ibG9ja3MgZGVsZXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl90aWNrZXRzIHJlYWQ6Y2xpZW50cyB1cGRhdGU6Y2xpZW50cyBkZWxldGU6Y2xpZW50cyBjcmVhdGU6Y2xpZW50cyByZWFkOmNsaWVudF9rZXlzIHVwZGF0ZTpjbGllbnRfa2V5cyBkZWxldGU6Y2xpZW50X2tleXMgY3JlYXRlOmNsaWVudF9rZXlzIHJlYWQ6Y29ubmVjdGlvbnMgdXBkYXRlOmNvbm5lY3Rpb25zIGRlbGV0ZTpjb25uZWN0aW9ucyBjcmVhdGU6Y29ubmVjdGlvbnMgcmVhZDpyZXNvdXJjZV9zZXJ2ZXJzIHVwZGF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGRlbGV0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGNyZWF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIHJlYWQ6ZGV2aWNlX2NyZWRlbnRpYWxzIHVwZGF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgZGVsZXRlOmRldmljZV9jcmVkZW50aWFscyBjcmVhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIHJlYWQ6cnVsZXMgdXBkYXRlOnJ1bGVzIGRlbGV0ZTpydWxlcyBjcmVhdGU6cnVsZXMgcmVhZDpydWxlc19jb25maWdzIHVwZGF0ZTpydWxlc19jb25maWdzIGRlbGV0ZTpydWxlc19jb25maWdzIHJlYWQ6aG9va3MgdXBkYXRlOmhvb2tzIGRlbGV0ZTpob29rcyBjcmVhdGU6aG9va3MgcmVhZDphY3Rpb25zIHVwZGF0ZTphY3Rpb25zIGRlbGV0ZTphY3Rpb25zIGNyZWF0ZTphY3Rpb25zIHJlYWQ6ZW1haWxfcHJvdmlkZXIgdXBkYXRlOmVtYWlsX3Byb3ZpZGVyIGRlbGV0ZTplbWFpbF9wcm92aWRlciBjcmVhdGU6ZW1haWxfcHJvdmlkZXIgYmxhY2tsaXN0OnRva2VucyByZWFkOnN0YXRzIHJlYWQ6dGVuYW50X3NldHRpbmdzIHVwZGF0ZTp0ZW5hbnRfc2V0dGluZ3MgcmVhZDpsb2dzIHJlYWQ6bG9nc191c2VycyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgdXBkYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgdXBkYXRlOmN1c3RvbV9kb21haW5zIHJlYWQ6ZW1haWxfdGVtcGxhdGVzIGNyZWF0ZTplbWFpbF90ZW1wbGF0ZXMgdXBkYXRlOmVtYWlsX3RlbXBsYXRlcyByZWFkOm1mYV9wb2xpY2llcyB1cGRhdGU6bWZhX3BvbGljaWVzIHJlYWQ6cm9sZXMgY3JlYXRlOnJvbGVzIGRlbGV0ZTpyb2xlcyB1cGRhdGU6cm9sZXMgcmVhZDpwcm9tcHRzIHVwZGF0ZTpwcm9tcHRzIHJlYWQ6YnJhbmRpbmcgdXBkYXRlOmJyYW5kaW5nIGRlbGV0ZTpicmFuZGluZyByZWFkOmxvZ19zdHJlYW1zIGNyZWF0ZTpsb2dfc3RyZWFtcyBkZWxldGU6bG9nX3N0cmVhbXMgdXBkYXRlOmxvZ19zdHJlYW1zIGNyZWF0ZTpzaWduaW5nX2tleXMgcmVhZDpzaWduaW5nX2tleXMgdXBkYXRlOnNpZ25pbmdfa2V5cyByZWFkOmxpbWl0cyB1cGRhdGU6bGltaXRzIGNyZWF0ZTpyb2xlX21lbWJlcnMgcmVhZDpyb2xlX21lbWJlcnMgZGVsZXRlOnJvbGVfbWVtYmVycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.q6q8_UZm-Zz71hV2tiGAytPfzgRPRQk1H6DzMSUrQeCqacyXh2qhgy0J6-JGMpTUvF6_sUp6mTD0BugrSI7BX8wf_mx_YwJo9uOBxiYCy2-nDPF5pbTUZbvpXXM4IVBPgaitwed2Yr0_d8O3cNjuvR1BeogFUmkUBEQnc7x5j3N2srF84LjgYMnDm09CFCF22UtW0AkiVwwcDokXsKPIH_Y1xahMquIPzZdkg6XWXHYRXzVjz7LkQIIu28cia76Lq8Y8XOMYvGWXE87dFNOAogNkBDNgXMIkCDu9k2h4KJMF5uxVBFIXXnwHkR6EvPSpeCIH4LrFzpZi7A2107CBrw'}, timeout=1)
    return jsonify({
      'success': True,
      'users': r.json()
    })


# Error Handling

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
