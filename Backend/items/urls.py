from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.ItemsBuyView.as_view(), name='buy'),
    path('place/', views.ItemsPlaceView.as_view(), name='place'),
    path('update/', views.ItemsUpdateView.as_view(), name='update'),
    path('cancel/', views.ItemsCancelView.as_view(), name='cancel'),
]