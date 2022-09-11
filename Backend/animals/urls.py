from django.urls import path
from . import views

urlpatterns = [
    path('test/<int:animal_id>/<int:order_id>/', views.AnimalsTestView.as_view()),
    path('eat/', views.AnimalsEatView.as_view()),
]
