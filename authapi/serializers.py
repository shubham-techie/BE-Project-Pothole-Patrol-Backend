from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']

    def create(self, validated_data):
        print('creating a user!')
        number=validated_data.pop('number',None)
        code=validated_data.pop('country_code',None)

        print('Popped number and country_code from the validated data',number,code)

        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        number=validated_data.pop('number',None)
        code=validated_data.pop('country_code',None)

        print('Popped number and country_code from the validated data',number,code)

        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token
    

