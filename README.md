# CITS3404_PROJ_2025
Group project for CITS3403 Agile Web Development, designing a metrics app with comparitive analytics of productivity app usage and recreational app usage.

| Student ID | Name | Github Username
| -------- | :------- |-------|
| 23164443 | Julie Salazar Franco | Julie-Salazar
| 23664629 | Yusuke Matsuki | Daimy0u
| 24109459 | Lyla Peng | seventhirty233
| 23655195 | Zac Morris | ozzy1323232


# Installation
To get started, here's how to install and run the flask application.

> [!IMPORTANT]
> Make sure you are in the correct directory before continuing. Run `cd </path/to/procrastinatrics>`, replacing the path with the project file location.

### 1. Install the required dependencies
Before starting, make sure you have installed Python 3.12 in your system.

Then, install all required dependencies by running:
``` shell
pip install -r requirements.txt
```

### 2. Initialise the Database Schema
For first time running, database initialisation will need to be done via the command:
``` shell
flask db init
```
``` shell
flask db migrate
```
``` shell
flask db upgrade
```
> [!CAUTION]
> Its important to run `flask db migrate` and `flask db upgrade` whenever important schema changes are made to the database. This is to ensure the changes are reflected in the web application.

### 3. Running the App
Now that all the dependencies are set up, you can now run the flask app.

To start the web-app, run the following:

``` shell
flask run
```

This will host the application at `http://127.0.0.1:5000`.

# Testing
Conventionally, you may test the features by accessing and signing up a user via `http://127.0.0.1:5000`.

But for more in-depth testing, we have already implemented testcases via [pytest-flask](https://pypi.org/project/pytest-flask/), which you can run simply by running:
```shell
pytest
```
