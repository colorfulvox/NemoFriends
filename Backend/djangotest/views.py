from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import TestSerializer, ArraySerializer
from animals.models import Animal
import json

from utils import *
from django.core.files.storage import FileSystemStorage

from django.conf import settings
class TestView(APIView):
    def post(self,request):
        test_serializer = TestSerializer(data=request.data)
        if test_serializer.is_valid(raise_exception=True):
            test_data = test_serializer.save()
        return Response(test_serializer.data)

class ArrayView(APIView):
    def post(self, request):
        serializer = ArraySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            print(data.column)
        return Response(serializer.data)

class DataAnimals(APIView):
    def post(self, request):
        with open('animals.json', encoding='utf-8') as json_file:
            data = json.load(json_file)['results']
            for animal in data:
                Animal.objects.create(**animal)
            print(type(data))

class AudioView(APIView):
    def post(self, request):
        audio = request.FILES.get("audio")


        # multipart/form-data로 받은 file을 테스트를 위해 bytes로 변환한 후
        # bytes를 wav 파일로 저장

        with open('media/copy.wav', mode='bx') as f:
            f.write(audio.file.read())

        # 서버에 file 저장
        fs = FileSystemStorage()
        filename = fs.save(audio.name, audio)

        # file의 경로
        uploaded_file_path = fs.path(filename)

        # file 삭제
        fs.delete(filename)
        fs.delete(settings.MEDIA_ROOT + '/copy.wav')
        return Response(SUCCESS)