#!/usr/bin/env python

import re, json, os

from bottle import route, run, template
from bottle import request, response, hook
from bottle import post, get, put, delete


from modules.calc import Calc


_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers


@route('/', method=['GET'])
def home():
    return "PyCalc v1.0"

@get('/greeting/<name>')
def greeting(name):
    return "Hello %s!" % name

@route('/openapi.json', method=['GET'])
def openapi_spec():
    response.headers['Content-Type'] = 'application/json'
    spec_path = os.path.join(os.path.dirname(__file__), 'openapi.json')
    with open(spec_path) as f:
        return f.read()

@route('/docs', method=['GET'])
def swagger_ui():
    response.headers['Content-Type'] = 'text/html'
    return """
<!DOCTYPE html>
<html>
  <head>
    <title>PyCalc API - Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = function() {
        SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui'
        });
      };
    </script>
  </body>
</html>
"""


@route('/add', method=['POST', 'OPTIONS'])
def add_handler():
    response.headers['Content-Type'] = 'application/json'

    if request.method == "OPTIONS":
      return json.dumps({'status': True})

    status = False
    result = None
    data = request.json
    print("data:", data)
    if data is not None:
        if data['number1'] is not None and \
            data['number2'] is not None:
            calc = Calc()
            result = calc.add(data['number1'], data['number2'])
            #sql_insert_query = "insert into `personaje` values(NULL, '%s', '%s', '%s')" % (data['first_name'], data["last_name"], data["twitter"])
            #result  = cursor.execute(sql_insert_query)
            #cnx.commit()
            status = True

    return json.dumps({'status': status, 'result': result})

@route('/sub', method=['POST', 'OPTIONS'])
def sub_handler():
    response.headers['Content-Type'] = 'application/json'

    if request.method == "OPTIONS":
      return json.dumps({'status': True})

    status = False
    result = None
    data = request.json
    if data is not None:
        if data['number1'] is not None and \
            data['number2'] is not None:
            calc = Calc()
            result = calc.sub(data['number1'], data['number2'])
            status = True

    return json.dumps({'status': status, 'result': result})

@route('/mul', method=['POST', 'OPTIONS'])
def mul_handler():
    response.headers['Content-Type'] = 'application/json'

    if request.method == "OPTIONS":
      return json.dumps({'status': True})

    status = False
    result = None
    data = request.json
    if data is not None:
        if data['number1'] is not None and \
            data['number2'] is not None:
            calc = Calc()
            result = calc.mul(data['number1'], data['number2'])
            status = True

    return json.dumps({'status': status, 'result': result})

@route('/div', method=['POST', 'OPTIONS'])
def div_handler():
    response.headers['Content-Type'] = 'application/json'

    if request.method == "OPTIONS":
      return json.dumps({'status': True})

    status = False
    result = None
    data = request.json
    if data is not None:
        if data['number1'] is not None and \
            data['number2'] is not None:
            calc = Calc()
            result = calc.div(data['number1'], data['number2'])
            status = True

    return json.dumps({'status': status, 'result': result})


if __name__ == '__main__':
    run(host='0.0.0.0', reloader=True, port=8081)
