from datetime import datetime
from os import access
import re
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from django.http import JsonResponse


from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status
from rest_framework.response import Response
from json.decoder import JSONDecodeError
from rest_framework.decorators import APIView
from utils import *
import requests, random

from .models import Mbti, User
from .serializers import UserChangeBGMSerializer, UserChangeEffectSerializer, UserAnimalInfoSerializer, UserItemInfoSerializer, AnimalInfoSerializer, ShopInfoSerializer
from animals.models import User_Animal, Animal
from items.models import Item, Decoration, User_Item, User_Decoration
import logging

logger = logging.getLogger(__name__)


def date_init():
    # 매일 자정에 초기화 되는 컬럼 : 모두 부르기(User), 놀아주기 횟수, 대화하기 횟수(User_animal)
    users = User.objects.all()
    user_animals = User_Animal.objects.all()

    users.update(is_called = default.get('is_called'))
    user_animals.update(talking_cnt=default.get('talking_cnt'), playing_cnt=default.get('playing_cnt'))

    logger.info('스케줄링 완료')

class StartAnimalView(APIView):
    def post(self, request):

        MBTI_STATIC = { 
            '1111': [1, 'ISTJ'],
            '1112': [2, 'ISTP'],
            '1121': [3, 'ISFJ'],
            '1122': [4, 'ISFP'],
            '1211': [5, 'INTJ'],
            '1212': [6, 'INTP'],
            '1221': [7, 'INFJ'],
            '1222': [8, 'INFP'],
            '2111': [9, 'ESTJ'],
            '2112': [10, 'ESTP'],
            '2121': [11, 'ESFJ'],
            '2122': [12, 'ESFP'],
            '2211': [13, 'ENTJ'],
            '2212': [14, 'ENTP'],
            '2221': [15, 'ENFJ'],
            '2222': [16, 'ENFP'],
        }
        # 동물 추천 알고리즘
        user = request.user
        if User_Animal.objects.filter(user=user).exists():
            return Response(FAIL)

        user_animals = user.user_animal_set.all()
        user_animals_count = user_animals.count()
        # 조작 이용자(튜토리얼로 강제 진입한 경우 등)
        if user_animals_count != 0:
            return Response({"success" : False})

        answer = request.data.get('answer')
        mbti = get_object_or_404(Mbti, mbti=MBTI_STATIC[answer][1])
        animal = mbti.animal
        # user = request.user  63번 라인과 같아서 주석해둬여 혹시 이유가 있으면 다시 풀어주세요!
        user_animal = User_Animal(user=user, animal=animal, name=animal.species, is_located=True)
        user_animal.save()
        user_animals_serializer = UserAnimalInfoSerializer(user_animal)

        response = {
            "animal" : user_animals_serializer.data,
            "mbti_id" : MBTI_STATIC[answer][0]
        }
        return Response(response)

