from django.urls import path,include
from keydo_api import views

app_name = 'keydo_api'

urlpatterns = [
    path('add/', views.AddKeystrokesView.as_view(), name='create'),
    # path('list/', )
]
