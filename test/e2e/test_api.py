import os
import unittest

import requests

BASE_URL = os.environ.get('API_URL', 'http://localhost:8081')


class TestApiE2E(unittest.TestCase):
    """
    Exercises the API over the real network against the actual built Docker
    image and its live process (as started by docker-e2e-test.sh). Anything
    that can be verified in-process belongs in test/integration instead;
    these tests only cover behavior that depends on the real deployed
    artifact: the wire protocol, process resilience, and multi-request
    workflows.
    """

    def test_readiness_probe_endpoint(self):
        # This is the same path k8s/deployment.yaml uses for its liveness
        # and readiness probes.
        response = requests.get(BASE_URL + '/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('PyCalc v1.0', response.text)

    def test_openapi_and_swagger_docs_are_served_over_http(self):
        spec_response = requests.get(BASE_URL + '/openapi.json')
        self.assertEqual(200, spec_response.status_code)
        self.assertEqual('application/json', spec_response.headers['Content-Type'])
        self.assertEqual('PyCalc API', spec_response.json()['info']['title'])

        docs_response = requests.get(BASE_URL + '/docs')
        self.assertEqual(200, docs_response.status_code)
        self.assertIn('swagger-ui', docs_response.text)

    def test_cors_preflight_over_the_network(self):
        response = requests.options(BASE_URL + '/add')
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual('*', response.headers['Access-Control-Allow-Origin'])
        self.assertIn('POST', response.headers['Access-Control-Allow-Methods'])

    def test_full_calculation_workflow(self):
        # Simulates a real client chaining several round trips through the
        # actual running server, each response feeding the next request.
        added = requests.post(BASE_URL + '/add', json={'number1': 12, 'number2': 5}).json()
        self.assertEqual(17.0, added['result'])

        subtracted = requests.post(BASE_URL + '/sub', json={'number1': added['result'], 'number2': 2}).json()
        self.assertEqual(15.0, subtracted['result'])

        multiplied = requests.post(BASE_URL + '/mul', json={'number1': subtracted['result'], 'number2': 2}).json()
        self.assertEqual(30.0, multiplied['result'])

        divided = requests.post(BASE_URL + '/div', json={'number1': multiplied['result'], 'number2': 5}).json()
        self.assertEqual(6.0, divided['result'])

    def test_unhandled_error_does_not_take_the_service_down(self):
        # calc.div raises ZeroDivisionError, uncaught by main.py, so the live
        # server returns a 500 for this request. What matters for an e2e
        # check is that the *process* survives it and keeps serving traffic
        # afterwards -- only observable against the real running server.
        crashing_response = requests.post(BASE_URL + '/div', json={'number1': 25, 'number2': 0})
        self.assertEqual(500, crashing_response.status_code)

        recovery_response = requests.get(BASE_URL + '/')
        self.assertEqual(200, recovery_response.status_code)


if __name__ == '__main__':
    unittest.main()
