from win32gui import GetWindowText, GetForegroundWindow
import time
import psutil

class Game:
    def __init__(self,game_name,game_procces):
        self.game_name = game_name
        self.game_procces = game_procces
        self.is_game_procces_active = False
        while self.is_game_procces_active == False:
            for process in psutil.process_iter():
                if self.game_procces == process.name():
                    self.is_game_procces_active = True
                    break
            time.sleep(1)

    #check is game active window if not check procces list
    def is_game_still_in_proggress(self):
        if GetWindowText(GetForegroundWindow()) == self.game_name:
            return True
        else:
            for process in psutil.process_iter():
                if self.game_procces == process.name():
                    return False
            self.is_game_procces_active = False