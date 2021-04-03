from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import time
import datetime
import convertdata
import numpy as np

class DataCollector(MouseListener,KeyboardListener):

    def __init__(self,game_object):
        self.game_object = game_object
        self.events_list_array = []
        self.start_time = time.time()
        self.interval = 0.1
        self.mouse_count = 0
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
            print("here")
            self.keyboard_listener.stop()
            self.mouse_listener.stop()

    def _current_time(self):
        clock = time.time() - self.start_time
        clock = round(clock, 3)
        return clock

    def _current_day(self):
        dt_date = datetime.datetime.now()
        return dt_date.strftime("%d_%m_%Y")

    def _keyboard_press(self,key):
        item = [self._current_time(),str(key),self.mouse.position]
        self.events_list_array.append(item)
    
    def _mouse_press(self,x,y,button, pressed):
        self.mouse_count += 1
        if self.mouse_count % 5 == 0:
            self._is_game_over()
            self.mouse_count = 0
        item = [self._current_time(),str(button),(x,y)]
        self.events_list_array.append(item)



    def _is_game_over(self):
        self.game_object.is_game_still_in_proggress()
        if self.game_object.is_game_procces_active == False:
            self.listener_on(False)

    def save(self):
        #check data
        if len(self.events_list_array) == 0:
            raise Exception("No data recorded")

        print("Files saved")
        return self.events_list_array, self.start_time()

    #keyboard
    def on_press(self,key):
        self._keyboard_press(key)

    def on_release(self,key):
        pass

    #mouse
    def on_move(self,x, y):
        pass

    def on_click(self,x, y, button, pressed):
        if pressed:
            self._mouse_press(x,y,button,pressed)
        else:
            pass

    def on_scroll(self, x, y, dx, dy):
        pass