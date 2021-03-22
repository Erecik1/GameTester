from win32gui import GetWindowText, GetForegroundWindow
import time
import ifmain
import getdata

def main():
    game_name = "League of Legends (TM) Client"
    while GetWindowText(GetForegroundWindow()) != game_name:
        print("Waiting for game!")
        time.sleep(1)
    else:
        gamedata.get_frame()

ifmain.main()