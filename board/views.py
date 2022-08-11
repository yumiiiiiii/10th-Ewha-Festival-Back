from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from .models import *
from .serializers import *


class BoothListView(views.APIView):
    serializer_class = BoothSerializer

    def get(self, request):
        user = request.user
        
        day = request.GET.get('day')
        college = request.GET.get('college')

        params = {'day': day, 'college': college}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        booths = Booth.objects.filter(**arguments)
        if user:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked=True

        serializer = self.serializer_class(booths, many=True)

        return Response({'message': '부스 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)


class BoothDetailView(views.APIView):
    serializer_class = BoothSerializer

    def get(self, request, pk):
        user = request.user
        booth = get_object_or_404(Booth, pk=pk)

        if booth.like.filter(pk=user.id).exists():
            booth.is_liked=True

        serializer = self.serializer_class(booth)

        return Response({'message': '부스 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def patch(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=booth, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '부스 정보 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '부스 정보 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class MenuDetailView(views.APIView):
    serializer_class = MenuSerializer

    def get(self, request, pk):
        menus = Menu.objects.filter(booth=pk)
        serializer = self.serializer_class(menus, many=True)
            
        return Response({'message': '메뉴 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
