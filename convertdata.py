import requests
import time
import json

class ConvertData:

    def __init__(self, event_list):
        #api response is diffrent on diffrents modes
        #http://static.developer.riotgames.com/docs/lol/queues.json 
        self.game_mode_list = (
            700,
            440,
            430,
            420,
            400,
        )
        self.event_list = event_list
        self.champion_played = ""
        self.game_mode = 0
        #time in secs
        self.game_duration = 0
        with open('login_data.json') as f:
            data = json.load(f)
        self.summoner_name = data['summoner_name']
        self.server = data['server']
        self.api_key = data['api_key']
        self.API_URL = f"https://{self.server}.api.riotgames.com/"
        self.headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": self.api_key
        }
        self.summoner_id = self._get_summoner_id()
        self.last_match_id = self._get_last_match_id(self.summoner_id)
        self.match_data = self._get_match_data_by_id(self.last_match_id)
    


    def _one_day_ago_in_epoch(self):
        now = time.time()
        #days before now
        secs_in_day = 5*24*60*60
        epoch_time = now - secs_in_day
        #riot api needs time in milliseconds
        epoch_time *= 1000
        return int(epoch_time)

    def _get_summoner_id(self):
        SUMMONER_ID_URL = f"/lol/summoner/v4/summoners/by-name/{self.summoner_name}"
        url = self.API_URL + SUMMONER_ID_URL
        r = requests.get(url, headers=self.headers)
        #validate
        if r.status_code != 200:
            raise Exception("ApiKey or summonersName error")
        output = r.json()['accountId']
        return output

    def _get_last_match_id(self,summoner_id):
        MATCH_URL = f"/lol/match/v4/matchlists/by-account/{summoner_id}?beginTime={self._one_day_ago_in_epoch()}"
        url = self.API_URL + MATCH_URL
        #waiting for riot servers to sync match_data
        #time.sleep(120)
        r = requests.get(url, headers=self.headers)
        output = r.json()
        #validate
        if output["totalGames"] == 0:
            raise Exception("No game in match history for last 24h")
        self.champion_played = output['matches'][0]['champion']
        self.game_mode = output['matches'][0]["queue"]
        self.game_mode = self.game_mode in self.game_mode_list
        output = output['matches'][0]['gameId']
        return output

    def _get_match_data_by_id(self,match_id):
        MATCH_URL = f"/lol/match/v4/matches/{match_id}"
        url = self.API_URL + MATCH_URL
        r = requests.get(url, headers=self.headers)
        output = r.json()

        #check for player in game id
        for player in output['participantIdentities']:
            if player['player']['accountId'] == self.summoner_id:
                in_game_id = player['participantId']
                break
        self.game_duration = output['gameDuration']
        output = output['participants'][int(in_game_id)-1]

        return output

    def dump_data(self):
        game_data = self.match_data
        print(game_data)
        win = False if game_data['stats']['win'] == 'false' else True
        #think about it
        if self.game_mode:
            cs_per_min_at_10 = game_data['timeline']['creepsPerMinDeltas']['0-10']
            cs_diff_at_10 = game_data['timeline']['csDiffPerMinDeltas']['0-10']
            xp_per_min_at_10 = game_data['timeline']['xpPerMinDeltas']['0-10']
            xp_diff_at_10 = game_data['timeline']['xpDiffPerMinDeltas']['0-10']
            gold_per_min_at_10 = game_data['timeline']['goldPerMinDeltas']['0-10']
        
            stats_dict = {
                'win': win,
                'cs_per_min_at_10' : cs_per_min_at_10,
                'cs_diff_at_10': cs_diff_at_10,
                'xp_per_min_at_10': xp_per_min_at_10,
                'xp_diff_at_10': xp_diff_at_10,
                'gold_per_min_at_10': gold_per_min_at_10
            }
        else: 
            stats_dict = {
                'win': win,
            }
        return stats_dict, self.game_duration

#testing class
#obj = ConvertData([0,0])