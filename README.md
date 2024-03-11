## FITNESS TRACKER API
This is a REST API for a Fitness Tracking App built with FastAPI, SQLAlchemy and SQLlite. 


## ROUTES TO IMPLEMENT
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
|

## How to run the Project
- Install SQllite, SQLalchemy 
- Install Python
- Git clone the project
- Create your virtualenv with `conda create` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```
- Set Up your SQLlite database and set its URI in your ```database.py```
```
engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>',
    echo=True
)
```

- Create your database by running ``` python init_db.py ```
- Finally run the API
``` uvicorn main:app ``
