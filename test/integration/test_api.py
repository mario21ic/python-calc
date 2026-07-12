import os
import unittest

import requests

BASE_URL = os.environ.get('API_URL', 'http://localhost:8081')


class TestApiIntegration(unittest.TestCase):

    def test_home(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('PyCalc v1.0', response.text)

    def test_greeting(self):
        response = requests.get(BASE_URL + '/greeting/world')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello world!', response.text)

    def test_add(self):
        response = requests.post(BASE_URL + '/add', json={'number1': 12, 'number2': 5})
        body = response.json()
        self.assertTrue(body['status'])
        self.assertEqual(17.0, body['result'])

    def test_sub(self):
        response = requests.post(BASE_URL + '/sub', json={'number1': 12, 'number2': 5})
        body = response.json()
        self.assertTrue(body['status'])
        self.assertEqual(7.0, body['result'])

    def test_mul(self):
        response = requests.post(BASE_URL + '/mul', json={'number1': 10, 'number2': 5})
        body = response.json()
        self.assertTrue(body['status'])
        self.assertEqual(50.0, body['result'])

    def test_div(self):
        response = requests.post(BASE_URL + '/div', json={'number1': 25, 'number2': 5})
        body = response.json()
        self.assertTrue(body['status'])
        self.assertEqual(5.0, body['result'])


if __name__ == '__main__':
    unittest.main()
