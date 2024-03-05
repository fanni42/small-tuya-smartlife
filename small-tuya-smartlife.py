from flask import Flask, request, jsonify
import requests
import threading
import time

"""
Required to run:
pip install flask
pip install requests
"""

app = Flask(__name__)

username = "" # Your username
password = "" # Your password
countryCode = "eu" # az, eu, ay, us, cn
bizType = "smart_life" # tuya or smart_life
from_name = "small-tuya-smartlife" # whatever you want
token_lock = threading.Lock()
access_token = None
last_discovery_time = None
cached_device_list = None

def get_access_token():
    global access_token
    while True:
        auth = requests.post(
            "https://px1.tuya"+countryCode+".com/homeassistant/auth.do",
            data={
                "userName": username,
                "password": password,
                "countryCode": countryCode,
                "bizType": bizType,
                "from": from_name,
            },
        ).json()
        with token_lock:
            access_token = auth.get("access_token")
            print("Token received successfully at:", time.strftime("%Y-%m-%d %H:%M:%S"))
        if access_token:
            time.sleep(864000)
        else:
            time.sleep(180)

token_thread = threading.Thread(target=get_access_token)
token_thread.daemon = True
token_thread.start()

@app.route("/devices", methods=["GET"])
def list_devices():
    global access_token, last_discovery_time, cached_device_list
    if access_token:
        # Check when was the last discovery request made
        if last_discovery_time is not None:
            time_since_last_discovery = time.time() - last_discovery_time
            if time_since_last_discovery < 1020 and cached_device_list is not None:
                return jsonify(cached_device_list)

        devices_response = requests.post(
            "https://px1.tuya" + countryCode + ".com/homeassistant/skill",
            json={"header": {"name": "Discovery", "namespace": "discovery", "payloadVersion": 1},
                  "payload": {"accessToken": access_token}}
        )
        print("Devices Response:", devices_response.text)  # Print the raw response for debugging
        devices = devices_response.json()

        if 'header' in devices and 'code' in devices['header'] and devices['header']['code'] == "FrequentlyInvoke":
            return jsonify({"error": "You can only perform discovery once in 1020 seconds."}), 429
        elif 'payload' in devices and 'devices' in devices['payload']:
            last_discovery_time = time.time()  # Update the last discovery time
            cached_device_list = [{"name": dev["name"], "id": dev["id"]} for dev in devices["payload"]["devices"]]
            return jsonify(cached_device_list)
        else:
            return jsonify({"error": "No devices found in the response."}), 500
    else:
        return jsonify({"error": "No access token available."}), 500

@app.route("/<path:dev_id>/<int:value>", methods=["GET"])
def control_device(dev_id, value):
    global access_token
    if access_token:
        turnonoff = requests.post(
            "https://px1.tuya"+countryCode+".com/homeassistant/skill",
            json={"header": {"name": "turnOnOff", "namespace": "control", "payloadVersion": 1}, "payload": {"accessToken": access_token, "devId": dev_id, "value": str(value)}}
        ).json()
        return jsonify(turnonoff)
    else:
        return jsonify({"error": "No access token available."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6543)
