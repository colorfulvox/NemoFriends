from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal, User_Animal
from items.models import User_Item
from accounts.models import WordChain
from .serializers import AnimalsRenameSerializer, AnimalsTestSerializer, UserAnimalSerializer
from . import serializers
from .utils import *
from utils import SUCCESS, FAIL

import random
from datetime import datetime, timedelta
from time import strftime, strptime


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
        user_animal = get_object_or_404(User_Animal, id=id)
        
        if request.user == user_animal.user:
            serializer = AnimalsRenameSerializer(instance=user_animal, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(SUCCESS)
        else:
            return Response(FAIL)


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
        context = recongize(request.user.username, request.FILES["audio"])

        user = get_object_or_404(get_user_model(), username=request.user)
        user_animals = get_list_or_404(User_Animal, user=user)
        
        for user_animal in user_animals:
            if user_animal.name in context:
                response = self.talk_to_one(user_animal, user, context)
                return Response(response)
        
        response = self.talk_to_all(context, user)
        return Response(response)


class AnimalsPlayWordchainStartView(APIView):
    def post(self, request):
        user = request.user
        animal_id = request.data.get('animal_id')
        animal = get_object_or_404(Animal, pk=animal_id)
        user_animal = get_object_or_404(User_Animal, user=user, animal=animal)

        if user_animal.playing_cnt < 1:
            response = FAIL.copy()
            response.update({'message': '오늘은 더 이상 놀아줄 수 없습니다.'})
            return Response(response)

        response_word = random.choice(start_words)

        # 삭제되지 않은 게임 기록 확인
        check = WordChain.objects.filter(user=user)
        if check:
            for wordchain in check:
                wordchain.delete()
            
        wordchain = WordChain(user=user, score=0, words=[response_word])
        wordchain.save()

        response = SUCCESS.copy()
        response.update({'response_word': response_word})

        return Response(response)


class AnimalsPlayWordchainNextView(APIView):
    # 게임 종료
    def finish(self, msg, score, request_word):
        response = FAIL.copy()
        response.update({'message': msg, 'request_word': request_word, 'score': score})
        return response

    def post(self, request):
        request_word = recongize(request.user.username, request.FILES['audio'])

        wordchain = WordChain.objects.get(user_id=request.user)
        words = wordchain.words
        score = wordchain.score
        
        # 사용자의 단어가 사전에 존재하는 단어인지 확인
        if request_word not in noun_dictionary:
            response = self.finish('사전에 존재하지 않는 단어입니다.', score, request_word)
            return Response(response)

        # 사용자의 단어가 이미 사용한 단어인지 확인
        if request_word in words:
            response = self.finish('이미 사용한 단어입니다.', score, request_word)
            return Response(response)

        # 사용자의 단어가 실제로 이어지는 단어인지 확인(두음 법칙 적용)
        ends = [words[-1][-1]]
        if ends[0] in convert_dict.keys():
            ends.append(convert_dict[ends[0]])

        if request_word[0] not in ends:
            response = self.finish('이어지지 않는 단어입니다.', score, request_word)
            return Response(response)
        
        # 시작 글자로 쓸 수 있는 글자들 확인(두음 법칙 적용)
        starts = [request_word[-1]]
        if starts[0] in convert_dict.keys():
            starts.append(convert_dict[starts[0]])
        
        # 다음 단어 선택
        response_words = []
        for word in noun_dictionary:
            if word[0] in starts and word not in words:
                response_words.append(word)
        
        response_word = random.choice(response_words)
        
        # WordChain 테이블 갱신
        wordchain.score += 1
        wordchain.words.append(request_word)
        wordchain.words.append(response_word)
        wordchain.save()

        response = SUCCESS.copy()
        response.update({'request_word': request_word, 'response_word': response_word, 'score': wordchain.score})
        return Response(response)


class AnimalsPlayWordchainFinishView(APIView):
    def post(self, request):
        user = request.user
        wordchain = WordChain.objects.get(user=user)
        score = wordchain.score
        animal_id = request.data.get('animal_id')
        animal = get_object_or_404(Animal, pk=animal_id)
        user_animal = get_object_or_404(User_Animal, user=user, animal=animal)
        action = 'playing'

        # 골드 증가
        user = reward_gold(user, action, score)
        user.save()

        # 놀이 횟수 차감
        user_animal.playing_cnt -= 1

        # 해당 동물 경험치 증가
        user_animal = reward_exp(user_animal, user, action, score)
        user_animal.save()

        # wordchain에서 행 삭제
        wordchain.delete()

        return Response(SUCCESS)


class AnimalsPlaceView(APIView):
    def post(self, request):
        id = request.data.get('id')
        user_animal = get_object_or_404(User_Animal, id=id)

        if request.user == user_animal.user:
            user_animal.is_located = user_animal.is_located ^ 1
            user_animal.save()
            return Response(SUCCESS)
        return Response(FAIL)


class AnimalsMazeView(APIView):
    def post(self, request):
        score = int(request.data.get('score'))
        user = reward_gold(request.user, 'playing_maze', score)
        user.save()
        return Response(SUCCESS)


class AnimalsExpUpView(APIView):
    def post(self, request):
        user = request.user
        user_animal = get_object_or_404(User_Animal, id=request.data.get('id'))
        response = FAIL.copy()

        if user == user_animal.user:
            if 0 < user.exp_cnt:
                user_animal = reward_exp(user_animal, user, 'exp_up')
                user_animal.save()
                user.exp_cnt -= 1
                user.save()
                return Response(SUCCESS)

            response['msg'] = '경험치 물약이 부족합니다.'
            return Response(response)

        response['msg'] = '요청을 보낸 사용자와 해당 동물을 보유한 사용자가 다릅니다.'
        return Response(response)


# class AnimalsColorView(APIView):
#     def post(self, request):
#         response = FAIL.copy() # response: 실패 응답이 담길 dict 

#         user_item_id = request.data.get('user_item_id')

#         if user_item_id == 1:
#             response["message"] = "경험치 물약을 보냈습니다."
#             return Response(response)

#         user_animal_id = request.data.get('user_animal_id')
#         user_animal = get_object_or_404(User_Animal, pk=user_animal_id)
#         user_item = get_object_or_404(User_Item, pk=user_item_id)

#         # 염색 Ok
#         if request.user == user_animal.user == user_item.user:
#             if 1 <= user_item.cnt:
#                 # user_animal 정보
#                 user_animal.color_id = user_item_id
#                 user_animal.save()
#                 # user_color 정보
#                 user_item.cnt -= 1
#                 user_item.save()
#                 return Response(SUCCESS)
#         # 염색 No
#             response["message"] = "보유한 염색약이 없습니다."
#             return Response(response)

#         response["message"] = "유저 정보가 다릅니다."
#         return Response(response)


class DepthTestView(APIView):
    def get(self, request, id):
        user_animal = get_object_or_404(User_Animal, pk=id)
        serializers = UserAnimalSerializer(instance=user_animal)
        return Response(serializers.data)
