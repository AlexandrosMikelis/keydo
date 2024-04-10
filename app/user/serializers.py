
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # hash passwords in the database, override default create function
    def create(self, validated_data):
        #extract password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) #doesnt include password

        if password is not None:
            instance.set_password(password) #hashes password
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_user(self, validated_data):
        user = authenticate(username=validated_data['email'], password=validated_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user

class AuthTokenSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )
    
    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password=password,
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs