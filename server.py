from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
userinformation = {"rx434@nyu.edu": "123456"}

# This is a test
@socketio.on('connect', namespace="/")
def test_connect():
    print("One user connect to index")
    emit('connection', {'data': 'Connected'})

@socketio.on('connect', namespace="/next_page")
def test_connect2():
    print("One user connect to next_page")


@socketio.on('disconnect')
def test_disconnect():
    print("One user disconnect.")

@socketio.on('connection')
def connection_success(message):
    msg = "Hello " + session['username'] + "!"
    emit('connection success', msg)

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        if session.get('username') != None:
            session.pop('username')
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']

        recordedpassword = userinformation.get(username, 'NULL')
        if recordedpassword == 'NULL':
            return render_template('login.html', error='Unknown username!')
        elif recordedpassword != password:
            return render_template('login.html', error='Wrong password!')
        else:
            session['username'] = username
            return render_template('test.html')

@app.route('/register', methods=['GET', 'POST'])
def toregister():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        find_existing_username = userinformation.get(username, 'NULL')
        if find_existing_username != 'NULL':
            return render_template('register.html', error='The username already exists!')
        elif confirm != password:
            return render_template('register.html', error='Your password and comfirm are not the same!')
        else:
            userinformation[username] = password
            return render_template('register.html', success='Success!')

@app.route("/next_page")
def page():
    return render_template("next_page.html")

@socketio.on('my event')
def my_event(message):
    emit('my response', {'data': message['data'], 'time': message['time']})



# @app.route('/ajax', methods = ['POST'])
# def ajax_request():
#     username = request.form['username']
#     time = request.form['time']
#     return jsonify(username=username, time=time)
    
    
if __name__ == "__main__":
    socketio.run(app, debug=True)
