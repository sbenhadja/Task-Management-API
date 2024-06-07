from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import *

# Create your views here.

# Login
class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

# User Registeration
class UserRegisterView(APIView): 
    permission_classes = [AllowAny] 
    def post(self, request):
        data = request.data
        print(data)

        serializer = UserRegisterSerializer(data=data)  

        if not serializer.is_valid() :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
            
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
