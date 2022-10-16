#for token gererating files
#########################################################
flag2=0 # banknifty 9:22 (If you want to stop strategy put 1)
flag3=0 # 12:30 nifty (If you want to stop strategy put 1)
trading_day2=['Monday','Wednesday', 'Tuesday', 'Thursday'] # banknifty 9:22
trading_day3=['Monday','Wednesday', 'Tuesday', 'Thursday']# 12:30 nifty
##############################################
b_lot=1 #Banknifty Lot Size
n_lot=1 #Nifty Lot Size
##############################################
import urllib.request, urllib.parse, urllib.error
import json
import pandas as pd
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
new_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#headers = {'User-Agent': 'Mozilla/5.0'}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en,en-US;q=0.9,ar;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
uh = urllib.request.urlopen(new_url, context=ctx)
data = uh.read().decode()

df = pd.DataFrame(columns=["token","symbol","name","expiry","strike","lotsize","instrumenttype","exch_seg","tick_size"])
js = json.loads(data)
da=pd.DataFrame(js)
token=da[da['instrumenttype']=='OPTIDX']
token.to_csv('symbol_token.csv')
#################################################
#lgoin file
#Please login to https://smartapi.angelbroking.com/ for create API keys
from smartapi import SmartConnect
api_key='APIKey' #API Key
secret='API Secret' #API Secret
obj=SmartConnect(api_key=api_key)
c_id='userID'# User ID
pas='Password'# Password
data = obj.generateSession(c_id,pas)
refreshToken= data['data']['refreshToken']
#fetch the feedtoken
feedToken=obj.getfeedToken()
#fetch User Profile
userProfile= obj.getProfile(refreshToken)
userProfile
#expiry file
#exp='04FEB21'
##############################################
import pandas as pd 
import datetime
tdat=datetime.datetime.now().strftime('%d%b%Y')
token=pd.read_csv('symbol_token.csv')
a=token[token['name']=='NIFTY']
expiry=a['expiry'].to_list()
expiry=set(expiry)
expiry=list(expiry)
expiry.sort(key=lambda date: datetime.datetime.strptime(date, "%d%b%Y"))
expiry=list(set(expiry))
exp=''
for ex in expiry:
    aaa=datetime.datetime.strptime(ex, '%d%b%Y') -datetime.datetime.strptime(tdat,'%d%b%Y')
    #print(aaa.days)
    if aaa.days <7 and aaa.days>=0:
        exp=ex
        print(ex)
    


exp=exp[0:5]+'21' 
a=obj.ltpData('NSE','BANKNIFTY','26009')['data']['ltp']#for banknifty
strb=100*round(a/100)
#exp='19FEB21'
bce='BANKNIFTY'+ exp+ str(strb)+ 'CE'
tok=int(token[token['symbol']==bce]['token'])
if obj.ltpData('NFO',bce,tok)['data']['ltp']:#for banknifty!=None:
    print('expiry ok')
import datetime
from  threading import Thread
import time

def modify_order(orid,odty,p,ty,tok,q):
    orderparams ={"variety":"NORMAL", "orderid":orid, "ordertype":odty,"producttype":"INTRADAY",
                  "duration":"DAY", "price":p,"quantity":q,"tradingsymbol":ty,"symboltoken":tok,
            "exchange":"NFO"
            }
    order_id=obj.modifyOrder(orderparams)
    return order_id
    
def order(variety,sy,tok,ty,exchange,odrty,p,q):
    #place order
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": sy,
            "symboltoken": tok,
            "transactiontype": ty,
            "exchange": exchange,
            "ordertype": odrty,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": p,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": q
            }
        orderId=obj.placeOrder(orderparams)
        return orderId
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))

    #logout
    try:
        logout=obj.terminateSession('Your Client Id')
        print("Logout Successfull")
    except Exception as e:
        print("Logout failed: {}".format(e.message))
#################################
def sl(variety,sy,tok,ty,exchange,odrty,p,q):
    #place order
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": sy,
            "symboltoken": tok,
            "transactiontype": ty,
            "exchange": exchange,
            "ordertype": odrty,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": '0',
            "triggerprice": p,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": q,
            }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
        return orderId
    except Exception as e:
        print("Order placement failed: {}".format(e.message))

    #logout
    try:
        logout=obj.terminateSession('Your Client Id')
        print("Logout Successfull")
    except Exception as e:
        print("Logout failed: {}".format(e.message))
###############################    
dt=datetime.datetime.now()
while datetime.datetime.now() <datetime.datetime(dt.year, dt.month, dt.day, 9, 20):
    time.sleep(1)
