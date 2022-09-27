from re import S
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import User_Decoration, Decoration
from .serializers import ItemsPlaceSerializer
from utils import *
import logging

logger = logging.getLogger(__name__)

class ItemsBuyView(APIView):
    def post(self, request):
        user = request.user
        decoration = get_object_or_404(Decoration, id=request.data.get("id"))

        # 희귀 조경 확인
        if decoration.is_rare:
            response = FAIL.copy()
            response.update({"message": "희귀 조경은 구매할 수 없습니다."})
            return Response(response)
        
        # 보유 골드 확인
        if user.gold < decoration.cost:
            response = FAIL.copy()
            response.update({"message": "보유한 골드가 부족합니다."})
            return Response(response)

        user_decoration = User_Decoration(user=user, decoration=decoration, is_located=False, location=-1, angle=-1)
        user_decoration.save()

        user.gold -= decoration.cost
        user.save()

        response = SUCCESS.copy()
        response.update({"id": user_decoration.id})

        return Response(response, status=status.HTTP_201_CREATED)


class ItemsPlaceView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        decoration = get_object_or_404(Decoration, id=data.get("id"))
        user_decoration_lst = User_Decoration.objects.filter(user=user, decoration=decoration).exclude(is_located=True)

        # 배치 가능한 조경 있는지 확인
        if len(user_decoration_lst) < 1:
            response = FAIL.copy()
            response.update({"message": "배치 가능한 조경이 없습니다."})
            return Response(response)

        user_decoration = user_decoration_lst[0]
        user_decoration.is_located = True
        serializer = ItemsPlaceSerializer(instance=user_decoration, data=data)

        location = int(data["location"])
        angle = int(data["angle"])

        if serializer.is_valid(raise_exception=True):
            # location, angle 값 확인
            location_lst = [user_decoration.location for user_decoration in User_Decoration.objects.filter(user=user).exclude(is_located=False)]

            if not (1 <= location <= 100 and location not in location_lst and 1 <= angle <= 4):
                response = FAIL.copy()
                response.update({"message": "입력값이 잘못되었습니다."})
                return Response(response)

            response = SUCCESS.copy()
            serializer.save()
            response.update({"id": user_decoration.id})
            return Response(response)


class ItemsUpdateView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        user_decoration = get_object_or_404(User_Decoration, id=data.get("id"))

        # 사용자 동일 여부 확인
        if user != user_decoration.user:
            response = FAIL.copy()
            response.update({"message": "요청을 보낸 사용자와 해당 조경을 보유한 사용자가 다릅니다."})
            return Response(response)

        serializer = ItemsPlaceSerializer(instance=user_decoration, data=data)

        location = int(data["location"])
        angle = int(data["angle"])
        
        if serializer.is_valid(raise_exception=True):
            # # location, angle 값 확인
            # location_lst = [user_decoration.location for user_decoration in User_Decoration.objects.filter(user=user).exclude(is_located=False)]

            # if (location != user_decoration.location and not (1 <= location <= 100 and location not in location_lst)) \
            #     or not 1 <= angle <= 4:
            #         response = FAIL.copy()
            #         response.update({"message": "입력값이 잘못되었습니다."})
            #         return Response(response)

            serializer.save()
            return Response(SUCCESS)


class ItemsCancelView(APIView):
    def post(self, request):
        user_decoration = get_object_or_404(User_Decoration, id=request.data.get("id"))

        # 사용자 동일 여부 확인
        if request.user != user_decoration.user:
            response = FAIL.copy()
            response.update({"message": "요청을 보낸 사용자와 해당 조경을 보유한 사용자가 다릅니다."})
            return Response(response)

        user_decoration.is_located = False
        user_decoration.save()
        return Response(SUCCESS)
