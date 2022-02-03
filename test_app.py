import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from auth import AuthError

from api import create_app
from models import BevTag, Beer, Cocktail, Wine, Ingredient, setup_db, sample_data


class BeverageGuideTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = 'bg_test'
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)

        self.manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkQyU2dPWWZ0NTNyQ1B5Nk1jX3E0MyJ9.eyJpc3MiOiJodHRwczovL2JldmVyYWdlLWd1aWRlLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxYjdiNWFjMzZiZjY1MDA3MTViOTQ4MiIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImlhdCI6MTY0MzY4ODM5MywiZXhwIjoxNjQzNjk1NTkzLCJhenAiOiJNVFVURU5lT2hHeWw1MTlPUUlseXVzYk1OSVJKM25GbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJlZXIiLCJkZWxldGU6Y29ja3RhaWxzIiwiZGVsZXRlOndpbmUiLCJnZXQ6YmVlciIsImdldDpjb2NrdGFpbHMiLCJnZXQ6aW5ncmVkaWVudHMiLCJnZXQ6dGFncyIsImdldDp3aW5lIiwicGF0Y2g6YmVlciIsInBhdGNoOmNvY2t0YWlscyIsInBhdGNoOmluZ3JlZGllbnRzIiwicGF0Y2g6d2luZSIsInBvc3Q6YmVlciIsInBvc3Q6Y29ja3RhaWxzIiwicG9zdDppbmdyZWRpZW50cyIsInBvc3Q6dGFncyIsInBvc3Q6d2luZSJdfQ.WKrYfTXJFr-pW_sD4DGIMKXPVi1ruVUTyd8dYdXiq-5IcqZNhJWrmc5CcJh0cip9c-yStfUtZjktQCbkRbyn-PcFtQociLZYMmIxSqw17kFdcNA2hWLf2RREZ5DrQWFrSy2h0ZMyHMR1MQHnXoGsMwNcSbeNfIiiHnyAKVfUCM2sSCA9dS3SumK442VgzSzX3v7ybpUNitkwHdxjAiQDnZuxcjhXEhowqkKGTrPi4qMkF1sV4GDHM2V_ifm0FbUllI0XXgEKZ6m6IhwyRRyH7n6F-em5V--L04VnMft9EueYB_fgPpeWeQ2mGQiOkj0il_CxOyACiQbIEojnCLruUw'
        self.team_member = ''

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            # create all tables
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_cocktail = {
            'name': 'test cocktail',
            'ingredients': [],
            'directions': 'test directions',
            'glassware': 'test glassware',
            'tags': []
        }

        self.new_cocktail_fail = {
            'name': 'test cocktail',
            'ingredients': [],
            'directions': 5,
            'glassware': 'test glassware',
            'tags': []
        }

        self.new_beer = {
            'name': 'test beer',
            'style': 'test style',
            'draft_or_bottle': 'draft',
            'tags': []
        }

        self.new_beer_fail ={
            'name': 'test beer',
            'style': 'test style',
            'draft_or_bottle': True,
            'tags': []
        }

        self.new_wine = {
            'name': 'test name',
            'classifictation': 'test classification',
            'varietal': 'test varietal',
            'vintage': 'test vintage',
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
            'name': True
        }

        self.new_ingredient = {
            'name': 'test name'
        }

        self.new_ingredient_fail = {
            'name': 5
        }

    #sample_data()

    def tearDown(self):
        pass

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

    def test_patch_cocktail_success(self):
        res = self.client().patch('/cocktails/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'directions': 'new set of directions'})
        data = json.loads(res.data)
        #cocktail = Cocktail.query.filter(Cocktail.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['directions'], 'new set of directions')

    def test_patch_beer_success(self):
        res = self.client().patch('/beer/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'style': 'new style'})
        data = json.loads(res.data)
        #beer = Beer.query.filter(Beer.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['style'], 'new style')

    def test_patch_wine_success(self):
        res = self.client().patch('/wine/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'vintage': 2008})
        data = json.loads(res.data)
        #wine = Wine.query.filter(Wine.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['vintage'], 2008)

    def test_patch_ingredient_succes(self):
        res = self.client().patch('/ingredients/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'name': 'test'})
        data = json.loads(res.data)
        #ingredient = Ingredient.query.filter(Ingredient.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'], 'test')

    def test_patch_cocktail_failure(self):
        res = self.client().patch('/cocktails/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'directions': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_beer_failure(self):
        res = self.client().patch('/beer/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'style': True})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_wine_failure(self):
        res = self.client().patch('/beer/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'vintage': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_ingredient_failure(self):
        res = self.client().patch('/ingredients/2',
                                  headers={'Authorization': 'Bearer ' + self.manager},
                                  json={'name': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_cocktail_success(self):
        res = self.client().delete('/cocktails/3',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_beer_success(self):
        res = self.client().delete('/beer/3',
                                   headers={'Authorization': 'Bearer ' + self.manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_wine_success(self):
        res = self.client().delete('/wine/3',
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


if __name__ == "__main__":
    unittest.main()


