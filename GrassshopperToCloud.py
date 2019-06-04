import sys
import time
import json 

import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=grasshopper.azure-devices.net;DeviceId=grasshopper;SharedAccessKey=h3hETAZHqyz+eQTLBT480btlxmzrmBVBFYO/qlI4cok="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
MSG_TXT = "{\"cursor_position\":%d,\"command\":\"%s\",\"robot_time\": \"%s\"}"  

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

client = iothub_client_init()
old_seq_no = 13


# Try to open a file to read, if not found wait and retry
FileNotFound = True
while FileNotFound:
 try:
  f = open('C:\\GrasshopperToCloud\\commonfile.txt','r')
  FileNotFound = False
 except:
  print("File not found trying again after 5 seconds")
  time.sleep(5)
f.close()
fr = open('C:\\GrasshopperToCloud\\commonfile.txt','r')
 
while True:
 fr.seek(0)
 telemetry = fr.read()
 if(telemetry !=''):
  try:
   j= json.loads(str(telemetry))
   if(old_seq_no!= int(j['message_id'])):
    print("Sending data to IoT Hub")
    print(telemetry)
    print('\n\n')
    old_seq_no= int(j['message_id'])
    try:
     msg_txt_formatted = MSG_TXT % (j["cursor_position"],j["command"],j["robot_time"])
     message = IoTHubMessage(msg_txt_formatted)
     client.send_event_async(message, send_confirmation_callback, None)
    except:
     print ( "Unexpected error %s from IoTHub" % iothub_error)
  except:
    print("Message not in proper format")   
 time.sleep(0.0625)
fr.close()
 
 
 
 
 


