# CITS3404_PROJ_2025
Group project for unit cits3404, designing a metrics app with comparitive analytics of productivity app usage and recreational app usage.


Here are the instructions for developing the project

1. Install the required dependencies:

``` shell
----IGNORE pip install -r requirements.txt -- DONT DO YET I NEED TO GET THE WHOLE LIST OF requirements first
```

### Database Setup
1. Initialise the Database Schema:
- run these 3 commands individually
``` shell
-- run this incase flask cant find 'app.py' : on CMD run in main folder :
'set FLASK_APP=app'

-- run below for db initialisation
flask db init
flask db migrate
flask db upgrade


if you changed the database schema then just run 
flask db migrate
flask db upgrade
```

## Running procrastinators
Now that all the dependencies are set up, you can now run the flask app.

To start the web-app, run the following:

``` shell
optional : python -m TEST 
the above will create 3 users for testing

to run the program:
flask run
```
This will host the application at http://127.0.0.1:5000




### Files

### `__init__.py`
Initialises the Flask app and sets up configurations

### `models.py`
Defines the data models (tables) 

### `routes.py`
Defines the routes of each page 

### `database.py`
Performs easy manipulation of the database
