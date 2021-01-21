from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
# jsonify is a function in Flask's flask.json module. jsonify serializes data to JavaScript Object Notation (JSON)
# format, wraps it in a Response object with the application/json mimetype


# jsonify is sometimes imported directly from the flask module instead of from flask.json. It is the same function
# that is imported, but there are less characters to type when you leave off the .json part.


app = Flask(__name__)

# API Application Programming Interface


# Basically In this Project i m creating an web api using flask (Flask is a backend web framework)
# it means that it provides the functionality for building web applications, including HTTP requests
# and rendering templates

# HTTP (Hypertext Transfer Protocol ) is designed to enable communication between clients and servers
# HTTP works as a requres response protocol between a client and server

# A client(browser) sends an HTTP request to the server; then server returns a response to the client
# The response contains information about the request and may also contain the requested content

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/printName/<string:name>')
def printName(name):
    result = {
        "Name" : name
    }
    return jsonify(result)

# It is the easiest way ti secure our web api is to require clients to provide username and password
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'sardanaboykanu':
        return 'iphone'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# Here I m handling exception
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Syntax'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
# for learning i m using a list object as database
# while developing working we have to use database here
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# Get request never be used when dealing with sensitive data, have length restrictions and are only used to request data
# curl -i http://localhost:5000/tasks
# curl -u sardanaboykanu:iphone -i http://localhost:5000/tasks
@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# POST method is used to send data to server to create/update a resource
# POST requests are never cached, do not remains in the browser history, can not be bookmarked  and have no restriction
# on data length
# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"MacBook", "description":"Good Product"}'
# http://localhost:5000/createTasks
@app.route('/createTasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/updateTasks/2
@app.route('/updateTasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/deleteTasks/1
@app.route('/deleteTasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)


# REST (REpresentational State Transfer) has emerged as the standard architectural design for web services and web APIs
