
from threading import Thread
import time
import websocket, json, pprint

import datetime as dt
import requests
import pandas as pd
import json 



class BOT_1 (Thread):

    def __init__(self, nome, durata, bot, user):
        Thread.__init__(self)
        self.nome = nome
        self.durata = durata
        self.bot = bot
        self.user = user	
        self.timeserver = 'http://api.binance.com/api/v3/time'	
        self.url = 'http://api.binance.com/api/v3/klines'		
        self.symbol = 'BATBTC'		
        self.interval = '1h'		
        self.endTime = str(json.loads(requests.get(self.timeserver).text)['serverTime'])		
        self.startTime = str(int((pd.to_datetime(self.endTime,unit='ms') - dt.timedelta(hours=3)).timestamp()*1000))	
        self.limit = '1000'	
        self.reqparams = {
		    'symbol' : self.symbol,
		    'interval' : self.interval,
		    'startTime' : self.startTime,
		    'endTime' : self.endTime,
		    'limit' : self.limit
		    }
        self.new = list(pd.DataFrame(json.loads(requests.get(self.url, params = self.reqparams).text)).loc[:,5])
        self.volume_mean = [int(float(i)) for i in self.new]	
        self.volume_mean = sum(self.volume_mean) / len(self.volume_mean)


    def run(self):
        time_started = time.time()
        X = 2
        count = 0
        while True: 
            if time.time() > time_started + X:
                self.bot.send_message(self.user,"Thread '" + self.name + "' terminato")
                return

            startTime2 = str(int((pd.to_datetime(self.endTime,unit='ms') - dt.timedelta(hours=3)).timestamp()*1000))
	      	
            reqparams2 = {
			    'symbol' : self.symbol,
			    'interval' : self.interval,
			    'startTime' : startTime2,
			    'endTime' : self.endTime,
			    'limit' : self.limit
			    }

            new2 = pd.DataFrame(json.loads(requests.get(self.url, params = reqparams2).text)).loc[:,5]

			
            if float(new2[0]) > float(new2[1]) > float(new2[2]) > self.volume_mean:
                self.bot.send_message(self.user,"trigger attivato su"+str(self.symbol))
                run = False
            else:	
                self.bot.send_message(self.user,"trigger non attivato su"+str(self.symbol))	
            count = count +1	
            if count > 4:		
                run = False	
            time.sleep(60)	
        self.bot.send_message(self.user,"Thread '" + self.name + "' terminato")

