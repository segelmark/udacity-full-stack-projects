# Full Stack Trivia API Backend

The Full Stack Trivia is offered to you as a RESTful API running on a Python based FLASK server.

Follow below instruction or head down to the (API documentation)[#api-documentation] to see what this powerful Trivia API is capable of.

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
- Returns: An object with keys "categories" (same as above), "current_category": null, "total questions": Int, and "questions" containing an array of objects with keys "answer", "category": String, "difficulty": Int, "id": Int, "question": String
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
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": "5", 
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


### DELETE '/questions/{question_id}'
- Deletes question with question_id from database
- Request Arguments:
  - URL Params: Question ID as Integer
- Returns: Object with 'deleted': question_id
```
{
  'success': True,
  'deleted': question_id
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