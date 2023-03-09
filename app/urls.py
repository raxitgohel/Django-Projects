
from django.urls import path
from . import views

urlpatterns =[
    path('', views.home),
    path('sim/', views.sim),
    path('algo/', views.algo),
    path('about/', views.about),
]