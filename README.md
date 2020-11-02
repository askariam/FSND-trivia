# Full Stack Trivia API Project

This project is to build an API for Trivia Game that allows users to get quizzes testing their knowledge in 6 different categories. The project package contains the API backend and a frontend application in addition to a test package to build on Test Driven approach. The different functionalities offered by the API are:

1. Display questions in paginated format.
2. Display questions of a specific category.
3. Delete a question by its id.
4. Create a new question.
5. Search for question(s) using a search term.
6. Play the quiz.

## Getting Started

### Installing Dependencies

#### Frontend Dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

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

## API Reference

### Introduction

- Base URL: currently the API is not published online and can be used locally only on `http://localhost:5000/`
- Currently the API does not require authentication

### Endpoints

#### GET /questions
- General: returns paginated questions (10 per page)
- Sample: `curl --location --request GET 'http://localhost:5000/questions?page=2'`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
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
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 30
}
```

#### GET /categories

- General: returns all categories of the questions
- Sample: `curl --location --request GET 'http://localhost:5000/categories'`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /categories/<int:id>/questions

- General: returns questions for a specific category
- Sample: `curl --location --request GET 'http://localhost:5000/categories/6/questions'`

```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### DELETE /questions

- General: Delete a question by providing its id
- Sample: `curl --location --request DELETE 'http://localhost:5000/questions/74'`

```
{
  "deleted": 74,
  "success": true
}
```


#### POST /questions 

- General: add a new question to the game
- Sample:
```
url --location --request POST 'http://localhost:5000/questions' \
--data-raw '{
    "question": "API Questoin",
    "answer": "API Answer",
    "difficulty": 2,
    "category": 2
}'
```
```
{
  "created": 75,
  "success": true
}
```

### POST /questions

- General: search for question(s) using search term
- Sample:
```
curl --location --request POST 'http://localhost:5000/questions' \
--data-raw '{
    "searchTerm": "title"
}'
```
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 30
}
```


### POST /quizzes

- General: play the game and get randomized questions
- Sample: 
```
curl --location --request POST 'http://localhost:5000/quizzes' \
--data-raw '{
    "previous_questions": [13, 14],
    "quiz_category": {"type": "Geography", "id": "3"}
}'
```
```
{
  "question": {
    "answer": "API answer",
    "category": 3,
    "difficulty": 2,
    "id": 73,
    "question": "API question"
  },
  "success": true
}
```

### Error Handling
- The application returns 3 different types of errors: 400, 404, and 422
- Sample: `curl --location --request GET 'http://localhost:5000/questions?page=20'`
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

