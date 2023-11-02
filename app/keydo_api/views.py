
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from keydo_api.serializers import AddKeystrokeSerializer

class AddKeystrokesView(APIView):
    
    def post(self, request):
        # if 'key_code' not in request.data:
        #     return Response({'msg': 'Required Fields missing'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        
        serializer = AddKeystrokeSerializer(data=data, many=True)
        
        if serializer.is_valid():
            keystrokes = serializer.save()
            # auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
