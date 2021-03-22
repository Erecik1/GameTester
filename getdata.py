import numpy as np
import pandas
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import logging
import time
import gameload

class DataCollector:

    def __init__(self):
        self.keyboard_events_array = np.array([],dtype='string')
        self.mouse_events_array = np.array([],dtype='string')
        self.start_time = time.time()
        self.interval = 0.1
        self.mouse = Controller()

    def current_time(self):
        return str(time.time() - self.start_time)

    def keyboard_press(self,key):
        item = np.array([current_time(),key,self.mouse.position],dtype='string')
        self.keyboard_events_array = np.append(keyboard_events_array,item)
    
    def mouse_press(self,x,y,button):
        item = np.array([current_time(),button,x,y],dtype='string')
        self.mouse_events_array = np.append(keyboard_events_array,item)

    def save(self):
        print(self.keyboard_events_array)
        print(self.mouse_events_array)

#keyboard
def on_press(key):
    data.keyboard_press(key)

def on_release(key):
    pass

#mouse
def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    if pressed:
        data.mouse_press(x,y,button,pressed)

def on_scroll(x, y, dx, dy):
    pass



game = gameload.Game("League of Legends (TM) Client","League of Legends.exe")
data = DataCollector()


keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()