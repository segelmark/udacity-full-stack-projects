# Full Stack Trivia API Backend

The Full Stack Trivia is offered to you as a RESTful API running on a Python based FLASK server.

Follow below instruction or head down to the [API documentation](#api-documentation) to see what this powerful Trivia API is capable of.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Activate  virtual environment by writing:

source env/bin/activate (on Mac or Linux - see docs for Windows instructions)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Documentation

This describes the resources that make up the official Full Stack Trivia API, which allows for easy integration of the trivia functionality into any web or mobile application.

## Endpoints
* GET '/categories'
* GET '/questions?page={page_number}'
* POST '/questions'
* DELETE '/questions/{question_id}'
* POST '/questions/search'
* GET '/categories/{category_id}/questions'
* POST '/quizzes'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with key "categories" containing an array of objects with key "id": Int and "type": String 
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    ...
  ], 
  "success": true
}
```

### Get '/questions?page={page_number}'
- Fetches a list of questions for all categories paginated with 10 questions per page
- Request Arguments:
  - Query string params: Page number as Integer (optional - defaults to page = 1)
- Returns: An object with keys "categories" (same as above), "current_category": null, "total questions": Int, and "questions" containing an array of objects with keys "answer", "category": Int, "difficulty": Int (1-5), "id": Int, "question": String
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    ...
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}
```

### POST '/questions/'
- Creates a new question
- Request Arguments:
  - Body: JSON Object containing "question": String, "answer": String, "difficulty": Int (1-5), "category": Int
```
{
    "question": "What is the best basketball player of all time?",
    "answer": "Michael Jordan",
    "difficulty": 1
    "category": 4
}
```

- Returns: Object with "created": Int
```
{
  "success": True,
  "created": question_id
}
```

### DELETE '/questions/{question_id}'
- Deletes question with question_id from database
- Request Arguments:
  - URL Params: Question ID as Int
- Returns: Object with 'deleted': Int
```
{
  "success": True,
  "deleted": question_id
}
```

### POST '/questions/search'
- Fetches a list of questions for a given search term among all categories paginated with 10 questions per page
- Request Arguments:
  - Query string params: Page number as Integer (optional - defaults to page = 1)
  - Body: JSON object with "search_tern": String
```
{
  "search_term": "Apollo 13",
}
```
- Returns: An object with keys "current_category": null, "total questions": Int, and "questions" containing an array of objects with keys "answer", "category": Int, "difficulty": Int, "id": Int, "question": String
```
{
  "success": true, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
  ], 
  "total_questions": 19
  "current_category": null, 
}
```

### GET '/categories/{category_id}/questions'
- Fetches a list of all questions for a particular category
- Request Arguments:
  - Query string params: Category id as Integer
- Returns: An object with keys "categories" (same as above), "current_category": null, "total questions": Int, and "questions" containing an array of objects with keys "answer", "category": Int, "difficulty": Int, "id": Int, "question": String
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    ...
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}
```

### POST '/quizzes'
- Fetches question to play the quiz
- Request Arguments:
  - Body: JSON object with "previous_questions": Array of Integers, "quiz_category": JSON object with "type": String, "id": Int
```
{
  "previous_questions":[],
  "quiz_category":{"type":null,"id":0}
}
```
- Returns: A JSON object with key "question" containing an object with "answer": String, "category": Integer, "difficulty": Integer, "id": Integer, "question": String
```
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```

## Status Codes

Trivia API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `Success` |
| 400 | `Bad Request` |
| 404 | `Resource Not Found` |
| 422 | `Unprocessable Entity` |

For all status codes a JSON object is included with a "success": Boolean and the correct data or error code and message.

```
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}
```