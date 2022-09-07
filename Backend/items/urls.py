from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
    path('create/', views.ItemsCreateView.as_view(), name='create'),
    path('update/', views.ItemsUpdateView.as_view(), name='update'),
    path('buy/', views.ItemsBuyView.as_view(), name='buy'),
]