while datetime.datetime.now() <datetime.datetime(dt.year, dt.month, dt.day, 15, 10):
     
    #print('working')

    if datetime.datetime.now() >datetime.datetime(dt.year, dt.month, dt.day, 9, 22) and flag2==0 and datetime.datetime.today().strftime("%A") in trading_day2 :
        #a=kite.ltp('NSE:NIFTY 50')['NSE:NIFTY 50']['last_price']
        #strn=50*round(a/50)
        flag2=1
        print('BNIFTY-ALLWEATHER-922 Executed')
        try:
            a=obj.ltpData('NSE','BANKNIFTY','26009')['data']['ltp']#for banknifty
        except:
            time.sleep(5)
            a=obj.ltpData('NSE','BANKNIFTY','26009')['data']['ltp']#for banknifty
        strb=100*round(a/100)
        #nce='NIFTY21'+ exp+ str(strn)+ 'CE'
        #npe='NIFTY21'+ exp+ str(strn)+ 'PE'
        bce='BANKNIFTY'+ exp+ str(strb)+ 'CE'
        bpe='BANKNIFTY'+ exp+ str(strb)+ 'PE'
        bcet=int(token[token['symbol']==bce]['token'])
        bpet=int(token[token['symbol']==bpe]['token'])
        Thread(target=order('NORMAL',bce,bcet,'SELL','NFO','MARKET',0,25*b_lot))
        #order('NORMAL','NIFTY21JAN2114500PE','58343','BUY','NFO','MARKET',0)
        Thread(target=order('NORMAL',bpe,bpet,'SELL','NFO','MARKET',0,25*b_lot))
        #obj.ltpData('NFO',bce,tok)['data']['ltp']
        slbce=round(1.32*obj.ltpData('NFO',bce,bcet)['data']['ltp']  ,1) # SL Change CE
        slbpe=round(1.32*obj.ltpData('NFO',bpe,bpet)['data']['ltp']   ,1)# SL Change PE
        #sl('STOPLOSS','PNB-EQ','10666','SELL','NSE','SL MARKET',38)
        #be_ce1=sl_order('NFO',bce,'BUY',25,slbce)
        be_ce1=sl('STOPLOSS',bce,bcet,'BUY','NFO','STOPLOSS_MARKET',slbce,25*b_lot)
        time.sleep(1)
        be_pe1=sl('STOPLOSS',bpe,bpet,'BUY','NFO','STOPLOSS_MARKET',slbpe,25*b_lot)
    #################################################3
    time.sleep(1)
    if datetime.datetime.now() >datetime.datetime(dt.year, dt.month, dt.day, 12, 30) and flag3==0 and datetime.datetime.today().strftime("%A") in trading_day3:
        try:
            a=obj.ltpData('NSE','NIFTY','26000')['data']['ltp']#for nifty
        except:
            time.sleep(5)
            a=obj.ltpData('NSE','NIFTY','26000')['data']['ltp']#  
        strn=50*round(a/50)
        flag3=1 
        print('NIFTY-SAFE Executed')
        nce='NIFTY'+ exp+ str(strn)+ 'CE'
        npe='NIFTY'+ exp+ str(strn)+ 'PE'
        ncet=int(token[token['symbol']==nce]['token'])
        npet=int(token[token['symbol']==npe]['token'])
        Thread(target=order('NORMAL',nce,ncet,'SELL','NFO','MARKET',0,75*n_lot))
        #order('NORMAL','NIFTY21JAN2114500PE','58343','BUY','NFO','MARKET',0)
        Thread(target=order('NORMAL',npe,npet,'SELL','NFO','MARKET',0,75*n_lot))
        #obj.ltpData('NFO',bce,tok)['data']['ltp']
        slnce=round(1.4*obj.ltpData('NFO',nce,ncet)['data']['ltp']  ,1)# SL Change CE
        slnpe=round(1.4*obj.ltpData('NFO',npe,npet)['data']['ltp']   ,1)# SL Change PE
        #sl('STOPLOSS','PNB-EQ','10666','SELL','NSE','SL MARKET',38)
        #be_ce1=sl_order('NFO',bce,'BUY',25,slbce)
        ne_ce1=sl('STOPLOSS',nce,ncet,'BUY','NFO','STOPLOSS_MARKET',slnce,75*n_lot)
        time.sleep(1)
        ne_pe1=sl('STOPLOSS',npe,npet,'BUY','NFO','STOPLOSS_MARKET',slnpe,75*n_lot)
    ###################################    
while datetime.datetime.now() <datetime.datetime(dt.year, dt.month, dt.day, 15, 10):
       time.sleep(10)  

#####################################
try:
     modify_order(be_ce1,'MARKET',0,bce,bcet,25*b_lot)# exit at 3.10 pm
    print('exit banknifty ce')   
except:
    pass
try:
    modify_order(be_pe1,'MARKET',0,bpe,bpet,25*b_lot)# exit at 3.10 pm
    print('exit banknifty pe')
except:
    pass
#####################################
try:
     modify_order(ne_ce1,'MARKET',0,nce,ncet,75*n_lot)# exit at 3.10 pm
    print('nifty ce exit')   
except:
    pass
try:
    modify_order(ne_pe1,'MARKET',0,npe,npet,75*n_lot)# exit at 3.10 pm
    print('nifty pe exit')
except:
    pass
#cancel_order('NORMAL','210121000285699')
#obj.cancelOrder('210121000285699','NORMAL')
#########################################
print('day trading done')    
