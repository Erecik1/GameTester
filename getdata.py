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
        self.keyboard_events_array = []
        self.mouse_events_array = []
        self.start_time = time.time()
        self.interval = 0.1
        self.mouse = Controller()

    def current_time(self):
        return str(time.time() - self.start_time)

    def keyboard_press(self,key):
        self.is_game_over()
        item = (self.current_time(),key,self.mouse.position)
        self.keyboard_events_array.append(item)
    
    def mouse_press(self,x,y,button, pressed):
        self.is_game_over()
        item = (self.current_time(),button,(x,y))
        self.mouse_events_array.append(item)


    def is_game_over(self):
        game.is_game_still_in_proggress()
        if game.is_game_procces_active == False:
            self.save()

    def save(self):
        global keyboard_listener
        global mouse_listener
        keyboard_listener.stop()
        mouse_listener.stop()

        print("Files saved")
        print(self.keyboard_events_array)
        print(self.mouse_events_array)
        #np.savetxt('kbfile.csv', [self.keyboard_events_array], delimiter=':', fmt='%s')
        #np.savetxt('msfile.csv', [self.mouse_events_array], delimiter=':', fmt='%s')

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
    else:
        pass

def on_scroll(x, y, dx, dy):
    pass



#game = gameload.Game("League of Legends (TM) Client","League of Legends.exe")
game = gameload.Game("League of Legends","LeagueClient.exe")
data = DataCollector()


keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()