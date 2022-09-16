from datetime import datetime
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
import requests, random

from .models import User
from .serializers import UserChangeBGMSerializer, UserChangeEffectSerializer, UserAnimalInfoSerializer, UserItemInfoSerializer, AnimalInfoSerializer, ShopInfoSerializer
from animals.models import User_Animal, Animal
from items.models import Item, Decoration, User_Item, User_Decoration
from utils import *

state = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

class StartAnimalView(APIView):
    def get(self,request):
        response = FAIL
        user = request.user
        animal = get_object_or_404(Animal, id=1)

        user_animal = User_Animal(user=user, animal=animal, name=animal.species, color_id=0)
        user_animal.save()
        response = SUCCESS
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
        list = [0 for i in range(0,decoration_len.count())]
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
        # 아이템 정보 가공
        items = user.user_item_set.all()
        items_serializer = UserItemInfoSerializer(items, many=True)
        items_data = items_serializer.data
        items_data.insert(0,{})
        # 유저 정보 Json
        user_info = {
            "name" : user.name,
            "gold" : user.gold,
            "decorations" : decorations_ilst,
            "located_decorations": located_decorations,
            "items" : items_data,
            "is_called" : user.is_called,
            "bgm" : user.bgm,
            "effect" : user.effect
        }

        # 게임 정보 - 동물 정보 가공
        animals = Animal.objects.all()
        animals_serializer = AnimalInfoSerializer(animals, many=True)
        for animal in animals_serializer.data:
            animal['feeds'].insert(0,[])
            animal['features'].insert(0,"")
            animal['commands'].insert(0,"")
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
    def delete(self,request):
        response = FAIL.copy()

        user = request.user
        user.delete()

        response = SUCCESS
        return Response(response)

class GachaView(APIView):
    def get(self,request):
        res = Response()
        response = FAIL.copy()
        user = request.user
        # 돈이 있는지 체크
        if user.gold >= 300:
        # 돈이 있다면 동물 목록(가지고 있지 않은), 염색약 목록, 희귀조경 목록을 가져와 하나의 리스트에 저장
            random_box = []
            own_animals = [i.animal for i in User_Animal.objects.filter(user=user)]
            all_animals = Animal.objects.all()
            items = Item.objects.all()
            decos = Decoration.objects.filter(is_rare=True)
            for animal in all_animals:
                random_box.append(animal)

            for check_animal in random_box[:]:
                if check_animal in own_animals:
                    random_box.remove(check_animal)
            for item in  items:
                random_box.append(item)
            for deco in decos:
                random_box.append(deco)
        # 랜덤 함수로 번호 선정
            number = random.randint(0, len(random_box)-1)
            obj = random_box[number]
        # 뽑힌 오브젝트의 타입 판별
            # 동물일 경우(animals.models.Animal)
            if type(obj) is Animal:
                user_animal = User_Animal(user=user, animal=obj, name=obj.species, item_id=0)
                user_animal.save()
                response.update({"result" : {"type" : "animal", "pk" : user_animal.id,"id" : obj.id}})
            # 조경일 경우
            elif type(obj) is Decoration:
                user_decoration = User_Decoration(user=user, decoration=obj, is_located=False, location=-1, angle=-1)
                user_decoration.save()
                response.update({"result" : {"type" : "decoration", "pk" : user_decoration.id,"id" : obj.id}})

            # 염색약일 경우
            elif type(obj) is Item:
                user_items = user.user_item_set.all()
                check = False
                id = ""
                for user_item in user_items:
                    if user_item.item == obj:
                        check = True
                        user_item.cnt += 1
                        user_item.save()
                        id = user_item.id
                        break;
                if not check:
                    user_item = User_Item(user=user, item=obj)
                    user_item.save()
                    id = user_item.id
                response.update({"result" : {"type" : "item", "pk" : id,"id" : obj.id}})
            # 타입별로 DB에 저장이 완료되었다면 골드 차감
            user.gold -= 300
            user.save()
            # 성공메시지 반환
            response["success"] = True
            res.data = response
            return res
        elif user.gold < 300:
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


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client