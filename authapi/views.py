import os
import base64

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status,serializers
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import pyotp
from datetime import datetime

from .models import MobileNumber
from .serializers import UserSerializer,MyTokenObtainPairSerializer


@api_view(['GET'])
def apiOverview(request):

    api_urls = {
        'generateOTP/':'generate OTP for a number',
        'verifyOTP/':'verify OTP for a number',
        'registerUser/': 'register user',
        'token/':'login user',
        'token/refresh/':'refresh JWT token',
        'protected/':'A dummy auth only protected route just for testing JWT tokens'
        }
        
    return Response(api_urls)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dummyProtectedView(request):
    return Response('This is a dummy protected view')


@api_view(['POST'])
def generateOTPForNumber(request):
    print(request.data)

    try:
        num=request.data['number']
        code=request.data['country_code']
    except KeyError:
        return Response({"error": "required field/s is missing"}, status=status.HTTP_400_BAD_REQUEST)

    print(f'Generating OTP for ${num}..')

    if(not MobileNumber.objects.filter(number=num,country_code=code).exists()):
        MobileNumber.objects.create(number=num,country_code=code)

    user_number=MobileNumber.objects.get(number=num,country_code=code)
    user_number.counter+=1
    user_number.save()

    key=base64.b32encode(generateOTPKey(str(code)+str(num)).encode())
    print(key)
    hotp=pyotp.HOTP(key,digits=4)
    print(hotp.at(user_number.counter))

    return Response({"otp": hotp.at(user_number.counter)}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verifyOTP(request):
    print(request.data)

    try:
        num=request.data['number']
        code=request.data['country_code']
        otp=request.data['otp']
    except KeyError:
        return Response({"error":"some field is missing"}, status=status.HTTP_400_BAD_REQUEST)

    print(f'Verifying OTP for +${code} ${num}')
    print(f'Sent OTP ${otp}')

    try:
        user_number=MobileNumber.objects.get(number=num,country_code=code)
    except ObjectDoesNotExist:
        return Response({"error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    key=base64.b32encode(generateOTPKey(str(code)+str(num)).encode())
    hotp=pyotp.HOTP(key,digits=4)

    if hotp.verify(otp, user_number.counter):
        user_number.is_verified = True
        user_number.save()
        return Response({"message":"You are authorised!"}, status=status.HTTP_200_OK)

    return Response({"error":"OTP is wrong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerUser(request):
    print(request.data)

    try:
        num=request.data['number']
        code=request.data['country_code']
    except KeyError:
        return Response({"error":"number/country_code field is missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer=UserSerializer(data=request.data)

    try:
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
    except serializers.ValidationError as e:
        print(e)
        return Response({"error":"a user with same username already exists / provided data is invalid"},status=status.HTTP_400_BAD_REQUEST)

    try:
        user_number=MobileNumber.objects.get(number=num,country_code=code)
        user_number.user=user
        user_number.save()
    except ObjectDoesNotExist:
        return Response({"error":"Number not registered!"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"success":"user created!"}, status=status.HTTP_201_CREATED)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


def generateOTPKey(phone):
    return phone + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success":"logout succesful!"}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error":"logout failed!"}, status=status.HTTP_400_BAD_REQUEST)