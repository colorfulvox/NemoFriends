from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Animal
from .serializers import AnimalsTestSerializer

# Create your views here.
class AnimalsEatView(APIView):
    def put(self, request):
        pass

class AnimalsTestView(APIView):
    def get(self, request, animal_id, order_id):
        print(request)
        print(order_id, type(order_id))
        animals = get_list_or_404(Animal)
        animal = get_object_or_404(Animal, id=animal_id)
        print(animals)
        # serializer = AnimalsTestSerializer(animals, many=True)
        serializer = AnimalsTestSerializer(animal)
        print(animal)
        space = animal.species
        feed = animal.feeds
        character = animal.characteristics
        commands = animal.commands
        print(f'space: {space}\ncharacter: {character}\ncommands: {commands}\nfeed: {feed}')
        # print('명령', commands[str(order_id)])
        print(commands.keys())
        print('먹이', type(feed[order_id]), feed[order_id])
        return Response(serializer.data)