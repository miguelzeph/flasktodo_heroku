
# ./app.py

from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json
import os
#from k import kx



from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['KEY'],os.environ['CLUSTER'],os.environ['APP_ID'],os.environ['SECRET'])


# create flask app
app = Flask(__name__)

# configure pusher object
"""pusher = Pusher(
  app_id = kx[0],
  key = kx[1],
  secret = kx[2],
  cluster = kx[3],
  ssl=True
)"""

pusher = Pusher(
  app_id = APP_id,
  key = KEY,
  secret = SECRET,
  cluster = CLUSTER,
  ssl=True
)


# index route, shows index.html view
@app.route('/')
def index():
  return render_template('index.html')

# endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addTodo():
  data = json.loads(request.data) # load JSON data from request
  pusher.trigger('todo', 'item-added', data) # trigger `item-added` event on `todo` channel
  return jsonify(data)

# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
  data = {'id': item_id }
  pusher.trigger('todo', 'item-removed', data)
  return jsonify(data)

# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
  data = {
    'id': item_id,
    'completed': json.loads(request.data).get('completed', 0)
  }
  pusher.trigger('todo', 'item-updated', data)
  return jsonify(data)

# run Flask app in debug mode
#app.run(debug=True)


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
