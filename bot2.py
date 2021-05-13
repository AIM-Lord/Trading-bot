#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 23:39:01 2021

@author: LordViola
"""

from threading import Thread
import time
import json
import datetime as dt
import requests
import pandas as pd


def bullish_engulfing(data):
    
    #cdstk_0 = data[['open', 'high', 'low', 'close']].loc[1,:] # terzultima candela
    cdstk_1 = data[['open', 'high', 'low', 'close']].loc[1,:] # penultima candela
    cdstk_2 = data[['open', 'high', 'low', 'close']].loc[2,:] # ultima candela
    
    print(cdstk_1)
    print(cdstk_2)
    
    # vedo se la prima è rossa e la seconda verde
    if cdstk_1['open'] > cdstk_1['close'] and cdstk_2['open'] < cdstk_2['close']:
        # engulfing
        if cdstk_1['open'] < cdstk_2['close'] and cdstk_1['close'] > cdstk_2['open']:
            print('engulfing')
            return True
        else:
            print('no engulfing')



class cspattern (Thread):

    def __init__(self, nome, bot, user):
        Thread.__init__(self)
        self.nome = nome
        self.bot = bot
        self.user = user	
        self.timeserver = 'http://api.binance.com/api/v3/time'	
        self.url = 'http://api.binance.com/api/v3/klines'		
        self.symbol = 'BATBTC'		
        self.interval = '1h'
        self.limit = '1000'			

    def run(self):
        time_started = time.time()
        timeout = 172800 # 48h in secondi

        while True: 

            if time.time() > time_started + timeout:
                self.bot.send_message(self.user,"Thread '" + self.name + "' terminato")
                return
            # ora attuale    
            endTime = str(json.loads(requests.get(self.timeserver).text)['serverTime'])    
            # 3 ore prima    
            startTime = str(int((pd.to_datetime(endTime,unit='ms') - dt.timedelta(hours=3)).timestamp()*1000))    
	      	
            reqparams = {
			    'symbol' : self.symbol,
			    'interval' : self.interval,
			    'startTime' : startTime,
			    'endTime' : endTime,
			    'limit' : self.limit
			    }

            new = pd.DataFrame(json.loads(requests.get(self.url, params = reqparams).text))
            names = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume',
                'Taker_buy_quote_asset_volume', 'ignore']
            new.columns = names
            
            if bullish_engulfing(new):
                self.bot.send_message(self.user,"Si è verificata una Bullish Engulfing su"+str(self.symbol))
                
            time.sleep(3601)	


        self.bot.send_message(self.user,"Thread '" + self.name + "' terminato")

