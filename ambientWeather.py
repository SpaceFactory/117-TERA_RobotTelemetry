# pip install ambient_api
# AMBIENT_ENDPOINT=https://api.ambientweather.net/v1
# AMBIENT_API_KEY='e7c61078fb7c44998ef2bcdd0d810d8071593e57a2554546ad9e9d092b23e241'
# AMBIENT_APPLICATION_KEY='b5c8869e65da44c7b3f58ac291c1dda56e859539e46a4ac5837a96e0a9ea7265'
import sys
import time
import json 
import iothub_client
from ambient_api.ambientapi import AmbientAPI
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

api = AmbientAPI()
devices = api.get_devices()
device = devices[0]


# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=grasshopper.azure-devices.net;DeviceId=robotsensors;SharedAccessKey=SRnRK12KY+l7EQdXZFLx7gomZpxFkbqyeIPsJ+9or7U="


# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
MSG_TXT = "{\"TemperatureOut\":%f,\"HumidityOut\":%f,\"WindSpeedOut\": %f}"  

def send_confirmation_callback(message, result, user_context):
    print ("IoT Hub responded to message with status: %s" % (result))

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

client = iothub_client_init()


while True:
 try:
    msg_txt_formatted = MSG_TXT % (j["cursor_position"],j["command"],j["robot_time"])
    message = IoTHubMessage(msg_txt_formatted)
    client.send_event_async(message, send_confirmation_callback, None)
 except:
    print ( "Unexpected error %s from IoTHub" % iothub_error)

