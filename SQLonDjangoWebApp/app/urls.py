from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('addEntry/', views.addEntry),
    path('deleteAll/', views.deleteAll),
    path('getSearch/', views.getSearch),
]
