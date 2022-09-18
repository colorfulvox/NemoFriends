from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ItemsCreateView.as_view(), name='create'),
    path('update/', views.ItemsUpdateView.as_view(), name='update'),
    path('buy/', views.ItemsBuyView.as_view(), name='buy'),
]