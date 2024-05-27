from django.conf import settings
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status , viewsets
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.models import UserKeystrokes
from keydo_api.serializers import KeystrokeSerializer
from keydo_api.services import KafkaPublisher, MessagePublisher

import jwt

message_publisher = MessagePublisher(client=KafkaPublisher())

class KeystrokeViewSet(viewsets.ModelViewSet):
    queryset = UserKeystrokes.objects.all()
    message_topic = settings.KAFKA_STREAM_TOPIC
    permission_classes = []
    
    def get_serializer_class(self):
        serializers = {
            # "list": MetricReadOnlySerializer,
            "create": KeystrokeSerializer,
            # "retrieve": MetricReadOnlySerializer,
            "bulk": KeystrokeSerializer,
            "add": KeystrokeSerializer,
        }
        return serializers.get(self.action)

    # def list(self, request):
    #     queryset = Metric.objects.all()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Metric.objects.all()
    #     metric = get_object_or_404(queryset, pk=pk)
    #     serializer = self.get_serializer(metric)
    #     return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data,
        )
        print(request.data)
        
        serializer = KeystrokeSerializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)
        # message_publisher = MessagePublisher(client=KafkaPublisher())
        message_publisher.publish(topic=self.message_topic, data=serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def add(self, request, pk=None):
        data = request.data
        
        serializer = KeystrokeSerializer(data=data, many=True)
        
        if serializer.is_valid():
            keystrokes = serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def bulk(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, many=True)
        
        print(request.data)

        serializer.is_valid(raise_exception=True)

        for data in serializer.data:
            message_publisher.publish(topic=self.message_topic, data=data)

        return Response(serializer.data)
    
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
