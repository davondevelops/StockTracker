from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register',views.register),
    path('register/create', views.create),
    path('login/validate', views.validate),
    path('homepage', views.homepage),
    path('logout', views.logout),
    path('stocktrackerform', views.addStockStats),
    path('addtovault', views.addtoVault),
    path('comparetovault', views.comparetoVault),
    path('performance', views.performance),
    path('addtovault/submit', views.submitToVault),
    path('addToHistory', views.addToHistory),
    path('displayStock/',views.displayStock),
    path('addtovault/intraday/submit/:stock', views.AddVaultIntraday),
    path('addtovault/daily/submit/:stock', views.AddVaultDaily),
    path('dayrecap/<str:date>', views.dayrecap),
    path('trade/<int:y>/edit', views.editTrade),
    path('trade/<int:z>/update', views.updateTrade),
    path('trade/<int:z>/delete',views.deleteTrade),
    path('watchlists',views.watchlist),
    path('watchlist/add',views.newWatchlist),
    path('watchlist/<int:y>/add', views.addToWatchlist),
    path('watchlist/<int:z>/add/stock', views.addStockToWatchlist),
    path('watchlist/new', views.addWatchlist),
    path('watchlist/<int:y>', views.viewWatchlist),
    path('watchlist/<int:x>/stock/<int:y>/delete', views.deleteStockFromWatchlist),
    path('watchlist/<int:y>/edit', views.editWatchlist),
    path('watchlist/<int:z>/update', views.updateWatchlist),
]