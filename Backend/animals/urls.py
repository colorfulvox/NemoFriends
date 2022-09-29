from django.urls import path
from . import views

urlpatterns = [
    path('eat/', views.AnimalsEatView.as_view()),
    path('rename/', views.AnimalsRenameView.as_view()),
    path('talk/', views.AnimalsTalkView.as_view()),
    path('place/', views.AnimalsPlaceView.as_view()),
    path('expup/', views.AnimalsExpUpView.as_view()),
    path('play/maze/', views.AnimalsMazeView.as_view()),
    path('play/wordchain/start/', views.AnimalsPlayWordchainStartView.as_view()),
    path('play/wordchain/next/', views.AnimalsPlayWordchainNextView.as_view()),
    path('play/wordchain/finish/', views.AnimalsPlayWordchainFinishView.as_view()),
]
