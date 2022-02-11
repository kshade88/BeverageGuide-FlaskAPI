# Beverage Guide API

## Introduction
Beverage Guide Api is a resftful api built upon the flask micro framework, utilizing a postrges SQL database. It is the 
final project in the Udacity Full Stack Nanodegree and demonstrates effective data modeling and api developement. 
Authentication provided by Auth0 and hosted live via Heroku. https://beverage-guide-api-fsnd.herokuapp.com/


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
      * Email: manager@email.com
      * Password: FSNDtest1!
2. Team Member 
    * Can access limited GET requests and can prform no CRUD funtionality.
    * Login
      * Email: teammember@gmail.com
      * Password: FSNDtest1!

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
        "directions": "Shake and pour",
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

### GET `/tags`
- Fetches a list of all tags.
- Expected return
```js
{
    "success": true,
    "tags": [
        {
            "id": 1,
            "name": "cool"
        },
        {
            "id": 2,
            "name": "refreshing"
        },
        {
            "id": 3,
            "name": "test tag"
        },
        {
            "id": 4,
            "name": "Boozy"
        }
    ]
}
```

### GET `tags/<int>/cocktails`
- Fetches a list of cocktails with a specific tag based on tag id.
- Expected return:
```js
{
    "cocktails": [
        {
            "id": 2,
            "name": "Screw Driver"
        },
        {
            "id": 1,
            "name": "Bloody Mary"
        },
        {
            "id": 3,
            "name": "cape cod"
        },
        {
            "id": 17,
            "name": "Cosmopolitan"
        }
    ],
    "success": true,
    "tag_id": 1,
    "tag_name": "cool"
}
```

### GET `tags/<int>/beer`
- Fetches a list of beer with a specific tag based on tag id.
- Expected return:
```js
{
    "beer": [
        {
            "id": 4,
            "name": "Creature Comfort Classic City Lager"
        },
        {
            "id": 6,
            "name": "Hey Man Ale"
        }
    ],
    "success": true,
    "tag_id": 1,
    "tag_name": "cool"
}
```

### GET `tags/<int>/wine`
- Fetches a list of wine with a specific tag based on tag id.
- Expected return:
```js
{
    "success": true,
    "tag_id": 1,
    "tag_name": "cool",
    "wine": [
        {
            "id": 3,
            "name": "Barone Motalto"
        }
    ]
}
```

### GET `/ingredients`
- Fetches a list of all possible cocktail ingredients.
- Expected return:
```js
{
    "ingredients": [
        {
            "id": 1,
            "name": "Tito's Vodka"
        },
        {
            "id": 2,
            "name": "Four Roses Bourbon"
        },
        {
            "id": 3,
            "name": "Cranberry Juice"
        },
        {
            "id": 4,
            "name": "Tripel Sec"
        },
        {
            "id": 5,
            "name": "Bitters"
        },
        {
            "id": 6,
            "name": "Simple Syrup"
        }
    ],
    "success": true
}
```

### GET `/ingredients/<int>/cocktails`
- Fetches a list of cocktails filtered by a specific ingredient id.
- Expected return:
```js
{
    "cocktails": [
        {
            "id": 17,
            "name": "Cosmopolitan"
        },
        {
            "id": 14,
            "name": "Dirty Martini"
        }
    ],
    "ingredient_id": 1,
    "ingredient_name": "Tito's Vodka",
    "success": true
}
```

### POST `/cocktails`
- Creates a new cocktail
- Sample body:
```js
{
    "name": "Old Fashioned",
    "ingredients": [2,5,6],
    "directions": "Stir ingredients together in ice, pour over fresh ice.",
    "glassware": "Rocks glass",
    "tags": [4]
}
```
- Expected return:
```js
{
    "created_cocktail": {
        "directions": "Old Fashioned",
        "glasswear": "Rocks glass",
        "id": 16,
        "ingredients": [
            "Four Roses Bourbon",
            "Bitters",
            "Simple Syrup"
        ],
        "name": "Old Fashioned 7",
        "tags": [
            "Boozy"
        ]
    },
    "success": true
}
```

