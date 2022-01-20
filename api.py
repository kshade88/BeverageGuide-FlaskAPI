import os
from flask import Flask, request, abort, jsonify, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, BevTag, Cocktail, Beer, Wine, Ingredient, db
from auth import requires_auth, AuthError
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')

        return response

    """
    Cocktails
    """
    # all cocktails order alphbetically

    @app.route('/cocktails')
    @requires_auth('get:cocktails')
    def get_cockatils(payload):
        try:
            cocktails = Cocktail.query.all()

            return jsonify({
                'success': True,
                'cocktails': [cocktail.basic() for cocktail in cocktails]
            })
        except Exception as e:
            print(e)
            abort(422)

    # specific cocktail info

    @app.route('/cocktails/<int:cocktail_id>')
    @requires_auth('get:cocktails')
    def get_cocktail_by_id(payload, cocktail_id):
        try:
            cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()

            return jsonify({
                'success': True,
                'cocktail': cocktail.detailed()
            })
        except:
            abort(422)

    # create cocktail

    @app.route('/cocktails', methods=['POST'])
    @requires_auth('post:cocktails')
    def create_cocktail(payload):
        body = request.get_json()

        name = body.get('name')
        ingredients = body.get('ingredients')
        directions = body.get('directions')
        glassware = body.get('glassware')
        tags = body.get('tags')

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # edit cocktail

    @app.route('/cocktails/<int:cocktail_id>', methods=['PATCH'])
    @requires_auth('patch:cocktails')
    def update_cocktail(cocktail_id, payload):
        body = request.get_json()

        cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()
        name = body.get('name', cocktail.name)
        ingredients = body.get('ingredients', cocktail.ingredients)
        directions = body.get('directions', cocktail.directions)
        glassware = body.get('glassware', cocktail.glassware)
        tags = body.get('tags', cocktail.tags)

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # delete cocktail

    @app.route('/cocktails/<int:cocktail_id>', methods=['DELETE'])
    @requires_auth('delete:cocktails')
    def delete_cocktail(cocktail_id, payload):
        try:
            cocktail = Cocktail.query.filter(Cocktail.id == cocktail_id).one_or_none()

            if len(cocktail) == 0:
                abort(404)

            cocktail.delete()

            return jsonify({
                'success': True,
                'cocktail_name': cocktail.name,
                'cocktail_id': cocktail.id
            })
        except Exception as e:
            print(e)
            abort(422)

    """
    Beer
    """
    # all beer

    @app.route('/beer')
    @requires_auth('get:beer')
    def get_beer(payload):
        try:
            all_beer = Beer.query.all()

            return jsonify({
                'success': True,
                'beer': [beer.basic() for beer in all_beer]
            })
        except Exception as e:
            print(e)
            abort(422)

    # beer info

    @app.route('/beer/<int:beer_id>')
    @requires_auth('get:beer')
    def get_beer_by_id(payload, beer_id):
        try:
            beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

            return jsonify({
                'success': True,
                'beer': beer.detailed()
            })
        except Exception as e:
            print(e)
            abort(422)

    # create beer

    @app.route('/beer', methods=['POST'])
    @requires_auth('post:beer')
    def create_beer(payload):
        body = request.get_json()

        name = body.get('name')
        style = body.get('style')
        draft_or_bottle = body.get('draft_or_bottle')
        tags = body.get('tags')

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # edit beer

    @app.route('/beer/<int:beer_id>', methods=['PATCH'])
    @requires_auth('patch:beer')
    def update_beer(beer_id, payload):
        body = request.get_json()
        beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

        if len(beer) == 0:
            abort(404)

        name = body.get('name', beer.name)
        style = body.get('style', beer.style)
        draft_or_bottle = body.get('draft_or_bottle', beer.draft_or_bottle)
        tags = body.get('tags', beer.tags)

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # delete beer

    @app.route('/beer/<int:beer_id>', methods=['DELETE'])
    @requires_auth('delete:beer')
    def delete_beer(beer_id, payload):
        try:
            beer = Beer.query.filter(Beer.id == beer_id).one_or_none()

            if len(beer) == 0:
                abort(404)

            beer.delete()

            return jsonify({
                'success': True,
                'beer_name': beer.name,
                'beer_id': beer.id,
            })
        except Exception as e:
            print(e)
            abort(422)
    """
    Wine
    """
    # all wine

    @app.route('/wine')
    @requires_auth('get:wine')
    def get_wine(payload):
        try:
            all_wine = Wine.query.all()

            return jsonify({
                'success': True,
                'wine': [wine.basic() for wine in all_wine]
            })
        except Exception as e:
            print(e)
            abort(422)

    # create wine

    @app.route('/wine', methods=['POST'])
    @requires_auth('post:wine')
    def create_wine(payload):
        body = request.get_json()

        name = body.get('name')
        classification = body.get('classification')
        varietal = body.get('varietal')
        vintage = body.get('vintage')
        appellation = body.get('appellation')
        tags = body.get('tags')

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # edit wine

    @app.route('/wine/<int:wine_id>', methods=['PATCH'])
    @requires_auth('patch:wine')
    def update_wine(payload, wine_id):
        body = request.get_json()
        wine = Wine.query.filter(Wine.id == wine_id).one_or_none()

        name = body.get('name', wine.name)
        classification = body.get('classification', wine.classification)
        varietal = body.get('varietal', wine.varietal)
        vintage = body.get('vintage', wine.vintage)
        appellation = body.get('appellation', wine.appellation)
        tags = body.get('tags', wine.tags)

        try:
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
        except Exception as e:
            print(e)
            abort(422)

    # delete wine

    @app.route('/wine/<int:wine_id>', methods=['DELETE'])
    @requires_auth('delete:wine')
    def delete_wine(wine_id, payload):
        try:
            wine = Wine.query.filter(Wine.id == wine_id).one_or_none()

            if len(wine) == 0:
                abort(404)

            wine.delete()

            return jsonify({
                'success': True,
                'wine_name': wine.name,
                'wine_id': wine.id,
            })
        except Exception as e:
            print(e)
            abort(422)


    """
    Tags
    """
    # all tags

    @app.route('/tags')
    @requires_auth('get:tags')
    def get_tags(payload):
        try:
            all_tags = BevTag.query.all()

            return jsonify({
                'success': True,
                'tags': [tag.detailed() for tag in all_tags]
            })
        except Exception as e:
            print(e)
            abort(422)

    # tags filtered by cocktails

    @app.route('/tags/<int:tag_id>/cocktails')
    @requires_auth('get:tags')
    def get_cocktails_by_tag(tag_id, payload):
        try:
            tag = BevTag.query.get(tag_id)

            if len(tag) == 0:
                abort(404)

            cocktails_list = tag.cocktails

            return jsonify({
                'success': True,
                'tag_name': tag.name,
                'tag_id': tag.id,
                'cocktails': [cocktail.basic() for cocktail in cocktails_list]
            })
        except Exception as e:
            print(e)
            abort(422)

    # tags filtered by wine

    @app.route('/tags/<int:tag_id>/wine')
    @requires_auth('get:tags')
    def get_wine_by_tag(tag_id, payload):
        try:
            tag = BevTag.query.get(tag_id)

            if len(tag) == 0:
                abort(404)

            wine_list = tag.wine

            return jsonify({
                'success': True,
                'tag_name': tag.name,
                'tag_id': tag.id,
                'cocktails': [wine.basic() for wine in wine_list]
            })
        except:
            abort(422)

    # tags filtered by beer

    @app.route('/tags/<int:tag_id>/beer')
    @requires_auth('get:tags')
    def get_beer_by_tag(tag_id, payload):
        try:
            tag = BevTag.query.get(tag_id)

            if len(tag) == 0:
                abort(404)

            beer_list = tag.beer

            return jsonify({
                'success': True,
                'tag_name': tag.name,
                'tag_id': tag.id,
                'cocktails': [beer.basic() for beer in beer_list]
            })
        except Exception as e:
            print(e)
            abort(422)

    # create tag

    @app.route('/tags', methods=['POST'])
    @requires_auth('post:tags')
    def create_tag(payload):
        body = request.get_json()

        name = body.get('name')

        try:
            new_tag = BevTag(name=name)

            new_tag.create()

            return jsonify({
                'success': True,
                'tag_name': new_tag.name,
                'tag_id': new_tag.id
            })
        except Exception as e:
            print(e)
            abort(422)

    """
    ingredients
    """
    # all ingredients

    @app.route('/ingredients')
    @requires_auth('get:ingredients')
    def get_ingredients(payload):
        try:
            all_ingredients = Ingredient.query.all()

            return jsonify({
                'success': True,
                'ingredients': [ingredient.detailed() for ingredient in all_ingredients]
            })
        except Exception as e:
            print(e)
            abort(422)

    # cocktails filtered by ingredient

    @app.route('/ingredients/<int:ingredient_id>/cocktails')
    @requires_auth('get:ingredients')
    def get_cocktails_by_ingredient(ingredient_id, payload):
        try:
            ingredient = Ingredient.query.get(ingredient_id)

            if len(ingredient) == 0:
                abort(404)

            cocktail_list = ingredient.cocktails

            return jsonify({
                'success': True,
                'ingredient_name': ingredient.name,
                'ingredient_id': ingredient.id,
                'cocktails': [cocktail.basic() for cocktail in cocktail_list]
            })
        except Exception as e:
            print(e)
            abort(422)

    # create ingredient

    @app.route('/ingredients', methods=['POST'])
    @requires_auth('post:ingredients')
    def create_ingredeint(payload):
        try:
            body = request.get_json()

            name = body.get('name')

            new_ingredient = Ingredient(name=name)

            new_ingredient.create()

            return jsonify({
                'success': True,
                'ingredient_name': new_ingredient.name,
                'ingredient_id': new_ingredient.id,
            })
        except Exception as e:
            print(e)
            abort(422)

    # edit ingredient

    @app.route('/ingredients/<int:ingredient_id>', methods=['PATCH'])
    @requires_auth('patch:ingredients')
    def update_ingredeint(ingredient_id, payload):
        try:
            body = request.get_json()

            name = body.get('name')

            ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).one_or_none()

            if len(ingredient) == 0:
                abort(404)

            ingredient.name = name

            ingredient.update()

            return jsonify({
                'success': True,
                'ingredient_name': ingredient.name,
                'ingredient_id': ingredient.id,
            })
        except Exception as e:
            print(e)
            abort(422)

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

    @app.errorhandler(AuthError)
    def auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
