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
    path('performance', views.performance)
    

]