### POST `/wine`
- Creates a new wine
- Sample body:
```js
{
    "name": "Barone Motalto",
    "classification": "white",
    "varietal": "Pinot Grigio",
    "vintage": "2019",
    "appellation": "Italy",
    "tags": [4]
}
```
- Expected return:
```js
{
    "created_wine": {
        "appellation": "Italy",
        "classification": "white",
        "id": 3,
        "name": "Barone Motalto",
        "tags": [
            "Light"
        ],
        "varietal": null,
        "vintage": 2019
    },
    "success": true
}
```
### POST `/beer`
- Creates a new beer in the database
- Sample body:
```js
{
    "name": "Wild Leap Chance",
    "style": "IPA",
    "tags": [4,2],
    "draft_or_bottle": "draft"
}
```
- Expected return:
```js
{
    "created_beer": {
        "draft_or_bottle": "draft",
        "id": 7,
        "name": "Wild Leap Chance",
        "style": "IPA",
        "tags": [
            "refreshing",
            "Boozy"
        ]
    },
    "success": true
}
```

### POST `/tags`
- Creates a new tag in the database.
- Sample body:
```js
{
    "name": "Boozy"
}
```
- Expected return:
```js
{
    "success": true,
    "tag_id": 4,
    "tag_name": "Boozy"
}
```

### POST `/ingredients`
- Creates a new tag in the database.
- Sample body:
```js
{
    "name": "Ketel One Vodka"
}
```
- Expected return:
```js
{
    "ingredient_id": 6,
    "ingredient_name": "Simple Syrup",
    "success": true
}
```

### PATCH `/cocktails/<int>`
- Edits an existing cocktail based on id.
- Will accept any number of attributes to edit, if none will keep old value.
- Expected body:
```js
{
    "name": "Classic Old Fashioned",
    "ingredients": [2,5,6],
    "directions": "Stir ingredients together in ice, pour over fresh ice. Garnish with cherry and orange",
    "glassware": "Rocks glass",
    "tags": [4]
}
```
- Expected return:
```js
{
    "created_cocktail": {
        "directions": "Classic Old Fashioned",
        "glasswear": "Rocks glass",
        "id": 16,
        "ingredients": [
            "Four Roses Bourbon",
            "Bitters",
            "Simple Syrup"
        ],
        "name": "Classic Old Fashioned",
        "tags": [
            "Boozy"
        ]
    },
    "success": true
}
```

### PATCH `/wine/<int>`
- Edits an existing wine based on id.
- Will accept any number of attributes to edit, if none will keep old value.
- Sample body:
```js
{
    "name": "Barone Motalto",
    "classification": "white",
    "varietal": "Pinot Grigio",
    "appellation": "Italy",
    "tags": [1,2]
}
```
- Expected return:
```js
{
    "created_wine": {
        "appellation": "Italy",
        "classification": "white",
        "id": 3,
        "name": "Barone Motalto",
        "tags": [
            "cool",
            "refreshing"
        ],
        "varietal": "Pinot Grigio",
        "vintage": 2019
    },
    "success": true
}
```

### PATCH `/beer/<int>`
- Edits an existing beer based on id.
- Sample body:
```js
{
    "tags": [2],
    "draft_or_bottle": "draft"
}
```
- Expected return:
```js
{
    "success": true,
    "updated_beer": {
        "draft_or_bottle": "draft",
        "id": 2,
        "name": "420",
        "style": "IPA",
        "tags": [
            "refreshing"
        ]
    }
}
```

### PATCH `/ingredients/<id>`
- Edits an existing ingredient based on id.
- Sample body:
```js
{
    "name": "Simple Syrup test"
}
```
- Expected return:
```js
{
    "ingredient_id": 6,
    "ingredient_name": "Simple Syrup",
    "success": true
}
```

### DELETE `/cocktails/<int>`
- Deletes an existing cocktail based on id.
- Expected return:
```js
{
    "cocktail_id": 15,
    "cocktail_name": "Old Fashioned",
    "success": true
}
```

### DELETE `/wine/<int>`
- Deletes an existing wine based on id.
- Expected return:
```js
{
    "success": true,
    "wine_id": 4,
    "wine_name": "Tribute"
}
```

### DELETE `/beer/<int>`
- Deletes an existing beer based on id.
- Expected return:
```js
{
    "beer_id": 5,
    "beer_name": "Hey Man Ale",
    "success": true
}
```

## Testing
### Locally with unit tests
- Set up a test database named `bg_test`.
- Using psql terminal commands run: `CREATE DATABSE bg_test`
- Under root directiory run: ```python3 test_app.py```
- If tests fail due to expired jwt, reference "Authentication" above and replace jwts in .env file.

### Live with Postman Collections
- Using the postman app, upload included postman collections
- All collections should run successfully on first run through with exit code 200.
- If collection is run more than once duplicate posts or deletes may cause conflict.
- Feel free to play with endpoints and add and delete data as wanted.
- Current JWTS are set for roughly 24 hours, if expired follow the steps above in order to generate new ones.

## To Do's
- Set up an usuable front end using html templates or node.js
- Create app in django and relaunch to heroku