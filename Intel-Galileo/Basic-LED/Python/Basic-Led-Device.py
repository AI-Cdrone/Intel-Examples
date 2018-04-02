# *****************************************************************************
# Copyright (c) 2014 Adam Milton-Barker.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#   Adam Milton-Barker
# *****************************************************************************

import time
import sys
import json

import mraa
import techbubbleiotjumpwaymqtt.device

class BasicLED():

    def __init__(self):

        self.JumpWayMQTTClient = ""
        self.configs = {}

        with open('config.json') as configs:
            self.configs = json.loads(configs.read())

        self.LED = mraa.Gpio(self.configs["Sensors"]["LED"]["PIN"])
        self.LED.dir(mraa.DIR_OUT)
        self.LED.write(0)

        self.startMQTT()

    def deviceCommandsCallback(self,topic,payload):

        print("Received command data: %s" % (payload))

        jsonData = json.loads(payload.decode("utf-8"))

        if jsonData['ActuatorID']==self.configs["Sensors"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':

            print('Turning ON')
            self.LED.write(1)

        elif jsonData['ActuatorID']==self.configs["Sensors"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':

            print('Turning OFF')
            self.LED.write(0)

    def startMQTT(self):

        try:

            self.JumpWayMQTTClient = techbubbleiotjumpwaymqtt.device.JumpWayPythonMQTTDeviceConnection({
				"locationID": self.configs["IoTJumpWaySettings"]["SystemLocation"],
				"zoneID": self.configs["IoTJumpWaySettings"]["SystemZone"],
				"deviceId": self.configs["IoTJumpWaySettings"]["SystemDeviceID"],
				"deviceName": self.configs["IoTJumpWaySettings"]["SystemDeviceName"],
				"username": self.configs["IoTJumpWayMQTTSettings"]["username"],
				"password": self.configs["IoTJumpWayMQTTSettings"]["password"]
			})

        except Exception as e:
            print(str(e))
            sys.exit()

        self.JumpWayMQTTClient.connectToDevice()
        self.JumpWayMQTTClient.subscribeToDeviceChannel("Commands")
        self.JumpWayMQTTClient.deviceCommandsCallback = self.deviceCommandsCallback

BasicLED = BasicLED()

while True:

    time.sleep(1)

BasicLED.JumpWayMQTTClient.disconnectFromDevice()