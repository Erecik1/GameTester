import numpy as np
import pandas as pd 
import seaborn as sns
from win32api import GetSystemMetrics

class DataProcces:
    def __init__(self, input_data, game_api_data=[], game_duration=1080):
        self.input_data = input_data
        self.game_duration = game_duration
        self.game_api_data = game_api_data
        self.screen_res = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.heatmap_make()
        self.apm_calculate()

    def heatmap_make(self):
        timeline_list = []
        button_list = []
        ox_list = []
        oy_list = []
        for lane in self.input_data:
            timeline = lane[0]
            button = lane[1]
            x,y = lane[2]
            timeline_list.append(timeline)
            button_list.append(button)
            ox_list.append(x)
            oy_list.append(y)
        data = {
            "time":timeline_list,
            "button":button_list,
            "x": ox_list,
            'y': oy_list
        }
        df = pd.DataFrame(data=data)
        self.input_data = df

    def apm_calculate(self):
        avarage_apm = len(self.input_data) / self.game_duration
        avarage_apm_per_min = 0
        max_time_value = self.input_data[-1:]['time'].values[0]
        print(type(max_time_value))
        for index, row in self.input_data.iterrows():
            time_row = row['time']
            index = time_row/max_time_value



    def data_frame_return(self):
        return self.input_data
