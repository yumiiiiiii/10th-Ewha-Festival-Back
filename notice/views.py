from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from rest_framework.status import *
from .models import *
from .serializers import *

# Create your views here.

class NoticeView(views.APIView):
    serializer_class = NoticeSerializer

    def post(self, request):
        serializer=NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'TF 공지 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': 'TF 공지 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)