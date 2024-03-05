# Small Tuya Smart Life

This Python script integrates Tuya / Smart Life devices with a Flask web server. It allows you to control your Tuya / Smart Life devices through HTTP requests.

This is an infinitely simple primitive solution.

You can only switch devices on (Switch on 1, Switch off 0) and trigger commands.
With TAP TO RUN commands, devices can be turned on and off with one endpoint (In this case, it is enough to start the command with 1)
For example, if we want to turn a light on and off with a single endpoint. We need to make a command in the Tuya / Smart Life application, a command that always toggles the state.

In essence, it was written so that I could control a couple of my devices with my Android TV remote control and Smartwatch.
I run it on my Linux-based router, but it also works on Raspberry Pi, or anything that can run python.

## Requirements

    Python 3.x
    Flask
    Requests

## Installation

First, make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

Install Flask and Requests using pip:

```bash
pip install flask
pip install requests
```

## Configuration

- Replace `<username>` and `<password>` with your Tuya / Smart Life account credentials in the Python script.
- Modify the `countryCode`, `bizType`, and `from_name` variables according to your Tuya / Smart Life account region and preferences.

## Usage

1. Run the Python script:

```bash
python small-tuya-smartlife.py
```

2. The Flask server will start running on `http://localhost:6543` by default.

3. You can send HTTP requests to the Flask server endpoints to interact with your Tuya / Smart Life devices.

## API Endpoints

### List Devices

- **URL:** `/devices`
- **Method:** `GET`
- **Description:** Retrieves a list of Tuya / Smart Life devices associated with the account.
- **Response:** JSON array containing device information.

### Control Device

- **URL:** `/<dev_id>/<value>`
- **Method:** `GET`
- **Description:** Controls the specified Tuya Smart Life device.
- **Parameters:**
  - `dev_id`: The ID of the device to control.
  - `value`: The value to set for the device (e.g., 0 for OFF, 1 for ON).
- **Response:** JSON object indicating the success or failure of the control operation.

## Example

To list devices:

```bash
curl http://localhost:6543/devices
```

To control a device:

```bash
curl http://localhost:6543/<dev_id>/<value>
```

## Notes

- This integration requires internet access to communicate with the Tuya cloud services.
- Make sure to keep your Tuya / Smart Life account credentials secure.

## License

This project is licensed under the MIT License.
