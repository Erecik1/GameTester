import getdata
import convertdata
import gameload
import sys

#game = gameload.Game("League of Legends (TM) Client","League of Legends.exe")
game = gameload.Game("League of Legends","LeagueClient.exe")
data = getdata.DataCollector(game)
output = data.save()
convert = convertdata.ConvertData(output)