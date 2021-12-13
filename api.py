import os
from flask import Flask, request, abort, jsonify, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, BevTag, Cocktail, Beer, Wine, Ingredient, db
from auth import requires_auth
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv


app = Flask(__name__)
setup_db(app)
app.secret_key = 'dev'
CORS(app)


"""
Auth0 Config
"""


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='MTUTENeOhGyl519OQIlyusbMNIRJ3nFm',
    client_secret='h2TbYeWGoUGxruf4v9Lzoo5u_SMsDxcH_Sgtk-l6QQhtoUOt-_mBRTlxhc99MXFS',
    api_base_url='https://beverage-guide-fsnd.us.auth0.com',
    access_token_url='https://beverage-guide-fsnd.us.auth0.com/oauth/token',
    authorize_url='https://beverage-guide-fsnd.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                        'GET,PATCH,POST,DELETE,OPTIONS')
    session.pop('_flashes', None)
    return response


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://localhost:5000/callback, '
                                                 'https://localhost:8100/tabs/user-page')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'MTUTENeOhGyl519OQIlyusbMNIRJ3nFm'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


"""
Cocktails
"""
# all cocktails order alphbetically


@app.route('/cocktails')
@requires_auth()
def get_cockatils(jwt):
    cocktails = Cocktail.query.all()

    return jsonify({
        'success': True,
        'name': [cocktail.basic() for cocktail in cocktails]
    })


# specific cocktail info


@app.route('/cocktails/<int:cocktail_id>')
def get_cocktail_by_id(cocktail_id):
    cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()

    return jsonify({
        'success': True,
        'cocktail': cocktail.detailed()
    })

# create cocktail


@app.route('/cocktails', methods=['POST'])
def create_cocktail():
    body = request.get_json()

    name = body.get('name')
    ingredients = body.get('ingredients')
    directions = body.get('directions')
    glassware = body.get('glassware')
    tags = body.get('tags')

    new_cocktail = Cocktail(name=name,
                            ingredients=ingredients,
                            directions=directions,
                            glassware=glassware)

    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()
    new_cocktail.tags = bev_tags

    new_cocktail.create()

    return jsonify({
        'success': True,
        'created_cocktail': new_cocktail.detailed()
    })


# edit cocktail


@app.route('/cocktails/<int:cocktail_id>', methods=['PATCH'])
def update_cocktail(cocktail_id):
    body = request.get_json()

    cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()
    name = body.get('name', cocktail.name)
    ingredients = body.get('ingredients', cocktail.ingredients)
    directions = body.get('directions', cocktail.directions)
    glassware = body.get('glassware', cocktail.glassware)
    tags = body.get('tags', cocktail.tags)

    cocktail.name = name
    cocktail.ingredients = ingredients
    cocktail.directions = directions
    cocktail.glassware = glassware

    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()
    cocktail.tags = bev_tags

    cocktail.update()

    return jsonify({
        'success': True,
        'created_cocktail': cocktail.detailed()
    })

# delete cocktail


@app.route('/cocktails/<int:cocktail_id>', methods=['DELETE'])
def delete_cocktail(cocktail_id):
    cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()

    cocktail.delete()

    return jsonify({
        'success': True,
        'cocktail_name': cocktail.name,
        'cocktail_id': cocktail.id
    })

"""
Beer
"""
# all beer


@app.route('/beer')
def get_beer():
    all_beer = Beer.query.all()

    return jsonify({
        'success': True,
        'beer': [beer.basic() for beer in all_beer]
    })


# beer info


@app.route('/beer/<int:beer_id>')
def get_beer_by_id(beer_id):
    beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

    return jsonify({
        'success': True,
        'beer': beer.detailed()
    })

# create beer


@app.route('/beer', methods=['POST'])
def create_beer():
    body = request.get_json()

    name = body.get('name')
    style = body.get('style')
    draft_or_bottle = body.get('draft_or_bottle')
    tags = body.get('tags')

    new_beer = Beer(name=name,
                    style=style,
                    draft_or_bottle=draft_or_bottle)

    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()

    new_beer.tags = bev_tags

    new_beer.create()

    return jsonify({
        'success': True,
        'created_beer': new_beer.detailed()
    })

# edit beer


@app.route('/beer/<int:beer_id>', methods=['PATCH'])
def update_beer(beer_id):
    body = request.get_json()
    beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

    name = body.get('name', beer.name)
    style = body.get('style', beer.style)
    draft_or_bottle = body.get('draft_or_bottle', beer.draft_or_bottle)
    tags = body.get('tags', beer.tags)

    beer.name = name
    beer.style = style
    beer.draft_or_bottle = draft_or_bottle
    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()
    beer.tags = bev_tags

    beer.update()

    return jsonify({
        'success': True,
        'updated_beer': beer.detailed()
    })

# delete beer


@app.route('/beer/<int:beer_id>', methods=['DELETE'])
def delete_beer(beer_id):
    beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

    beer.delete()

    return jsonify({
        'success': True,
        'beer_name': beer.name,
        'beer_id': beer.id,
    })
"""
Wine
"""
# all wine