class QuestionView(APIView):
    def get(self,request):
        response = FAIL.copy()

        questions = {
            "IE" : [
                {
                    "question" : "꼭 이 두 가지 동물 중 하나가 되어야 한다면?",
                    "ans1" : "나는야 고독한 맹수 호랑이. 나만의 길을 걷는다.",
                    "ans2" : "사자 대가족의 일원, 다같이 살아가는 게 인생이지."
                },
                {
                    "question" : "평화로운 휴일, 동네 친구 여우가 갑자기 놀러가자고 불러냈어요.",
                    "ans1" : '"나 바빠" 사실 하나도 안 바쁘지만 바쁘다고 하고 집에서 쉰다.',
                    "ans2" : '"당연히 가야지!" 한가했는데 마침 잘됐다.'
                }
            ],
            "SN" : [
                {
                    "question" : "당신은 곰입니다. 좋아하는 꿀을 가지고 맛있는 요리를 할 수 있는 레시피를 구했어요.",
                    "ans1" : '"레시피가 정답이야!" 레시피에 적힌대로 정확히 요리를 한다.',
                    "ans2" : '"내 입맛에 맞아야지!" 내 감각을 믿고 눈대중, 손대중으로 양을 맞춘다.'
                },
                {
                    "question" : "당신은 병아리입니다. 내일 다른 병아리들과 소풍을 떠나기로 했어요.",
                    "ans1" : '"내일 재밌겠다! 빨리 자야지" 바로 잠에 든다.',
                    "ans2" : '"내일 비오지는 않겠지? 누가 날 잡아먹으면 어떡해?" 걱정이 줄줄 이어진다.'
                }
            ],
            "TF" : [
                {
                    "question" : "원숭이가 누군가 몰래 빼먹은 바나나를 보며 주저앉아 엉엉 울고있어요.",
                    "ans1" : '"지금 이럴 때가 아니야! 빨리 범인을 찾아야지!" 범인을 찾으러 가자고 한다.',
                    "ans2" : '"너무 슬프겠다... 정말 아끼는 바나나였잖아 ㅠㅠㅠ" 옆에서 같이 운다.'
                },
                {
                    "question" : "친구 원숭이가 정말 어려운 공중제비를 성공했어요!",
                    "ans1" : '"와 이걸 성공하네" 성공했다는 사실에 감탄한다.',
                    "ans2" : '"얼마나 열심히 연습했을까... 고생했어." 그동안의 노력에 감탄한다.'
                }
            ],
            "JP" : [
                            {
                    "question" : "당신은 다람쥐가 되었습니다. 집에 있는 먹을 것들은 어떤 모습인가요?",
                    "ans1" : '해바라기 씨, 도토리, 아몬드, 호박씨.. 종류별로 깔끔하게 나뉘어 있다.',
                    "ans2" : '한 구덩이에 뭉텅이로 모여있다.'
                },
                {
                    "question" : "친구 거북이가 내일 약속시간을 바꿀 수 있냐고 물어봤어요.",
                    "ans1" : '"시간이 바뀌면 내일 짜둔 계획이 틀어지는데..." 불편하다.',
                    "ans2" : '"그래~ 혹시 시간 당겨진 건 아니지?" 별 생각 없다. 시간이 미뤄지면 왠지 기분이 좋다.'
                }
            ]
        }
        response = {
            "mbti" : [
                {},
                questions["IE"][random.randint(0, 1)],
                questions["SN"][random.randint(0, 1)],
                questions["TF"][random.randint(0, 1)],
                questions["JP"][random.randint(0, 1)],
            ]
        }

        return Response(response)


class LoadGameView(APIView):
    def get(self, request):
        # id = request.data.get('id')
        # 구글 로그인 부분
        response = Response()
        user = request.user
        # user = get_object_or_404(User, username=id) # 이 코드는 추후 구글로그인 때 사용 할 지도?

        # 데이터 전달 부분 : 로그인 직후 바로 보내는 것이기 때문에 jwt 토큰 없이 진행될 수 있음.

        # 획득한 동물 정보
        user_animals = user.user_animal_set.all()
        user_animals_serializer = UserAnimalInfoSerializer(user_animals,many=True)
        # 시간정보 '/' 구분자로 변경
        for user_animal in user_animals_serializer.data:
            user_animal['last_eating_time']=user_animal['last_eating_time'].replace('-','/')
            user_animal['last_eating_time']=user_animal['last_eating_time'].replace('T','/')
            user_animal['last_eating_time']=user_animal['last_eating_time'].replace(':','/')
            user_animal['created_at']=user_animal['created_at'].replace('-','/')
        # 리스트 패딩
        user_animals_data = user_animals_serializer.data.copy()
        user_animals_data.insert(0,{})
        # 가구 정보 가공 : 보관함
        decorations = user.user_decoration_set.all()
        decoration_len = Decoration.objects.all()
        list = [0 for i in range(0,decoration_len.count()+1)]
        for decoration in decorations:
            if not decoration.decoration.is_rare and not decoration.is_located:
                list[decoration.decoration.id] += 1
        decorations_ilst = []
        decorations_ilst.append({})
        for i in range(0,len(list)):
            if list[i] != 0:
                decorations_ilst.append({
                    "decoration_id" : i,
                    "cnt" : list[i],
                })
        # 가구 정보 가공 : 배치 가구
        located_decorations = []
        located_decorations.append({})
        for decoration in decorations:
            if decoration.is_located:
                located_decorations.append({
                    "id" : decoration.id,
                    "location" : decoration.location,
                    "decoration_id" : decoration.decoration.id,
                    "angle" : decoration.angle,
                })
        # 유저 정보 Json
        user_info = {
            # "name" : user.name
            "gold" : user.gold,
            "decorations" : decorations_ilst,
            "located_decorations": located_decorations,
            "exp_cnt" : user.exp_cnt,
            "is_called" : user.is_called,
            "bgm" : user.bgm,
            "effect" : user.effect
        }

        # 게임 정보 - 동물 정보 가공
        animals = Animal.objects.all()
        animals_serializer = AnimalInfoSerializer(animals, many=True)
        for animal in animals_serializer.data:
            one_feed = animal['feeds'][1]
            two_feed = animal['feeds'][2]
            three_feed = animal['feeds'][3]
            animal['feeds'] = {
                "one" : one_feed,
                "two" : two_feed,
                "three" : three_feed
            }
        animals_data = animals_serializer.data.copy()
        animals_data.insert(0,{})

        # 게임 정보 - 상점 정보 가공
        shop = Decoration.objects.exclude(is_rare=True)
        shop_serializer = ShopInfoSerializer(shop, many=True)
        shop_data = shop_serializer.data.copy()
        shop_data.insert(0,{})
        # 게임 정보 Json
        gameinfo = {
            "animal" : animals_data,
            "shop" : shop_data
        }
        response.data = {
            "user_animal" : user_animals_data,
            "user" : user_info,
            "gameinfo" : gameinfo
        }
        return response
