#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from .connect import get_db, make_dicts
from .sql_script import create_table
import socketio
import json
import requests, threading
import time
from flask import Flask
from flask_cors import CORS, cross_origin
import serial


#SOCKET

#Initialisation
sio = socketio.Client()

#Get IP
f = open("/home/telo/Documents/ipVenv","r")
ip = f.read().split("\n")[0]
print("http://" + ip + ":9400")

#Serial Port communication
try:
	serialcomm = serial.Serial('/dev/ttyUSB0', 9600)
	serialcomm.timeout = 1
except ExplicitException:
    print("ttyUSB0 indisponible")
try:
    serialcomm = serial.Serial('/dev/ttyUSB1', 9600)
    serialcomm.timeout = 1
except ExplicitException:
    print("ttyUSB1 indisponible")
try:
    serialcomm = serial.Serial('/dev/ttyUSB2', 9600)
    serialcomm.timeout = 1
except:

	print("ttyUSB2 indisponible")


#Connexion au serveur
sio.connect("http://"+ ip +":9400", namespaces=['/api'])
print('my sid is', sio.sid)



app = Flask(__name__)
CORS(app)

def sendToArduino(direction):
    #serialcomm.write(direction.encode())
    time.sleep(0.5)
    #print(serialcomm.readline().decode('ascii'))
    

@app.route('/api/create_table', methods=['GET'])
def create_table_():
    create_table()
    return "OK"


@app.route('/api/start', methods=['GET'])
def start():
   
    # query = "A:5:S:D:1"
    # requests.get('http://192.168.252.119/'+query)
    # time.sleep(7)
    data = "Akwaaba.     Je suis Telo!"
    #Connexion au serveur
    sio.emit('start-speak', data, namespace='/api')
    return "OK"


@app.route('/api/personnel', methods=['GET'])
def get_tasks():
    cur = get_db().execute("select * from personnel")
    rv = cur.fetchall()
    
    data = list()
    for row in rv:
        data.append(make_dicts(cur, row))
        
    #res = json.decoder( data )
    #for row in rv:
        #print(row)
    print(data)
    #Connexion au serveur
    sio.emit('info-personal', data, namespace='/api')
    return "OK"


# @app.route('/api/guide', methods=['GET'])
# def get_tasks():
#     cur = get_db().execute("select * from personnel")
#     rv = cur.fetchall()
#     data = list()
#     for row in rv:
#         data.append(make_dicts(cur, row))
        
#     #res = json.decoder( data )
#     #for row in rv:
#         #print(row)
#     print(data)
#     #Connexion au serveur
#     sio.emit('info-personal', data, namespace='/api')
#     return "OK"


@app.route('/api/guide/run/<section>', methods=['GET'])
def guide_section(section):
    cur = get_db().execute("select road from personnel where section = '" + section + "'")
    rv = cur.fetchall()
    data = list()
    for row in rv:
        data.append(make_dicts(cur, row))
        
    #res = json.decoder( data )
    #for row in rv:
        #print(row)
    print(data[0]['road'])
    #query = data[0]['road']
    #requests.get('http://192.168.252.107/'+query)
    #sendToArduino(section)
    
    #serialcomm.write(section.encode())
    serialcomm.write(data[0]['road'].encode())
    
    return "Trajet " + section + " ==> " + data[0]['road']


@app.route('/api/command/<direction>', methods=['GET'])
def guide_with_command(direction):
    
    print(direction)

    #serialcomm.write(section.encode())
    serialcomm.write(direction.encode())
    
    return "Commande " + direction

# @app.route('/api/visite/manager', methods=['GET'])
# def get_tasks():
#     cur = get_db().execute("select * from personnel")
#     rv = cur.fetchall()
#     data = list()
#     for row in rv:
#         print(make_dicts(cur, row))
#         data.append(make_dicts(cur, row))
#     #res = json.decoder( data )
#     #for row in rv:
#         #print(row)
#     print(data)
#     #Connexion au serveur
#     sio.emit('guide-personal', data, namespace='/api')
#     return 200

@app.route('/api/song/<states>', methods=['GET'])
def start_singing(states):
    if(states != "on"):
        states = "off"
    sio.emit('start-song', states, namespace='/api')
    return "Soit je chante, soit je chante pas"

@app.route('/api/parler/<data>', methods=['GET'])
def speak_info_section(data):
    sio.emit('speak-section', data, namespace='/api')
    return data

@app.route("/api/personnel/add", methods=['POST'])
def post_tasks():
    data = request.get_json()
    cur = get_db().execute('''
        INSERT INTO personnel(nom, prenoms, contact, photo, poste, description)
            VALUES(?,?,?,?,?,?) ''', (data['nom'], data['prenoms'], data['contact'], data['photo'], data['poste'], data['description']))
    get_db().commit()
    return str(cur.lastrowid)


@app.route('/api/personnel/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/personnel', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'nom': request.json['nom'],
        'prenoms': request.json['prenoms'],
        'contact': request.json['contact'],
        'photo': request.json['photo'],
        'poste': request.json['poste'],
        'description': request.json['description'],
        #'prenoms': request.json.get('description', ""),
	#'description':request.json['description'],
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/api/personnel/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'nom' in request.json and type(request.json['nom']) != unicode:
        abort(400)
    if 'prenoms' in request.json and type(request.json['prenoms']) != unicode:
        abort(400)
    if 'contact' in request.json and type(request.json['contact']) != unicode:
        abort(400)
    if 'photo' in request.json and type(request.json['photo']) != unicode:
        abort(400)
    if 'poste' in request.json and type(request.json['poste']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
   # if 'description' in request.json and type(request.json['description']) is not unicode:
        #abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['nom'] = request.json.get('nom', task[0]['nom'])
    task[0]['prenoms'] = request.json.get('prenoms', task[0]['prenoms'])
    task[0]['contact'] = request.json.get('contact', task[0]['contact'])
    task[0]['photo'] = request.json.get('photo', task[0]['photo'])
    task[0]['poste'] = request.json.get('poste', task[0]['poste'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    #task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/api/personnel/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


# Info manager section

@app.route('/api/section/manager/<section>', methods=['GET'])
def get_manager_section(section):
    cur = get_db().execute("select * from personnel where section = '"+ section+"'")
    rv = cur.fetchall()
    data = list()
    for row in rv:
        data.append(make_dicts(cur, row))
    
    print(data)
    #Connexion au serveur
    sio.emit('info-manager-section', data, namespace='/api')
    
    return "ok"

# Info section

@app.route('/api/section/<section>', methods=['GET'])
def get_section(section):
    cur = get_db().execute("select section_image from personnel where section = '"+ section+"'")
    rv = cur.fetchall()
    data = list()
    for row in rv:
        data.append(make_dicts(cur, row))
    
    print(data)
    #Connexion au serveur
    sio.emit('info-section', data, namespace='/api')
    
    return "ok"


if __name__ == '__main__':
    app.run(host=f.read(), port=6400)


