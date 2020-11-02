import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


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
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test getting questions - normal flow
    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10) # for first page only
        self.assertTrue(data['current_category'] == None) # for ALL or data['current_category'] in [1,2,3,4,5,6] )


    # test getting categories - normal flow
    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']) == 6)

    # test out of range pages
    def test_out_of_range_page_error(self):
        result = self.client().get('/questinos?page=10') # page 10 does not exist in test database
        data = json.loads(result.data)

        self.assertTrue(result.status_code == 404)
        self.assertFalse(data['success'])  
        self.assertEqual(data['message'], 'resource not found')
    
    # test successful question add - normal flow
    def test_successful_question_add(self):
        test_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 2
        }

        # first step: get total questions before insert
        result_read = self.client().get('/questions')
        data_read = json.loads(result_read.data)
        total_questions1 = data_read['total_questions']

        # second: create a new questions
        result = self.client().post('/questions', json=test_question) 
        data = json.loads(result.data)

        # third: get total questions after insert
        result_read = self.client().get('/questions')
        data_read = json.loads(result_read.data)
        total_questions2 = data_read['total_questions']

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertEqual(total_questions2, total_questions1 + 1)

    # test invalid question add
    def test_invalid_question_add(self):
        test_question = {
        
        }

        # create a new questions
        result = self.client().post('/questions', json=test_question) 
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # test invalid question add another scenario
    def test_invalid_question_add2(self):
        test_question = {
            'question': '',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 2
        }

        # create a new questions
        result = self.client().post('/questions', json=test_question) 
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # test delete a question - normal flow
    def test_successful_question_delete(self):
        test_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 2
        }

        # first: add a new questions to be deleted later
        result = self.client().post('/questions', json=test_question) 
        data = json.loads(result.data)

        # get the question id
        created = data['created']

        # second: delete the question
        result = self.client().delete('/questions/{}'.format(created)) 
        data = json.loads(result.data)
        
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(created, data['deleted'])

    # test delete invalid question id
    def test_invalid_question_delete(self):

        # try to delete invalid id questions
        result = self.client().delete('/questions/{}'.format(1000))  # 1000 does not exist in test data
        data = json.loads(result.data)
       
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # test get questions by category - normal flow
    def test_get_category_questions(self):
        result = self.client().get('/categories/{}/questions'.format(3)) # category 3 for testing only
        data = json.loads(result.data)

        right_category = True
        for question in data['questions']:
            if not question['category'] == 3:
                right_category = False


        self.assertEqual(result.status_code, 200)
        self.assertTrue(right_category)
        self.assertEqual(data['current_category'], 3)

    
    # test get questions by category - invalid category
    def test_get_invalid_category_questions(self):
        result = self.client().get('/categories/{}/questions'.format(8)) # category 8 does not exist
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    
    # test successful question search - normal flow
    def test_successful_question_search(self):
        test_search = {
            'searchTerm': 'title'
        }

        # call the search endpoint
        result = self.client().post('/questions', json=test_search) 
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 2)


    # test invalid question search
    def test_invalid_question_search(self):
        test_search = {
        }

        # call the search endpoint
        result = self.client().post('/questions', json=test_search) 
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # test blank question search
    def test_blank_question_search(self):
        test_search = {
            'searchTerm': ''
        }

        # call the search endpoint
        result = self.client().post('/questions', json=test_search) 
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # test play quiz - normal flow
    def test_play_quiz(self):
        mock_quiz = {
            'previous_questions': [13, 14],
            'quiz_category': {'type': 'Geography', 'id': '3'}

        }

        result = self.client().post('quizzes', json=mock_quiz)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 3)
        self.assertNotIn(data['question']['id'], [13, 14])

    # test invalid play quiz
    def test_invalid_play_quiz(self):
        mock_quiz = {
            'previous_questions': [13, 14],
            'quiz_category': {}
        }

        result = self.client().post('quizzes', json=mock_quiz)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()