
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

import jwt
import datetime

# Create your views here.

class registerAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   #if anything not valid, raise exception
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        #find user using email
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found:)')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

       
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        # token.decode('utf-8')
        #we set token via cookies
        

        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)  #httonly - frontend can't access cookie, only for backend

        response.data = {
            'jwt token': token
        }

        #if password correct
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
            #decode gets the user

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
        #cookies accessed if preserved

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successful'
        }

        return response
    
class CreateUserView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    
class CreateTokenView(ObtainAuthToken):
    
    serializer_class = AuthTokenSerializer
    rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES
