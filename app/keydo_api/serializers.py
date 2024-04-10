
from core.models import UserKeystrokes
from django.utils.translation import gettext as _
from rest_framework import serializers

class KeystrokeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserKeystrokes
        fields = ('key_code', 'event', 'timestamp', 'user')
        
