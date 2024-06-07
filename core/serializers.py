from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User

class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(UserLoginSerializer, self).validate(attrs)
        # Custom data to include
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        data.update({'is_superuser': self.user.is_superuser})
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password",'is_superuser','is_active', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True},}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'],password=validated_data['password'],
                                       is_active = validated_data['is_active'], first_name = validated_data['first_name'], last_name = validated_data['last_name'] )
                                        
        user.set_password(validated_data['password'])
        user.save()
        return user  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )
