import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src import api
from src.database.models import setup_db, Drink

class CoffeeTestCas(unittest.TestCase):
    
    def setUp(self):
        self.app = api.app
        setup_db(self.app)

        self.client = self.app.test_client


    def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()