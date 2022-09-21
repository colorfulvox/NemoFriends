from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal, User_Animal
from .serializers import AnimalsRenameSerializer, AnimalsTestSerializer, UserAnimalSerializer
from animals import serializers
from items.models import User_Item
from utils import *

import random
from datetime import datetime, timedelta
from time import strftime, strptime


class DepthTestView(APIView):
    def get(self, request, id):
        user_animal = get_object_or_404(User_Animal, pk=id)
        serializers = UserAnimalSerializer(instance=user_animal)
        return Response(serializers.data)


class AnimalsEatView(APIView):
    def put(self, request):
        id = request.data.get('id')
        result = request.data.get('result')
        user_animal = get_object_or_404(User_Animal, pk=id)

        if request.user == user_animal.user:
            # 먹이 쿨타임
            last_time = user_animal.last_eating_time
            possible_time = last_time + timedelta(hours=4)
            now = datetime.now()
            response = {'last_eating_time' : last_time.strftime(date_format_slash)}

            # 쿨타임 No
            if now < possible_time:
                response.update(FAIL)
                return Response(response)

            # 쿨타임 Ok -> 먹이 판단
            feeds = user_animal.animal.feeds[-1]  # feeds : 전체 먹이 정보

            # 섭취 Ok
            if result in feeds:
                action = 'eatting'
                
                # 동물 정보 업데이트(호감도, 쿨타임)
                user_animal = reward_exp(animal=user_animal, user=request.user, action=action)
                user_animal.last_eating_time = now
                user_animal.save()
                
                # 유저 정보 업데이트(골드)
                user = reward_gold(user=request.user, action=action)
                user.save()  

                response['last_eating_time'] = now.strftime(date_format_slash)
                response.update(SUCCESS)
                return Response(response)

            # 섭취 No
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
        else:
            return Response(FAIL)


class AnimalsColorView(APIView):
    def put(self, request):
        response = FAIL.copy() # response: 실패 응답이 담길 dict 

        user_item_id = request.data.get('user_item_id')

        if user_item_id == 1:
            response["message"] = "경험치 물약을 보냈습니다."
            return Response(response)

        user_animal_id = request.data.get('user_animal_id')
        user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
        user_item = get_object_or_404(User_Item, pk=user_item_id)

        # 염색 Ok
        if request.user == user_animal.user == user_item.user:
            if 1 <= user_item.cnt:
                # user_animal 정보
                user_animal.color_id = user_item_id
                user_animal.save()
                # user_color 정보
                user_item.cnt -= 1
                user_item.save()
                return Response(SUCCESS)
        # 염색 No
            response["message"] = "보유한 염색약이 없습니다."
            return Response(response)

        response["message"] = "유저 정보가 다릅니다."
        return Response(response)


class AnimalsTalkView(APIView):
    def recognize(data):
        data = "노란아 앉아"
        return data

    def put(self, request):
        user_animal_id = request.data.get('id')
        print(user_animal_id)
        user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
        print(request.user)
        if request.user == user_animal.user:
            result = self.recognize(request.data.get('voice'))
            level = user_animal.level
            commands = user_animal.animal.commands[:level+1]
            print(request.user.animal_set.all())
            if result in commands:
                action = 'talking'
                user_animal.playing_cnt += 1
                user_animal = reward_exp(user_animal, request.user, action)
                user_animal.save()
                user = reward_gold(request.user, action)
                user.save()
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