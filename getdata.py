import numpy as np
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import time
import pandas as ps
import datetime

class DataCollector(MouseListener,KeyboardListener):

    def __init__(self,game_object):
        self.game_object = game_object
        self.keyboard_events_array = []
        self.mouse_events_array = []
        self.start_time = time.time()
        self.interval = 0.1
        self.mouse = Controller()
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.listener_on(True)

    def listener_on(self,statment):
        if statment == True:
            self.keyboard_listener.join()
            self.mouse_listener.join()
        elif statment == False:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()

    def current_time(self):
        clock = time.time() - self.start_time
        clock = round(clock, 3)
        return str(clock)

    def current_day(self):
        dt_date = datetime.datetime.now()
        return dt_date.strftime("%d_%m_%Y")

    def keyboard_press(self,key):
        self.is_game_over()
        item = [self.current_time(),key,self.mouse.position]
        self.keyboard_events_array.append(item)
    
    def mouse_press(self,x,y,button, pressed):
        self.is_game_over()
        item = [self.current_time(),button,(x,y)]
        self.mouse_events_array.append(item)


    def is_game_over(self):
        self.game_object.is_game_still_in_proggress()
        if self.game_object.is_game_procces_active == False:
            self.save()
            self.listener_on(False)

    def save(self):
        np.savetxt(f"keyboard_{self.current_day()}.csv", 
                self.keyboard_events_array,
                delimiter =", ", 
                fmt ='% s')
        np.savetxt(f"mouse_{self.current_day()}.csv", 
                self.mouse_events_array,
                delimiter =", ", 
                fmt ='% s')

        self.keyboard_events_array = []
        self.mouse_events_array = []
        print("Files saved")

#keyboard
    def on_press(self,key):
        self.keyboard_press(key)

    def on_release(self,key):
        pass

    #mouse
    def on_move(self,x, y):
        pass

    def on_click(self,x, y, button, pressed):
        if pressed:
            self.mouse_press(x,y,button,pressed)
        else:
            pass

    def on_scroll(self, x, y, dx, dy):
        pass