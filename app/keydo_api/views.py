
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.models import UserKeystrokes
from keydo_api.serializers import KeystrokeSerializer

import jwt

class KeystrokesView(APIView):
    
    def post(self, request):
        # if 'key_code' not in request.data:
        #     return Response({'msg': 'Required Fields missing'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        
        serializer = KeystrokeSerializer(data=data, many=True)
        
        if serializer.is_valid():
            keystrokes = serializer.save()
            # auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ListKeystrokesView(APIView):    
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
        keystrokes = UserKeystrokes.objects.filter(user=user)
        serializer = KeystrokeSerializer(keystrokes, many=True)
        return Response(serializer.data)
