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
from time import strftime, strptime


class AnimalsEatView(APIView):
    def put(self, request):
        id = request.data.get('id')
        result = request.data.get('result')
        user_animal = get_object_or_404(User_Animal, pk=id)

        # request.user == user_animal.user 체크 필요
        last_time = user_animal.last_eating_time
        possible_time = last_time + timedelta(hours=4)
        now = datetime.now()
        response = {'last_eating_time' : last_time.strftime(date_format_slash)}
 
        # 먹이 쿨타임 No
        if now < possible_time:
            response.update(FAIL)
            return Response(response)

        # 먹이 쿨타임 Ok 
        feeds = user_animal.animal.feeds[-1]  # feeds : 전체 먹이 정보

        # 먹이 섭취 Ok
        if result in feeds:
            user_animal.exp += 100
            user_animal.last_eating_time = now
            user_animal.level = level_up(user_animal.exp, user_animal.level)
            user_animal.save()  # 동물 정보 업데이트(호감도, 쿨타임)
            user_animal.user.gold += 100
            user_animal.user.save()  # 유저 정보 업데이트(골드)
            response['last_eating_time'] = now.strftime(date_format_slash)
            response.update(SUCCESS)
            return Response(response)

        # 먹이 섭취 No
        response.update(FAIL)
        # response['recommend'] = random.choice(feeds)
        return Response(response)


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
            return Response(FAIL)


class AnimalsColorView(APIView):
    def put(self, request):
        user_animal_id = request.data.get('user_animal_id')
        user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
        user_color_id = request.data.get('user_color_id')
        user_color = get_object_or_404(User_Color, pk=user_color_id)

        # request.user == user_animal.user 체크 필요
        # 염색 Ok
        if 1 <= user_color.cnt:
            # user_animal 정보
            user_animal.color_id = user_color_id
            user_animal.save()
            # user_color 정보
            user_color.cnt -= 1
            user_color.save()
            return Response(SUCCESS)
        # 염색 No
        return Response(FAIL)


class AnimalsTalkView(APIView):
    def recognize(data):
        return data

    def put(self, request):
        user_animal_id = request.data.get('id')
        user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
        
        # request.user == user_animal.user 체크 필요
        result = self.recognize(request.data.get('voice'))
        level = user_animal.level
        commands = user_animal.animal.commands[:level+1]
        if result in commands:
            user_animal.playing_cnt += 1
            user_animal.exp += 100
            user_animal.level = level_up(user_animal.exp, user_animal.level)
            user_animal.save()
            user_animal.user.gold += 100
            user
            return Response(SUCCESS)
        return Response(FAIL)


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