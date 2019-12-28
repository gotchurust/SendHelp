import csv
import requests
import time
import sys
from datetime import datetime, timedelta
import pytz
import collections

buyaverage = 0
stockamount = 0
status = 'Buy'
budget = 1000
totalprofit = 0
BuyReq = 5
sheet = 2
total = 0

def Buy(Market):
    global buyaverage
    buyaverage = (float(Market[1][2]) + float(Market[1][3]))/2
    global stockamount, budget
    stockamount = budget // buyaverage
    print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
    print('buy:', format(buyaverage,'.2f'), 'stock:', format(stockamount,'.2f'))
    global status
    status = "Sell"
    return buyaverage, status, stockamount

def Sell(Market):
    sellaverage = (float(Market[1][2]) + float(Market[1][3]))/2
    print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
    print('Sell:', format(sellaverage,'.2f'))
    global buyaverage, stockamount
    profit = (sellaverage - buyaverage) * stockamount
    print('Profit:', format(profit,'.2f'))
    global totalprofit
    totalprofit = profit + totalprofit
    print("Total Profit", format(totalprofit,'.2f'))
    global status
    status = "Sell"
    return status, totalprofit

def GetOut(timestamp):
    Marketurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=UGAZ&interval=1min&apikey=DWTJCP0TP657X9J0&datatype=csv"
    with requests.Session() as s:
        download1 = s.get(Marketurl)
        decoded_Market = download1.content.decode('utf-8')
        list1 = csv.reader(decoded_Market.splitlines(), delimiter=",")
        Market = list(list1)
        lastaverage = (float(Market[1][2]) + float(Market[1][3]))/2
        global buyaverage
        if lastaverage > buyaverage:
            global stockamount, totalprofit
            profit = (lastaverage - buyaverage) * stockamount
            totalprofit = profit + totalprofit
            print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
            print("profit: ", format(profit,'.2f'), "total profit: ", format(totalprofit,'.2f'))
        else:
            pass

def Choice(timestamp):
    while True:
        Choice = []
        Choice = collections.deque(maxlen=5)
        Marketurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=UGAZ&interval=1min&apikey=DWTJCP0TP657X9J0&datatype=csv"
        EMAurl = "https://www.alphavantage.co/query?function=EMA&symbol=UGAZ&interval=1min&time_period=15&series_type=open&apikey=DWTJCP0TP657X9J0&datatype=csv"
        try:
            with requests.Session() as s:
                download1 = s.get(Marketurl)
                decoded_Market = download1.content.decode('utf-8')
                list1 = csv.reader(decoded_Market.splitlines(), delimiter=",")
                download2 = s.get(EMAurl)
                decoded_EMA = download2.content.decode('utf-8')
                list2 = csv.reader(decoded_EMA.splitlines(), delimiter=",")
                Market = list(list1)
                EMA = list(list2) 
                for i in range(1,6):
                    if Market[i][1]< EMA[i][1] and Market[i][2]<=EMA[i][1]:
                        action = 'Under'
                        Choice.append(action)
                    elif Market[i][3]>= EMA[i][1] and Market[i][4]> EMA[i][1]:
                        action = 'Over'
                        Choice.append(action)
                    else:
                        action = 'In'
                        Choice.append(action)
                Choice = list(Choice)
                Choice = [s.replace("'","") for s in Choice]
                    #print(Choice)
                    #print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
                Action(Choice, Market)
                break
        except:
            print('error')
            break
        
def Action(Choice, Market):
    Count = 0
    global BuyReq
    if Choice[0] == "In":
        global status
        for i in range(1,BuyReq + 1):
            if Choice[i] == "Under" and status == "Buy": #and Choice[1] =="Under" and Choice[1] =="Under" and Choice[1] =="Under" and
                Count = Count + 1
                #print('Buy')
            elif Choice[i] == "Over" and status == "Sell":
                Count = Count - 1
                #print('Sell')
            else:
                pass
            if Count == BuyReq:
                #print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
                #print('Buy')
                Buy(Market)
            elif Count == -(BuyReq):
                #print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
                #print('Sell')
                Sell(Market)
            else:
                #print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
                print('do nothing')
    else:
        #print("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
        print('moshmosh')
        pass
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
def Program():
    time_start = time.time()
    future = time_start + 60
    NY = pytz.timezone("America/New_York")
    timestamp = datetime.now(NY)
    finish = timestamp.replace(day=timestamp.day + 0, hour=15, minute=30, second=0, microsecond=0) + timedelta(days=0)

    while True:
        if timestamp >= finish:
            if status == 'Sell':
                #Getout()
                print("total profit:", totalprofit)
                break
            else:
                print("total profit:", totalprofit)
                break 
        elif time.time() > future: #runs the action program until it reaches finish
            timestamp = datetime.now(NY)
            t1 = datetime.now(NY)
            print ("%s:%s:%s" % (timestamp.hour % 12,timestamp.minute,timestamp.second))
            Choice(timestamp)
            sys.stdout.flush()
            t2 = datetime.now(NY)
            print('processing time:', t2-t1)
            time.sleep(55) #waits 5 seconds before running the time
            continue
        
Program()