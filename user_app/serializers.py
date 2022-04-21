from argon2 import hash_password
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=True)

    # r = serializers.PrimaryKeyRelatedField(
    #     many = True,
    #     read_only = True
    # )

    class Meta:
        model = User
        # fields = ('username','email','password')
        fields = "__all__"


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'])

        user.set_password(validated_data['password'])
        user.save()
        return user


class ManagePassword(serializers.ModelSerializer):



    class Meta:
        model = PassManager
        fields = "__all__"

    def create(self, validated_data):
    
        item = PassManager.objects.create(
            user_id = validated_data["user_id"],
            site_name = validated_data['site_name'],
        )
        item.password = make_password(validated_data['password'])
        item.save()

        return item
    
class SharingDetailsSerializer(serializers.ModelSerializer):
    u = RegisterSerializer(many=True, read_only=True)
    m = ManagePassword(many=True, read_only=True)


    class Meta:
        model = SharingDetails
        fields = "__all__"


