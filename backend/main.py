import time
from datetime import datetime
import serial
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:xxxx@localhost/kyrsova"
CORS(app)
db = SQLAlchemy(app)



arduino_serial = serial.Serial("COM2", 9600, timeout=1)

password = 1234


class Action_with_Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, action, timestamp):
        self.action = action
        self.timestamp = timestamp


class Robber(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bad_password = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, bad_password, timestamp):
        self.bad_password = bad_password
        self.timestamp = timestamp


class Changed_password(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    changed_password = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, changed_password, timestamp):
        self.changed_password = changed_password
        self.timestamp = timestamp


@app.route('/home', methods=["POST"])
def home():
    data = request.get_json()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    if data.isnumeric():
        if int(data) == password:
            start_green()
            return "agree_password", 201

        if int(data) != password:
            db.session.add(Robber(data, dt_string))
            db.session.commit()
            send_command("buzz")
            return "bad_password", 202

    if data == "remove_alarm":
        db.session.add(Action_with_Alarm("remove_the_alarm", dt_string))
        db.session.commit()
        start_green()
    if data == "set_alarm":
        db.session.add(Action_with_Alarm("set_the_alarm", dt_string))
        db.session.commit()
        start_red()
    if data == "start_red":
        start_red()
    if data == "buzz":
        send_command("buzz")
    return "Ok", 200


@app.route('/change_password', methods=["POST"])
def change_password():
    data = request.get_json()
    global password
    password = int(data)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    db.session.add(Changed_password(password, dt_string))
    db.session.commit()
    return "Ok", 200

def set_password():
    cursor = db.cursor()



def start_green():
    send_command("start_led_green")
    send_command("end_led_red")


def start_red():
    send_command("start_led_red")
    send_command("end_led_green")


def send_command(command):
    arduino_serial.write(command.encode())
    print(command)
    time.sleep(5)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, use_reloader=False)
