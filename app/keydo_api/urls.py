from django.urls import path,include
from keydo_api import views

app_name = 'keydo_api'

urlpatterns = [
    path('add/', views.KeystrokesView.as_view(), name='create'),
    path('', views.ListKeystrokesView.as_view())
]
