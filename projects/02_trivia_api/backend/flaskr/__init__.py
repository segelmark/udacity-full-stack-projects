import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

ENTRIES_PER_PAGE=10

#Formats categories correctly
def format_entities(entities):
  return [entity.format() for entity in entities]

#paginates all entries returning the right page for a certain entries per page
def paginate(entries,page,entries_per_page):
  start =  (page - 1) * entries_per_page
  end = start + entries_per_page
  return entries[start:end]

#paginates a selecation for the right number of pages given by the get request argument
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  entries = format_entities(selection)
  return paginate(entries,page,ENTRIES_PER_PAGE)


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={r"/*": {"origins": "*"}})

  # CORS Headers - Setting access control allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  #Endpoint to handle GET requests for all available categories
  @app.route('/categories')
  def retrieve_categories():
    try:
      categories = Category.query.order_by(Category.id).all()
    except:
      abort(422)
    
    #Make sure we got some categories
    if len(categories) == 0:
      abort(404)

    #Return the categories
    return jsonify({
      'success': True,
      'categories': format_entities(categories),
    })


  #Endpoint to handle GET requests for all questions paginated (10 questions)
  @app.route('/questions')
  def retrieve_questions():
    try:
      questions = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
    except:
      abort(422)
    
    #Paginate list of questions and make sure it is a valid page
    questions_paginated = paginate_questions(request, questions)
    if len(questions_paginated) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions_paginated,
      'categories': format_entities(categories),
      'total_questions': len(questions),
      'current_category': None
    })


  #Endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
    except:
      abort(422)
    #Make sure the question we want to delete exists
    if not question:
      abort(404)
    try:
      question.delete()
    except:
      abort(422)
    return jsonify({
      'success': True,
      'deleted': question_id
    })


  #Endpoint to POST a new question, 
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    try:
      question = Question(question=new_question, answer=new_answer,
                          difficulty=new_difficulty, category=new_category)
      question.insert()
      return jsonify({
        'success': True,
        'created': question.id,
      })
    except:
      abort(422)        

  #Endpoint to get questions based on a search term. 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      body = request.get_json()
      search_term = body.get('searchTerm', None)

      if not search_term:
        abort(404)

      search_result = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')
      ).all()

      return jsonify({
        'success': True,
        'questions': paginate_questions(request, search_result),
        'total_questions': len(search_result),
        'current_category': None
      })
    except:
      abort(422)

  # Endpoint to handle GET requests for questions in a certain category
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    try:
      questions = Question.query.filter_by(
        category=category_id
        ).order_by(Question.id).all()
      categories = Category.query.order_by(Category.type).all()

      if len(questions) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'questions': paginate_questions(request, questions),
        'categories': format_entities(categories),
        'total_questions': len(questions),
        'current_category': category_id
      })
    except:
      abort(422)

  #POST endpoint to get questions to play the quiz
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      body = request.get_json()
      if not ('quiz_category' in body and 'previous_questions' in body):
        abort(422)
      category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')

      if category['type'] == 'click':
        new_question = Question.query.filter(
          Question.id.notin_((previous_questions))
        ).all()
      else:
        new_question = Question.query.filter_by(
          category=(int(category['id']))
        ).filter(Question.id.notin_((previous_questions))).all()

      return jsonify({
        'success': True,
        'question': random.choice(new_question).format() if new_question else None,
      })
    except:
      abort(422)
  
  #Error handlers for all expected errors 

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
  
  return app

    