
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
class CreateUserView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    

class CreateTokenView(ObtainAuthToken):
    
    serializer_class = AuthTokenSerializer
    rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class LoginView(APIView):
    
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
