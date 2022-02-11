import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from auth import AuthError
from dotenv import load_dotenv

from api import create_app
from models import BevTag, Beer, Cocktail, Wine, Ingredient, setup_db, sample_data

load_dotenv()


class BeverageGuideTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = 'bg_test'
        self.database_path = os.environ['TEST_DATABASE_URL']

        self.team_member = os.environ['TEAM_MEMBER_JWT']
        self.manager = os.environ['MANAGER_JWT']
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            # create all tables
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            sample_data()

        self.new_cocktail = {
            'name': 'test cocktail pass',
            'ingredients': [],
            'directions': 'test directions',
            'glassware': 'test glassware',
            'tags': []
        }

        self.new_cocktail_fail = {
            'name': 'test cocktail fail',
            'ingredients': 5,
            'directions': 'test directions',
            'glassware': 'test glassware',
            'tags': []
        }

        self.new_beer = {
            'name': 'test beer pass',
            'style': 'test style',
            'draft_or_bottle': 'draft',
            'tags': []
        }

        self.new_beer_fail ={
            'name': 'test beer fail',
            'style': 'test style',
            'draft_or_bottle': 'draft',
            'tags': "blue"
        }

        self.new_wine = {
            'name': 'test name',
            'classifictation': 'test classification',
            'varietal': 'test varietal',
            'vintage': 2000,
            'appelation': 'test appellation',
            'tags': []
        }

        self.new_wine_fail = {
            'name': 'test name',
            'classifictation': 'test classification',
            'varietal': 'test varietal',
            'vintage': 'test vintage',
            'appelation': 'test appellation',
            'tags': 'tags!'
        }

        self.new_tag = {
            'name': 'test name',
        }

        self.new_tag_fail = {
            'name': 'Test tag1'
        }

        self.new_ingredient = {
            'name': 'new ingredient'
        }

        self.new_ingredient_fail = {
            'name': 'test ingredient1'
        }

    def tearDown(self):
        pass

    # GET Tests
    def test_get_cocktails_success(self):
        res = self.client().get('/cocktails', headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cocktails'])

    def test_get_beer_success(self):
        res = self.client().get('/beer', headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['beer'])

    def test_get_wine_success(self):
        res = self.client().get('/wine', headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['wine'])

    def test_get_bevtags_success(self):
        res = self.client().get('/tags', headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tags'])

    def test_get_ingredients_success(self):
        res = self.client().get('/ingredients', headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['ingredients'])

    # POST Tests
    def test_add_cocktail_success(self):
        res = self.client().post('/cocktails',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_cocktail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['created_cocktail']))

    def test_add_beer_success(self):
        res = self.client().post('/beer',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_beer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['created_beer']))

    def test_add_wine_success(self):
        res = self.client().post('/wine',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_wine)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['created_wine']))

    def test_add_tag_success(self):
        res = self.client().post('/tags',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_tag)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['tag_name']))

    def test_add_ingredient_success(self):
        res = self.client().post('/ingredients',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_ingredient)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['ingredient_name']))

    def test_add_cocktail_failure(self):
        res = self.client().post('/cocktails',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_cocktail_fail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_beer_failure(self):
        res = self.client().post('/beer',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_beer_fail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_wine_failure(self):
        res = self.client().post('/wine',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_wine_fail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_tag_failure(self):
        res = self.client().post('/tags',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_tag_fail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_ingredient_failure(self):
        res = self.client().post('/ingredients',
                                 headers={'Authorization': 'Bearer ' + self.manager},
                                 json=self.new_ingredient_fail)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # PATCH Tests
    def test_patch_cocktail_success(self):
        res = self.client().patch('/cocktails/1',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'directions': 'new set of directions'})
        data = json.loads(res.data)
        #cocktail = Cocktail.query.filter(Cocktail.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_cocktail'])

    def test_patch_beer_success(self):
        res = self.client().patch('/beer/1',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'style': 'new style'})
        data = json.loads(res.data)
        #beer = Beer.query.filter(Beer.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_beer'])

    def test_patch_wine_success(self):
        res = self.client().patch('/wine/1',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'vintage': 2008})
        data = json.loads(res.data)
        #wine = Wine.query.filter(Wine.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_wine'])

    def test_patch_ingredient_succes(self):
        res = self.client().patch('/ingredients/1',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'name': 'test'})
        data = json.loads(res.data)
        #ingredient = Ingredient.query.filter(Ingredient.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['ingredient_name'])

    def test_patch_cocktail_failure(self):
        res = self.client().patch('/cocktails/5',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'directions': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_beer_failure(self):
        res = self.client().patch('/beer/5',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'style': True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_wine_failure(self):
        res = self.client().patch('/wine/5',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'vintage': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_ingredient_failure(self):
        res = self.client().patch('/ingredients/5',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'name': "new"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # DELETE Tests
    def test_delete_cocktail_success(self):
        res = self.client().delete('/cocktails/1',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_beer_success(self):
        res = self.client().delete('/beer/1',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_wine_success(self):
        res = self.client().delete('/wine/1',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_cocktail_failure(self):
        res = self.client().delete('/cocktails/100000',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_beer_failure(self):
        res = self.client().delete('/beer/100000',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_wine_failure(self):
        res = self.client().delete('/wine/100000',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Auth Fail Tests
    def test_no_header_failuer(self):
        res = self.client().get('/cocktails')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_role_unauthorized_failure(self):
        res = self.client().post('/tags',
                                 headers={'Auhorization': 'Bearer ' + self.team_member},
                                 json={'name': 'test tag fail'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)




if __name__ == "__main__":
    unittest.main()


