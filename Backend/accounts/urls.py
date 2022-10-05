"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from . import views
from .serializers import MyTokenRefreshView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('', include('allauth.urls')),
    path('refresh/', MyTokenRefreshView.as_view(), name='refresh_token'),
    path('sound/', views.ChangeSoundView.as_view(), name='change_bgm'),
    path('delete/', views.UserDeleteView.as_view(), name='account_delete'),
    path('gacha/', views.GachaView.as_view(), name='gacha'),
    path('start/', views.StartAnimalView.as_view(), name='start_animal'),
    path('question/', views.QuestionView.as_view(), name='get_question'),
    path('loadgame/',views.LoadGameView.as_view(), name='load_game')
]
 