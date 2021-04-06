import numpy as np
import pandas as pd 
import seaborn as sns
from win32api import GetSystemMetrics

class DataProcces:
    def __init__(self, input_data, game_api_data=[], game_duration):
        self.input_data = input_data
        self.game_duration = game_duration
        self.game_api_data = game_api_data
        self.screen_res = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.heatmap_make()
        self.apm_per_minute_array = self.apm_calculate()
        self.avarage_apm = len(self.input_data) / (self.game_duration/60)

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
        apm_per_minute_array = []
        actions = 0
        avarage_apm_per_min = 0
        max_time_value = self.input_data[-1:]['time'].values[0]
        for index, row in self.input_data.iterrows():
            actions += 1
            time_row = row['time']
            index = int(time_row/60)
            try: 
                apm_per_minute_array[index] += 1
            except IndexError:
                apm_per_minute_array.append(1)
        return apm_per_minute_array



    def data_frame_return(self):
        output = [self.input_data, self.apm_per_minute_array, self.avarage_apm]
        return output
