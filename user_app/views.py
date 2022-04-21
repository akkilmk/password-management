
from ast import Pass, Return
from urllib import request
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import RegisterSerializer, ManagePassword, SharingDetailsSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class SignUP(APIView):
    def get(self, request):
        queryset = User.objects.filter(id = request.GET["id"])
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteRegistration(APIView):

    def get(self, request, format=None):
        try:
            user_id = request.GET['user_id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        credentials = PassManager.objects.filter(user_id=user_id)
        serial_cred = ManagePassword(credentials, many=True)
        return Response(serial_cred.data, status=status.HTTP_200_OK)

    def post(self, request):
        site_datas = ManagePassword(data=request.data)
        if site_datas.is_valid():
            site_datas.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(site_datas.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data['id']
        password = request.data['password']
        user_id = request.data['user_id']

        if PassManager.objects.filter(id=id, user_id=user_id).exists():
            item_id = PassManager.objects.get(id=id, user_id=user_id)
        
            
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result = check_password(password, item_id.password)
        if result:
            pssw = make_password(request.data['new_password'])
            item_id.password = pssw
            item_id.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.GET['id']
        user_id = request.GET['user_id']
        try:
            PassManager.objects.filter(id=id, user_id=user_id).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Permission(APIView):
    def post(self, request):

        print(request.data["receiver"])

        send = User.objects.get(pk=request.data["sender"])
        SharingDetails.objects.create(
            sender=send,
            receiver=request.data["receiver"]
        )
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        permission_id = request.data["id"]
        permission = SharingDetails.objects.get(id=permission_id)
        permission.edit_access = not(permission.edit_access)
        permission.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        sender = request.GET['sender']
        sen = User.objects.get(id=sender)
        value = SharingDetails.objects.filter(sender=sen)
        serializer = SharingDetailsSerializer(value, many=True)
        return Response(serializer.data)

class SharingDetail(APIView):

    def get(self, request):
        receiver = request.GET['receiver']
        value = SharingDetails.objects.filter(receiver=receiver)

        access_false = []
        access_true = []

        for i in value:
            if i.edit_access == True:
                access_true.append(i.sender)
                continue
            access_false.append(i.sender)

        combined = []

        AccessTrue = PassManager.objects.filter(
            user_id__in = access_true).select_related(
                "user_id").values("user_id__id", "id","site_name", "password" )

        AccessFalse = PassManager.objects.filter(
            user_id__in = access_false).select_related(
                "user_id").values("user_id__id", "id","site_name", "password" )

        combined.append({"true": AccessTrue})
        combined.append({"false": AccessFalse})

        return Response(list(combined))

    def put(self, request):
        id = request.data['id']
        sender = request.data['sender']
        receiver = request.data['receiver']
        password = request.data['password']
        new_password = request.data['new_password']
    
        if SharingDetails.objects.filter(
            sender = sender, receiver = receiver, edit_access = True
            ).exists() and PassManager.objects.filter(
            id = id, user_id__id = sender).exists():

            item_id = PassManager.objects.get(id = id)
            result = check_password(password, item_id.password)

            if result:
                pssw = make_password(new_password)
                item_id.password = pssw
                item_id.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)





