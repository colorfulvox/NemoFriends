from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal, User_Animal
from .serializers import AnimalsRenameSerializer, AnimalsTestSerializer
from utils import *

# class AnimalsEatView(APIView):
#     def put(self, request):
#         pass

class AnimalsRenameView(APIView):
    def put(self, request):
        id = request.data.get('id')
        user_animal = get_object_or_404(User_Animal, pk=id)

        if request.user == user_animal.user:
            serializers = AnimalsRenameSerializer(instance=user_animal, data=request.data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return Response(SUCCESS)
        # 로그인 안되있어서 request.user가 AnoymousUser로 나옴
        else:
            FAIL['reason'] = '유저의 정보가 일치하지 않습니다.'
            return Response(FAIL)


# class AnimalsColorView(APIView):
#     def put(self, request):
#         pass

# class AnimalsTalkView(APIView):
#     def put(self, request):
#         pass

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