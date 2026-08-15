from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json
import time
import os

app = Flask(__name__)

sensor_data = {}
last_update = 0

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with code: " + str(rc))
    client.subscribe("esp32/YOUR_STUDENT_ID/data")  # match your ESP32 sketch's topic exactly

def on_message(client, userdata, msg):
    global sensor_data, last_update
    payload = msg.payload.decode()
    print(f"Message received: {payload}")
    try:
        sensor_data = json.loads(payload)
        last_update = time.time()
    except json.JSONDecodeError:
        print("Invalid JSON received")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({**sensor_data, "last_update": last_update})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)