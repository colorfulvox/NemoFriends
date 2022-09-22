from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal, User_Animal
from .serializers import AnimalsRenameSerializer, AnimalsTestSerializer, UserAnimalSerializer
from .utils import *
from animals import serializers
from items.models import User_Item
from utils import SUCCESS, FAIL

import random
from datetime import datetime, timedelta
from time import strftime, strptime


class DepthTestView(APIView):
    def get(self, request, id):
        user_animal = get_object_or_404(User_Animal, pk=id)
        serializers = UserAnimalSerializer(instance=user_animal)
        return Response(serializers.data)


class AnimalsEatView(APIView):
    def post(self, request):
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
    def post(self, request):
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
    def post(self, request):
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
    # 전체 동물 대화
    def talk_to_all(self, context, user):
        for i in range(1, len(ALL_COMMANDS)):
            if ALL_COMMANDS[i] in context:
                if not user.is_called:
                    user = reward_gold(user, 'talking_all')
                    user.is_called = True
                    user.save()
                response = {'animal_id': -1, 'cmd': i}
                response.update(SUCCESS)
                return response
        return FAIL

    # 특정 동물 대화
    def talk_to_one(self, user_animal, user, context):
        action = 'talking_one'
        grade = user_animal.grade
        commands = user_animal.animal.commands[:grade+1]

        for i in range(1, len(commands)):
            if commands[i] in context:
                # 대화 보상 Ok
                if user_animal.talking_cnt:
                    user_animal = reward_exp(user_animal, user, action)
                    user_animal.talking_cnt -= 1
                    user_animal.save()
                    user = reward_gold(user, action)
                    user.save()
                # 대화 보상 No
                response = {'animal_id': user_animal.animal_id, 'cmd': i}
                response.update(SUCCESS)
                return response
        return FAIL

    def post(self, request):
        audio = request.data.get('voice')
        
        # multipart/form-data로 받은 file을 테스트를 위해 bytes로 변환한 후
        # bytes를 wav 파일로 저장

        # with open('media/copy.wav', mode='bx') as f:
            # f.write(audio.file.read())

        # 서버에 file 저장
        fs = FileSystemStorage()
        filename = fs.save(request.user.username +'.wav', audio)
        # filename = fs.save(request.user, audio)
        # filename = fs.save(audio.name, audio)

        # 로직        
        context = '꼬꼬 앉아'
        # file의 경로
        uploaded_file_path = fs.path(filename)

        # file 삭제
        fs.delete(filename)
        fs.delete(settings.MEDIA_ROOT + f'/{filename}.wav')

        context = speech_to_text(audio)
        # print(context)

        user = get_object_or_404(get_user_model(), username=request.user)
        user_animals = get_list_or_404(User_Animal, user=user)
        
        for user_animal in user_animals:
            if user_animal.name in context:
                response = self.talk_to_one(user_animal, user, context)
                return Response(response)
        
        response = self.talk_to_all(context, user)
        return Response(response)


class AnimalPlayMaze(APIView):
    def post(self, request):
        pass


class AnimalsPlayWordChainView(APIView):
    def post(self, request):
        pass

