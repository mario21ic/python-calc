import json
import os
import sys
import unittest

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, SRC_DIR)

import bottle
from webtest import TestApp

import main  # noqa: E402  (importing registers the routes on bottle's default app)


class TestAppIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(bottle.default_app())

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('PyCalc v1.0', response.text)

    def test_greeting(self):
        response = self.app.get('/greeting/world')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello world!', response.text)

    def test_cors_headers_present(self):
        response = self.app.get('/')
        self.assertEqual('*', response.headers['Access-Control-Allow-Origin'])

    def test_openapi_spec_is_served_and_valid(self):
        response = self.app.get('/openapi.json')
        self.assertEqual(200, response.status_code)
        spec = json.loads(response.text)
        self.assertEqual('PyCalc API', spec['info']['title'])
        self.assertIn('/add', spec['paths'])

    def test_docs_serves_swagger_ui(self):
        response = self.app.get('/docs')
        self.assertEqual(200, response.status_code)
        self.assertIn('swagger-ui', response.text)

    def test_add(self):
        response = self.app.post_json('/add', {'number1': 12, 'number2': 5})
        body = response.json
        self.assertTrue(body['status'])
        self.assertEqual(17.0, body['result'])

    def test_sub(self):
        response = self.app.post_json('/sub', {'number1': 12, 'number2': 5})
        body = response.json
        self.assertTrue(body['status'])
        self.assertEqual(7.0, body['result'])

    def test_mul(self):
        response = self.app.post_json('/mul', {'number1': 10, 'number2': 5})
        body = response.json
        self.assertTrue(body['status'])
        self.assertEqual(50.0, body['result'])

    def test_div(self):
        response = self.app.post_json('/div', {'number1': 25, 'number2': 5})
        body = response.json
        self.assertTrue(body['status'])
        self.assertEqual(5.0, body['result'])

    def test_add_options_preflight(self):
        response = self.app.options('/add')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['status'])

    def test_add_without_json_body_returns_status_false(self):
        response = self.app.post('/add', 'not-json', content_type='text/plain')
        body = response.json
        self.assertFalse(body['status'])
        self.assertIsNone(body['result'])


if __name__ == '__main__':
    unittest.main()
