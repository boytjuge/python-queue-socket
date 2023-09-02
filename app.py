from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
clients = []  # To store connected clients
num = 0
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/queue')
def queue():
    return render_template('queue.html')


@app.route('/queue_data')
def queue_data():
    return render_template('queue_data.html')


@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)  # Add the client's session ID to the list
    emit('data', {'data': request.sid}, room=request.sid)
    print(f'Client {request.sid} connected')

@socketio.on('test')
def handle_message_test(message):
    data  = {"queue": "1", "msg":"เรียกคิว"}
   # for client in clients:
    emit('test', {'data': data["msg"] + str(message)  }, broadcast=True)


@socketio.on('json')
def json_message(message):
    for client in clients:
        emit('json', {'data': message, "c":clients }, room=client)



@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)  # Remove the client's session ID from the list
    print(f'Client {request.sid} disconnected')

@socketio.on('message')
def handle_message(message):
    for client in clients:
        emit('response', {'data': message}, room=client)



if __name__ == '__main__':
    socketio.run(app, debug=True)