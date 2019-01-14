# Flask ToDo app.


# Installation

Clone the repo:
`git clone https://github.com/pdybka-ep/flask-todoapp.git`

## Tech Stack
Development Language: Python
Web Framework: Flask
Database ORM: SQLAlchemy
Database: SQLITE

# Run tests: </br>
`nosetests -s`

# Routes Expossed: </br>
## User:</br>
`POST` /user/registration/ - Register a new user with username and password.</br>
`POST` /user/login/ - Login with the username and password as credentials. </br>
`POST` /token/refresh - Refresh access token for the user. </br>
`POST` /user/logout/ - Logs out the user. Revoking access token and refresh token.</br>

## ToDo:</br>
`POST` /user/todo/ - Creates a new TODO </br>
`GET` /user/todo/ - Get all todos for the user.</br>
`GET` /user/todo/1 - Get todo with given resource ID.</br>
`DELETE` /user/todo/1 - Delete todo with given resource ID.</br>

## DB Migration
export FLASK_APP=server.py
`flask db init`
`flask db migrate`
`flask db upgrade`

### Usage

```bash
docker build -t maxwell_todo:latest . && docker run --name maxwell_todo -d -p 8000:5000 --rm maxwell_todo:latest
```
