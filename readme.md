# Beverage Guide API

## Introduction
Beverage Guide Api is a resftful api built upon the flask micro framework, utilizing a postrges SQL database. It is the 
final project in the Udacity Full Stack Nanodegree and demonstrates effective data modeling and api developement. 
Authentication provided by Auth0 and hosted live via Heroku.

## Getting started 
Below is a set of instructions for running the api locally on your own machine.
- Python 3.7 or later is required, refer to [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) for installation and uppdating.
- Set up a virtual enviorment before installing dependencies (recomended).
### Dependencies
- Navigate to the root directory of your application.
- Install dependencies with `pip install -r requirements.txt` (use pip3 instead if needed).
### Run Server
- Set api.py as the flask app:
  `export FLASK_APP=api.py`
- Run Flask:
  `flask run --reload`

## Authentication
Beverage Guide Api is secured with role-based access controls through the Auth0 authentication system. Two roles 
have been defined and an example for each has been provided below for testing purposes.

1. Manager
    * Can access all endpoints and preform all CRUD functionallity.
    * Login
      * Email:
      * Password:
2. Team Member 
    * Can access limited GET requests and can prform no CRUD funtionality.
    * Login
      * Email:
      * Password:

To login or renew expired JWTs, boiler-plate authenication access is located at:

`https://beverage-guide-fsnd.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=MTUTENeOhGyl519OQIlyusbMNIRJ3nFm&redirect_uri=http://localhost:8100`

## Resource Endpoint Library
Below is a library of all expected endpoints and their behaviors.

### GET `/cocktails`
- Fetches list of all cocktails in a name and id format
- Expected return:
```js
{
    "cocktails": [
        {
            "id": 2,
            "name": "Cosmo"
        },
        {
            "id": 1,
            "name": ""
        },
        {
            "id": 3,
            "name": "cape cod"
        },
        {
            "id": 4,
            "name": "sangria"
        }
    ],
    "success": true
}
```

### GET `/cocktails/<int>`
- Fectches a specific coktail based on cocktail id.
- Returns a detailed response of id, name, directions, ingredients, glassware, and tags.
- Expected return:
```js
{
    "cocktail": {
        "directions": "Cosmo",
        "glasswear": "martini glass",
        "id": 2,
        "ingredients": [],
        "name": "Cosmo",
        "tags": [
            "cool"
        ]
    },
    "success": true
}
```

### GET `/beer`
- Fetches list of all beer in a name and id format
- Expected return
```js
{
    "beer": [
        {
            "id": 2,
            "name": "420"
        },
        {
            "id": 3,
            "name": "Bell's Two Hearted"
        },
        {
            "id": 4,
            "name": "Hey Man Ale"
        }
    ],
    "success": true
}
```

### GET `/beer/<int>`
- Fetches a specific beer based on beer id.
- Returns a detailed response id, name, style, tags, and draft or bottle
- Expected return:
```js
{
    "beer": {
        "draft_or_bottle": "bottle",
        "id": 2,
        "name": "420",
        "style": "IPA",
        "tags": []
    },
    "success": true
}
```

### GET `/wine`
- Fecthes a list of all wine in a name and id format
- expected return:
```js
{
    "success": true,
    "wine": [
        {
            "id": 1,
            "name": "Katherine Goldsmcidt"
        },
        {
            "id": 2,
            "name": "Portlandia"
        }
    ]
}
```

### GET `/wine/<int>`
- Fetches a specific wine based on wine id.
- Returns a detailed repsonse.
- Expected return:
```js
{
    "success": true,
    "wine": {
        "appellation": "Oregon",
        "classification": "red",
        "id": 2,
        "name": "Portlandia",
        "tags": [],
        "varietal": "Pinot Noir",
        "vintage": 2019
    }
}
```

