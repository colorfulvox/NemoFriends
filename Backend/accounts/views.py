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
from .serializers import UserChangeBGMSerializer, UserChangeEffectSerializer
from animals.models import User_Animal, Animal
from items.models import Color, Decoration, User_Color, User_Decoration
from utils import *

state = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

class StartAnimalView(APIView):
    def post(self,request):
        response = FAIL
        user = request.user
        animal = get_object_or_404(Animal, id=1)
        
        user_animal = User_Animal(user=request.user, animal=animal, name=animal.species, color_id=0)
        user_animal.save()
        response = SUCCESS
        return Response(response)
class UserDeleteView(APIView):
    def delete(self,request):
        response = FAIL.copy()

        user = request.user
        user.delete()

        response = SUCCESS
        return Response(response)

class GachaView(APIView):
    def post(self,request):
        res = Response()
        response = FAIL.copy()
        user = request.user
        # 돈이 있는지 체크
        if user.gold >= 300:
        # 돈이 있다면 동물 목록(가지고 있지 않은), 염색약 목록, 희귀조경 목록을 가져와 하나의 리스트에 저장
            random_box = []
            own_animals = [i.animal for i in User_Animal.objects.filter(user=user)] 
            all_animals = Animal.objects.all()
            colors = Color.objects.all()
            decos = Decoration.objects.filter(is_rare=True)
            for animal in all_animals:
                random_box.append(animal)

            for check_animal in random_box[:]:
                if check_animal in own_animals:
                    random_box.remove(check_animal)
            for color in  colors:
                random_box.append(color)
            for deco in decos:
                random_box.append(deco)
        # 랜덤 함수로 번호 선정
            number = random.randint(0, len(random_box)-1)
            obj = random_box[number]
        # 뽑힌 오브젝트의 타입 판별
            # 동물일 경우(animals.models.Animal)
            if type(obj) is Animal:
                user_animal = User_Animal(user=user, animal=obj, name=obj.species, color_id=0)
                user_animal.save()
                response.update({"result" : {"type" : "animal", "pk" : user_animal.id,"id" : obj.id}})
            # 조경일 경우
            elif type(obj) is Decoration:
                user_decoration = User_Decoration(user=user, decoration=obj, is_located=False, location=-1, angle=-1)
                user_decoration.save()
                response.update({"result" : {"type" : "decoration", "pk" : user_decoration.id,"id" : obj.id}})

            # 염색약일 경우
            elif type(obj) is Color:
                user_colors = user.user_color_set.all()
                check = False
                id = ""
                for user_color in user_colors:
                    if user_color.color == obj:
                        check = True
                        user_color.cnt += 1
                        user_color.save()
                        id = user_color.id
                        break;
                if not check:
                    user_color = User_Color(user=user, color=obj)
                    user_color.save()
                    id = user_color.id
                response.update({"result" : {"type" : "color", "pk" : id,"id" : obj.id}})
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