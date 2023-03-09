"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from app.views import addProcess, cal_fcfs, cal_rr, deleteAll, deleteProcess, totalProcess, cal_sjf, cal_srtf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('addProcess/', addProcess),
    path('deleteProcess/<int:proid>/', deleteProcess),
    path('deleteAll/', deleteAll),
    path('cal_fcfs/', cal_fcfs),
    path('cal_sjf/', cal_sjf),
    path('cal_srtf/', cal_srtf),
    path('totalProcess/', totalProcess),
    # path('addTQ/', addTQ),
    path('cal_rr/', cal_rr),
    
]
