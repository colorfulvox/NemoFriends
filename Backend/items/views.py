from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import User_Decoration, Decoration
from .serializers import ItemsUpdateSerializer, ItemsCreateSerializer
from utils import *


# 조경 생성 테스트용
class ItemsCreateView(APIView):
    def post(self, request):
        serializer = ItemsCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class ItemsUpdateView(APIView):
    def put(self, request):
        user_decoration = get_object_or_404(User_Decoration, id=request.data.get("id"))

        # 요청 보낸 사용자와 로그인 사용자 동일 여부 확인
        if request.user != user_decoration.user:
            response = FAIL
            response.update({"message": "요청을 보낸 사용자와 로그인한 사용자가 다릅니다."})
            return Response(response)

        serializer = ItemsUpdateSerializer(instance=user_decoration, data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(SUCCESS)


class ItemsBuyView(APIView):
    def post(self, request):
        decoration = get_object_or_404(Decoration, id=request.data.get("id"))
        user = request.user

        # 희귀 조경 확인
        if decoration.is_rare:
            response = FAIL
            response.update({"message": "희귀 조경은 구매할 수 없습니다."})
            return Response(response)
        
        # 보유 골드 확인
        if user.gold < decoration.cost:
            response = FAIL
            response.update({"message": "보유한 골드가 부족합니다."})
            return Response(response)

        user_decoration = User_Decoration(user=user, decoration=decoration, is_located=False, location=-1, angle=-1)
        user_decoration.save()

        user.gold -= decoration.cost
        user.save()

        response = SUCCESS
        response.update({"id": user_decoration.id})

        return Response(response, status=status.HTTP_201_CREATED)