import serial
from serial import Serial
from numpy import interp
import json
import time
import os

testing_without_connection = False

# wenn es nicht get "sudo chmod 666 /dev/ttyUSB0" im terminal
class Serial_Driver:
    def __init__(self, port = "COM12"):
        if not testing_without_connection:
            self.ser = serial.Serial(port, baudrate=115200)
        self.data_recived = {}
        self.start_process = False
    
    
    def send(self, data):
        data = json.dumps(data)

        
        if not testing_without_connection:
            self.ser.write((data + '\n').encode( "utf-8"))
            #print(data)
            data_from_teensy = self.recive_data()

        if testing_without_connection:
            data_from_teensy = {"buttonState": True}
            print(data)
        self.data_recived = data_from_teensy
        
        



    def ask_for_data(self):
        json_data = {
            "type": "ask"
        }
        self.send(json_data)

    def send_position(self,pos, speed = 10):
        json_data = {
            "type": "move_slide",
            "position": pos,
            "speed": speed
        }
        self.send(json_data)


    def change_band_data(self,state, speed):
        json_data = {
            "type": "move_conveyor",
            "conveyor_running": state,
            "conveyor_speed": speed
        }
        self.send(json_data)

    def controll_vib_motor(self,state):
        json_data = {
            "type": "vib_motor",
            "state": state 
        }
        self.send(json_data)

    def feed_it(self, with_which_one: int, delay: int):
        json_data = {"type": "feed", "selection": with_which_one, "delay": delay}
        self.send(json_data)

    def recive_data(self): 
        while True:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                print(response)
                try:
                    ack = json.loads(response)
                    return ack
                except json.JSONDecodeError:
                    print("Received invalid JSON:", response)
        
            