@app.route('/wine')
def get_wine():
    all_wine = Wine.query.all()

    return jsonify({
        'success': True,
        'wine': [wine.basic() for wine in all_wine]
    })


# create wine


@app.route('/wine', methods=['POST'])
def create_wine():
    body = request.get_json()

    name = body.get('name')
    classification = body.get('classification')
    varietal = body.get('varietal')
    vintage = body.get('vintage')
    appellation = body.get('appellation')
    tags = body.get('tags')

    new_wine = Wine(name=name, classification=classification,
                    varietal=varietal,
                    vintage=vintage,
                    appellation=appellation)

    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()
    new_wine.tags = bev_tags

    new_wine.create()

    return jsonify({
        'success': True,
        'created_wine': new_wine.detailed()
    })


# edit wine


@app.route('/wine/<int:wine_id>', methods=['PATCH'])
def update_wine(wine_id):
    body = request.get_json()
    wine = Wine.query.filter(Wine.id == wine_id).one_or_none()

    name = body.get('name', wine.name)
    classification = body.get('classification')
    varietal = body.get('varietal')
    vintage = body.get('vintage')
    appellation = body.get('appellation')
    tags = body.get('tags')

    wine = Wine.query.filter(Wine.id == wine_id).one_or_none()

    wine.name = name
    wine.classification = classification
    wine.varietal = varietal
    wine.vintage = vintage
    wine.appellation = appellation
    wine.tags = tags
    bev_tags = BevTag.query.filter(BevTag.id.in_(tags)).all()
    wine.tags = bev_tags

    wine.update()

    return jsonify({
        'success': True,
        'created_wine': wine.detailed()
    })

# delete wine


@app.route('/wine/<int:wine_id>', methods=['DELETE'])
def delete_wine(wine_id):
    wine = Wine.query.filter(Wine.id == wine_id).one_or_none()

    wine.delete()

    return jsonify({
        'success': True,
        'wine_name': wine.name,
        'wine_id': wine.id,
    }, 200)

"""
Tags
"""
# all tags


@app.route('/tags')
def get_tags():
    all_tags = BevTag.query.all()

    return jsonify({
        'success': True,
        'tags': [tag.detailed() for tag in all_tags]
    })


# tags filtered by cocktails


@app.route('/tags/<int:tag_id>/cocktails')
def get_cocktails_by_tag(tag_id):
    tag = BevTag.query.get(tag_id)
    cocktails_list = tag.cocktails

    return jsonify({
        'success': True,
        'tag_name': tag.name,
        'tag_id': tag.id,
        'cocktails': [cocktail.basic() for cocktail in cocktails_list]
    })

# tags filtered by wine


@app.route('/tags/<int:tag_id>/wine')
def get_wine_by_tag(tag_id):
    tag = BevTag.query.get(tag_id)
    wine_list = tag.wine

    return jsonify({
        'success': True,
        'tag_name': tag.name,
        'tag_id': tag.id,
        'cocktails': [wine.basic() for wine in wine_list]
    })

# tags filtered by beer


@app.route('/tags/<int:tag_id>/beer')
def get_beer_by_tag(tag_id):
    tag = BevTag.query.get(tag_id)
    beer_list = tag.beer

    return jsonify({
        'success': True,
        'tag_name': tag.name,
        'tag_id': tag.id,
        'cocktails': [beer.basic() for beer in beer_list]
    })

# create tag


@app.route('/tags', methods=['POST'])
def create_tag():
    body = request.get_json()

    name = body.get('name')

    new_tag = BevTag(name=name)

    new_tag.create()

    return jsonify({
        'success': True,
        'tag_name': new_tag.name,
        'tag_id': new_tag.id
    })


"""
ingredients
"""
# all ingredients


@app.route('/ingredients')
def get_ingredients():
    all_ingredients = Ingredient.query.all()

    return jsonify({
        'success': True,
        'ingredients': [ingredient.detailed() for ingredient in all_ingredients]
    })

# ingredients filter by cocktail


@app.route('/ingredients/<int:ingredient_id>/cocktails')
def get_cocktails_by_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    cocktail_list = ingredient.cocktails

    return jsonify({
        'success': True,
        'ingredient_name': ingredient.name,
        'ingredient_id': ingredient.id,
        'cocktails': [cocktail.basic() for cocktail in cocktail_list]
    })

# create ingredient


@app.route('/ingredients', methods=['POST'])
def create_ingredeint():
    body = request.get_json()

    name = body.get('name')

    new_ingredient = Ingredient(name=name)

    new_ingredient.create()

    return jsonify({
        'success': True,
        'ingredient_name': new_ingredient.name,
        'ingredient_id': new_ingredient.id,
    })


# edit ingredient


@app.route('/ingredients/<int:ingredient_id>', methods=['PATCH'])
def update_ingredeint(ingredient_id):
    body = request.get_json()

    name = body.get('name')

    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).one_or_none()

    ingredient.name = name

    ingredient.update()

    return jsonify({
        'success': True,
        'ingredient_name': ingredient.name,
        'ingredient_id': ingredient.id,
    })


# Error handlers


@app.errorhandler(400)
def invalid_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "invalid request"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    })