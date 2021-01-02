# Full Stack API Final Project

## Full Stack Trivia

Trivia app project designed to teach the ability to structure plan, implement, and test an API - skills essential for enabling applications to communicate with others 

Please see the API documentation:
* [`API Documentation`](./backend/README.md#api-documentation)

The application has the following features:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## About the Stack

The project consists of separate frontend and backend applications.

### Backend

The `./backend` directory contains a Flask and SQLAlchemy server. In the project I worked primarily on defining the endpoints and in models.py for DB and SQLAlchemy setup. 

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a React frontend to consume the data from the Flask server. I updated the endpoints after defining them in the backend.

[View the README.md within ./frontend for more details.](./frontend/README.md)
