import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#def is_success_response(res,data):


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Example question for use in tests
        self.example_question = {
            'question': 'What is the largest ocean in the world?',
            'answer': 'Pacific Ocean',
            'difficulty': 1,
            'category': '3'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests
    """

    # Test that we get a response when trying to get categories
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(len(data['categories']))

    # Test that we get a response when trying to get a page of questions
    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions'])<=10)
        self.assertTrue(len(data['categories']))

    # Test what happens if we try to look for a page that is out of range
    def test_get_questions_page_not_found(self):
        res = self.client().get('/questions?page=9999')
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test what happens if we try to delete something that doesn't exist
    def test_delete_question_page_not_found(self):
        res = self.client().delete('/questions/9999')
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_and_delete_question_success(self):
        #Count what is in the database
        questions_initially = Question.query.all()

        res = self.client().post('/questions', json=self.example_question)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        question_id = data['created']

        #Count again and compare to baseline
        questions_created = Question.query.all()
        self.assertTrue(len(questions_created)>len(questions_initially))

        res_delete = self.client().delete('/questions/'+str(question_id))
        data_delete = json.loads(res_delete.data)

        #Check for successful deletion
        self.assertEqual(res_delete.status_code, 200)
        self.assertEqual(data_delete['success'], True)

        #Make sure we delete the right thing
        self.assertEqual(data_delete['deleted'], question_id)

        #Count again after delete and compare to previous counts
        questions_deleted = Question.query.all()
        self.assertTrue(len(questions_deleted)<len(questions_created))
        self.assertTrue(len(questions_deleted)==len(questions_initially))

        #Make sure the question we deleted doesn't exist
        question = Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(question, None)


    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()