class UserDeleteView(APIView):
    def post(self,request):
        response = FAIL.copy()

        if request.data.get('username') == request.user.username:
            user = request.user
            user.delete()
            response = SUCCESS.copy()

        return Response(response)

class GachaView(APIView):
    def get(self,request):
        res = Response()
        response = FAIL.copy()
        user = request.user
        # 돈이 있는지 체크
        if user.gold >= 500:
        # 돈이 있다면 동물 목록(가지고 있지 않은), 염색약 목록, 희귀조경 목록을 가져와 하나의 리스트에 저장
            random_box = []
            own_animals = [i.animal for i in User_Animal.objects.filter(user=user)]
            all_animals = Animal.objects.all()
            decos = Decoration.objects.all()
            for animal in all_animals:
                random_box.append(animal)
            for check_animal in random_box[:]:
                if check_animal in own_animals:
                    random_box.remove(check_animal)
            for deco in decos:
                random_box.append(deco)
            random_box.append("item")
            random_box.append("item")
            random_box.append("item")
            random_box.append("item")
            random_box.append("item")
        # 랜덤 함수로 번호 선정
            number = random.randint(0, len(random_box)-1)
            obj = random_box[number]
        # 뽑힌 오브젝트의 타입 판별
            # 동물일 경우(animals.models.Animal)
            if type(obj) is Animal:
                user_animal = User_Animal(user=user, animal=obj, name=obj.species)
                user_animal.save()
                user_animals_serializer = UserAnimalInfoSerializer(user_animal)
                response.update({"type" : "animal", "pk" : user_animal.id,"id" : obj.id,"animal" : user_animals_serializer.data})
            # 조경일 경우
            elif type(obj) is Decoration:
                user_decoration = User_Decoration(user=user, decoration=obj, is_located=False, location=-1, angle=-1)
                user_decoration.save()
                response.update({"type" : "decoration", "pk" : user_decoration.id,"id" : obj.id})

            # 경험치약일 경우
            elif obj == "item":
                user.exp_cnt += 1
                user.save()
                response.update({"type" : "exp"})
            # 타입별로 DB에 저장이 완료되었다면 골드 차감
            user.gold -= 500
            user.save()
            # 성공메시지 반환
            response["success"] = True
            res.data = response
            return res
        elif user.gold < 500:
            response = FAIL
            res.data = response
            return res

class ChangeBGMView(APIView):
    def post(self,request):
        response = FAIL
        user = request.user
        serializers = UserChangeBGMSerializer(instance=user, data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
        User.objects
        response = SUCCESS
        return Response(response)

class ChangeEffectView(APIView):
    def post(self,request):
        response = FAIL
        user = request.user
        serializers = UserChangeEffectSerializer(instance=user, data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
        response = SUCCESS
        return Response(response)
