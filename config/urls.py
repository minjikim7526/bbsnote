"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from bbsnote import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bbsnote/', include('bbsnote.urls')), # 주소가 127.~~~/bbsnote이면 views.py의 index가 나오도록 설정함
    path('common/', include('common.urls')),
    path('', views.index,name='index'), # 주소창에 아무것도 없어도 오류창 안 뜨고 bbsnote처럼 나오게 설정한 것
    
]
