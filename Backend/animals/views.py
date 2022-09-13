from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal, User_Animal
from .serializers import AnimalsRenameSerializer, AnimalsTestSerializer
from animals import serializers
from items.models import User_Color
from utils import *

import random
from datetime import datetime, timedelta


class AnimalsEatView(APIView):
    def put(self, request):
        id = request.data.get('id')
        result = request.data.get('result')
        user_animal = get_object_or_404(User_Animal, pk=id)

        last_time = user_animal.last_eating_time.replace(tzinfo=None)
        now = datetime.now()
        delta = timedelta(hours=4)
        possible_time = last_time + delta
 
        # 먹이 쿨타임 No
        if now < possible_time:
            response = FAIL
            response['reason'] = '배가 불러서 더 못먹겠어요.'
            return Response(response)
        # 먹이 쿨타임 Ok 
        feeds = user_animal.animal.feeds[-1]  # feeds : 전체 먹이 정보

        # 먹이 섭취 Yes
        if result in feeds:
            print('먹을 수 있따!!')
            user_animal.exp += 100  # 호감도 증가
            user_animal.user.gold += 100  # 골드 증가
            user_animal.last_eating_time = now  # 쿨타임 갱신
            user_animal.save()
            response = SUCCESS
            response['last_eating_time'] = user_animal.last_eating_time
            print('후',user_animal.user.gold)
            return Response(response)
        # 먹이 섭취 No
        response = FAIL
        response['recommend'] = random.choice(feeds)
        response['feeds'] = feeds
        return Response(FAIL)


class AnimalsRenameView(APIView):
    def put(self, request):
        id = request.data.get('id')
        user_animal = get_object_or_404(User_Animal, pk=id)

        if request.user == user_animal.user:
            serializer = AnimalsRenameSerializer(instance=user_animal, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(SUCCESS)
        # 로그인 안되있어서 request.user가 AnoymousUser로 나옴
        else:
            response = FAIL
            response['reason'] = '유저의 정보가 일치하지 않습니다.'
            return Response(response)


# 염색약이 남아있는 지 확인 -> -1하고 돌려준다.
class AnimalsColorView(APIView):
    def put(self, request):
        user_animal_id = request.data.get('user_animal_id')
        user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
        
        user_color_id = request.data.get('user_color_id')
        user_color = get_object_or_404(User_Color, pk=user_color_id)

        if 1 <= user_color.cnt:
            user_color.cnt -= 1
            user_color.save()
            user_animal.color_id = user_color_id
            user_animal.save()
            return Response(SUCCESS)

        response = FAIL
        response['reason'] = '염색약이 부족합니다.'
        return Response(response)


class AnimalsTalkView(APIView):
    def put(self, request):
        pass

# class AnimalsPlayNewGame(APIView):
#     def put(self, request):
#         pass

# class AnimalsPlayWordChainView(APIView):
#     def put(self, request):
#         pass


# class AnimalsTestView(APIView):
#     def get(self, request, animal_id, order_id):
#         print(request)
#         print(order_id, type(order_id))
#         animals = get_list_or_404(Animal)
#         animal = get_object_or_404(Animal, id=animal_id)
#         print(animals)
#         # serializer = AnimalsTestSerializer(animals, many=True)
#         serializer = AnimalsTestSerializer(animal)
#         print(animal)
#         space = animal.species
#         feed = animal.feeds
#         character = animal.characteristics
#         commands = animal.commands
#         print(f'space: {space}\ncharacter: {character}\ncommands: {commands}\nfeed: {feed}')
#         # print('명령', commands[str(order_id)])
#         print(commands.keys())
#         print('먹이', type(feed[order_id]), feed[order_id])
#         return Response(serializer.data)