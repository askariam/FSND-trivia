import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10 #configure questions per page

# this will paginate questions
# request is the request object from the http call. selection is the big list to be paginated
def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start_index = (page - 1) * QUESTIONS_PER_PAGE # index of first item in the page
  end_index = start_index + QUESTIONS_PER_PAGE #index of the last item in the page

  #format the list
  items = [item.format() for item in selection]
  page_items = items[start_index:end_index]

  return page_items

def create_app(test_config=None):
  # create and configure the app
  # this method will return app at the end
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app, resources={r"/api/*": {"origins": "*"}}) // from the course slides
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response # we need to return te response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    # abort if no categories in db
    if not categories:
      abort(404)

    # if we found categories, return the json response
    return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
            })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    total_questinos = len(questions)
    page_questions = paginate(request, questions)
    print(request)
    if not page_questions:
      abort(404)
    categories = Category.query.all()

    return jsonify(
      {
        'success': True,
        'questions': page_questions,
        'total_questions' : total_questinos,
        'categories': {category.id: category.type for category in categories},
        'current_category': None # all categories
      }
    )

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id

      })
    except Exception as e:
      abort(404)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


  # This end point will handle both search and adding new question
  @app.route('/questions', methods=['POST'])
  def post_question():
    data = request.get_json()
    search_term = data.get('searchTerm')
    if search_term is None:
      question = data.get('question')
      answer = data.get('answer')
      difficulty = data.get('difficulty')
      category = data.get('category')

      if question is None or answer is None or difficulty is None or category is None:
        abort(400)
      
      if question == '' or answer == '' or difficulty ==  '' or category == '':
        abort(400)

      try:
        new_question = Question(question=question, answer=answer,
                              difficulty=difficulty, category=category)
        new_question.insert()

        return jsonify({
          'success': True,
          'created': new_question.id
        })
      except expression as identifier:
        abort(422)
    else:
      if search_term == '':
        abort(400)
      selection = Question.query.filter(
          Question.question.ilike(f'%{search_term}%')
        ).all()
      total_questinos = Question.query.count()
      
      if selection:
        page_questions = paginate(request, selection)
        return jsonify({
          'success': True,
          'questions': page_questions,
          'total_questions': total_questinos
        })
      
      else:
        abort(404)




  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questinos_by_category(category_id):
    current_category = Category.query.get(category_id) # get the selected category
    str_id = str(category_id)
    try:
      questions = Question.query.filter_by(category=str_id).all()
      page_questions = paginate(request, questions)
      total_questinos = len(questions)
      return jsonify(
        {
          'success': True,
          'questions': page_questions,
          'total_questions' : total_questinos,
          'current_category':  current_category.id
        }
      )
    except Exception as e:
      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    category = data.get('quiz_category')
    if category:
      category_id = category['id']
    else:
      abort(400)

    if category_id == 0:
      question_bank = Question.query.all()
    
    else:
      question_bank = Question.query.filter_by(category=category_id).all()

    for q in previous_questions:
      for b in question_bank:
        if b.id == q:
          question_bank.remove(b)

    
    if question_bank:
      new_question = question_bank[random.randint(0, len(question_bank)-1)]
    else:
      abort(404)


    return jsonify(
      {
        'success': True,
        'question': new_question.format()
      }
    )

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400
  
  return app

    