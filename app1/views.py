from typing import List
from django.db.models.deletion import SET_NULL
from django.db.models.query import QuerySet, RawQuerySet
from django.http import response
from django.http.request import QueryDict
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from requests.models import Request
from .models import *
from django.contrib import messages
import requests
import datetime
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import json
from decouple import config
# Create your views here.




def index(request):
    request.session['id']=0
    return render(request, 'index.html')


def login(request):
    request.session['id']=0
    return render(request, 'login.html')


def register(request):
    request.session['id']=0
    return render(request, 'register.html')


def create(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    x=request.POST
    hashedpassword= bcrypt.hashpw(x['pw'].encode(), bcrypt.gensalt(rounds=10)).decode()
    newUser=User.objects.create(first_name=x['fname'], last_name=x['lname'], email= x['email'],  password= hashedpassword)
    request.session['id']=newUser.id
    return redirect('/homepage')


def validate(request):
    x=request.POST
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    user= User.objects.filter(email=x['email'])
    request.session['id']=user[0].id
    return redirect('/homepage')


def homepage(request):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    stockhist=(StockHistory.objects.filter(user_id=x))
    
    hist=serialize('python',stockhist)
    
    context ={
        'loggedin': user,
        "hist":hist
    }
    return render(request, 'homepage.html', context)


def logout(request):
    request.session['id']=0
    return redirect('/')


def editAccount(request):
    if request.session['id']==0:
        return redirect('/login')
    x= request.session['id']
    context ={
        'loggedin': User.objects.get(id=x)
    }
    return render(request, 'editAccount.html', context)


def addStockStats(request):
    x= request.session['id']
    context ={
        'loggedin': User.objects.get(id=x)
    }
    return render(request,'stockTrackerForm.html', context)


def addtoVault(request):
    return render(request, 'addVault.html')


def comparetoVault(request):
    return render(request, 'comparetoVault.html')


def performance(request):
    x= request.session['id']
    current_user=User.objects.get(id=x)
    context={
        'statHistory':current_user.stockHistory
    }
    return render(request, 'performance.html', context)


def submitToVault(request):
    errors = stockVault.objects.addToVault(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtovault')
    y=request.POST
    stock=y['stock_ticker'] 
    stockInfo=PullStockInfo(stock)
    
    content={
        "stock": stock,
        "overview":stockInfo.overview,
        "daily":stockInfo.daily
    }
    return redirect('/addtovault')


def addToHistory(request):
    print(request.POST)
    errors = StockHistory.objects.validateForm(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/stocktrackerform')
    y=request.POST
    x= request.session['id']
    current_user=User.objects.get(id=x)
    StockHistory.objects.create(ticker=y['stock_ticker'], entry=y['entry'], exit=y['exit'], position_size=y['position_size'], trade_pattern=y['pattern'], dateOfTrade=y['date'], sector=y['sector'],desc=y['desc'], buy_or_short=y['trade_type'], user= current_user)
    return redirect('/homepage')


def displayStock(request):
    y=request.GET
    type=y['asset']
    print(type)
    if type=="stock":
        
        stock=y['stock_ticker'] 
        stockInfo=PullStockInfo(stock)
        password=config('Alpha')
        content={
            "stock": stock,
            "overview":stockInfo['overview'],
            "password": password
        }
        
        return render(request, 'displayStock.html', content)
    elif type == "crypto":
        crypto=y['stock_ticker'] 
        cryptoInfo=PullCryptoInfo(crypto)
        cryptoChart=PullCryptoChart(crypto)
        content={
            "crypto": crypto,
            "overview":cryptoInfo,
            "chartData":cryptoChart
        }
        return render(request, 'displayCrypto.html', content)
    else:
        return redirect('/homepage')


def AddVaultIntraday(request, stock):
    stockInfo=PullStockInfo(stock);
    password=config('Twelve_Data')
    y=stock
    quote=requests.request("GET",f"https://api.twelvedata.com/quote?apikey={password}&symbol={stock}").json
    dayChart=getIntradayChart(stock)
    stockVault.object.create(ticker=stockInfo['symbol'],sector=stockInfo['sector'], industry=stockInfo['industry'], exchange=stockInfo['exchange'], open=quote[y]['open'], high=quote[y]['high'], low=quote[y]['low'], close=quote[y]['close'], previous_close=quote[y]['previous_close'], volume=quote[y]['volume'], year_high=stockInfo['52WeekHigh'],year_low=stockInfo['52WeekLow'],float=stockInfo['SharesFloat'], market_cap=stockInfo['SharesOutstanding'], daychart=dayChart)


def AddVaultDaily(request, stock):
    stockInfo=PullStockInfo(stock);
    password=config('Twelve_Data')
    y=stock
    quote=requests.request("GET",f"https://api.twelvedata.com/quote?apikey={password}&symbol={stock}").json
    dayChart=getDailyChart(stock)
    stockVault.object.create(ticker=stockInfo['symbol'],sector=stockInfo['sector'], industry=stockInfo['industry'], exchange=stockInfo['exchange'], open=quote[y]['open'], high=quote[y]['high'], low=quote[y]['low'], close=quote[y]['close'], previous_close=quote[y]['previous_close'], volume=quote[y]['volume'], year_high=stockInfo['52WeekHigh'],year_low=stockInfo['52WeekLow'],float=stockInfo['SharesFloat'], market_cap=stockInfo['SharesOutstanding'],daychart=dayChart)

def PullCryptoChart(name):
    crypto=name+"usd"
    quote= requests.request("GET",f"https://api.gemini.com/v2/candles/{crypto}/15m")
    return quote.json()


def PullCryptoInfo(name):
    crypto=name+ "usd"
    print(crypto)
    quote=requests.request("GET",f"https://api.gemini.com/v2/ticker/{crypto}")
    return quote.json()

def PullStockInfo(stock):
    password=config('Alpha')
    overview=requests.request("GET",f"https://www.alphavantage.co/query?symbol={stock}&apikey={password}&function=OVERVIEW")
    context={
        "overview":overview.json()
    }
    return context


def PullStockQuote(stock):
    password=config('Alpha')
    quote=requests.request("GET",f"https://www.alphavantage.co/query?symbol={stock}&function=GLOBAL_QUOTE&apikey={password}")
    return quote.json()


def getIntradayChart(stock):
    password=config('Twelve_Data')
    result=requests.request('GET', f"https://api.twelvedata.com/time_series?apikey={password}&interval=5min&outputsize=78&symbol={stock}")
    values=result['values']
    return values;


def getDailyChart(stock):
    password=config('Twelve_Data')
    result=requests.request('GET', f"https://api.twelvedata.com/time_series?apikey={password}&interval=1day&outputsize=252&symbol={stock}")
    values=result['values']
    return values;

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            print("****************************")
            print("The type of the object is a QuerySet")
            return str(obj)
        return super().default(obj)


def dayrecap(request, date):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    stockhist=(StockHistory.objects.filter(user_id=x, dateOfTrade=date ))
    
    try:
        watchlist= Watchlist.objects.get(user=user, date=date)
    except:
        watchlist="undefined"
    hist=serialize('python',stockhist)
    
    context={
        'date':date,
        'daysHist':hist,
        "watchlist":watchlist
    }
    return render(request, "dayrecap.html", context)


def editTrade(request, y):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    stockhist=(StockHistory.objects.filter(id=y ))
    hist=serialize('python',stockhist)

    context={
        'date':date,
        'trade':hist[0],
        "id": y
    }
    return render(request, "editTrade.html", context)


def updateTrade(request, z):
    errors = StockHistory.objects.validateForm(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trade/{z}/edit')
    y=request.POST
    trade=StockHistory.objects.get(id=z)
    trade.ticker=y['stock_ticker']
    trade.entry=y['entry']
    trade.exit=y['exit']
    trade.position_size=y['position_size']
    trade.trade_pattern=y['pattern']
    trade.dateOfTrade=y['date']
    trade.sector=y['sector']
    trade.desc=y['desc']
    trade.buy_or_short=y['trade_type']
    trade.save()
    return redirect('/homepage')


def deleteTrade(request, z):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    trade=StockHistory.objects.get(id=z)
    # tradeS=serialize('python',trade)
    if(trade.user!=user):
        redirect('/homepage')
    trade.delete()
    return redirect('/homepage')


def watchlist(request):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    watchlist= Watchlist.objects.filter(user=user)
    
    context={
        "watchlist":watchlist
    }
    return render(request, 'watchlist.html', context)


def addWatchlist(request):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    y=request.POST
    watchlist=Watchlist.objects.create(name=y['name'], user=user, date=y['date'])
    id=watchlist.id
    return redirect(f'/watchlist/{id}/add')


def addToWatchlist(request, y):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    watchlist=Watchlist.objects.get(id=y)
    watchlists=Watchlist.objects.filter(user=user)
    print("***************")
    
    
    print(x)
    context={
        "watchlist":watchlist,
        "id":y,
        "watchlists":watchlists
    }
    return render(request, "addToWatchlist.html", context)


def addStockToWatchlist(request,z):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    y=request.POST
    user=User.objects.get(id=x)
    watchlists=Watchlist.objects.get(id=z)
    StockWatchlist.objects.create(ticker=y['ticker'], category=y['category'], catalyst=y['catalyst'], desc=y['desc'], watchlist=watchlists )
    return redirect(f'/watchlist/{z}/add')


def newWatchlist(request):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    return render(request, "newWatchlist.html")


def viewWatchlist(request,y):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    watchlist=Watchlist.objects.get(id=y)
    watchlists=Watchlist.objects.filter(user=user)
    print("***************")
    
    
    print(x)
    context={
        "watchlist":watchlist,
        "id":y,
        "watchlists":watchlists
    }
    return render(request, "viewWatchlist.html", context)


def deleteStockFromWatchlist(request,x, y):
    stock=StockWatchlist.objects.get(id=y)
    stock.delete()
    return redirect(f"/watchlist/{x}/add") 


def editWatchlist(request, y):
    if request.session['id']==0 or request.session['id']==None:
            return redirect('/login')
    z= request.session['id']
    user=User.objects.get(id=z)
    watchlist= Watchlist.objects.get(id=y)
    
    context={
        "watchlist":watchlist
    }
    return render(request, "editWatchlist.html", context)

def updateWatchlist(request,z):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    user=User.objects.get(id=x)
    y=request.POST
    watchlist=Watchlist.objects.get(id=z)
    watchlist.name=y['name'] 
    watchlist.date=y['date']
    watchlist.save()
    id=watchlist.id
    return redirect(f'/watchlist/{id}/add')

