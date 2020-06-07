
# ./app.py

from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json
import os



# create flask app
app = Flask(__name__)



######configure pusher object#########
####### MODO NÃO SEGURO ##############

"""
from key import keys

pusher = Pusher(
  app_id = keys[0],
  key = keys[1],
  secret = keys[2],
  cluster = keys[3],
  ssl=True
)"""


#############configure pusher object####################
#################### MODO SEGURO #######################
########## NESTE MODO NÓS ADD VARS NO HEROKU#############
#### ENTÃO CHAMAMOS AS VARS DIRETO DO SERVIDOR HEROKU####
#OBS: Se tentar rodar aqui no LOCAL não irá funcionar...
#pois essas variáveis estão no SERVIDOR!!!!!

try:#RODAR NO SERVIDOR PRIMEIRO
  pusher = Pusher(
    app_id = str(os.environ['APP_ID']),
    key = str(os.environ['KEY']),
    secret = str(os.environ['SECRET']),
    cluster = str(os.environ['CLUSTER']),
    ssl=True
  )
except:# Não DEU CERTO? ENTÃO RODA LOCAL!!!!
  
  from key import keys
  pusher = Pusher(
    app_id = keys[0],
    key = keys[1],
    secret = keys[2],
    cluster = keys[3],
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
