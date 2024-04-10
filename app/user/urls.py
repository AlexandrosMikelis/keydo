from django.urls import path,include
from .views import *

app_name = 'user'

urlpatterns = [
    path('register/', registerAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('keystrokes/', include('keydo_api.urls')),
]
