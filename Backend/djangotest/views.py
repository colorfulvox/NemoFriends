from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import TestSerializer, ArraySerializer
from animals.models import Animal
import json
import io
import numpy
# import soundfile as sf

class AudioTestView(APIView):
    def put(self, request):
#         print('request', request)
#         file = request.data.get('vocie')
#         print(file, type(file))
#         # pprint(file.__dir__())
#         print(f'name: {file.name}, file: {file.file}, filed_name: {file.field_name}, content_type: {file.content_type}, charset: {file.charset}, size: {file.size}')
#         with open('media/copy.wav', mode='bx') as f:
#             f.write(audio.file.read()) 
#         a = bytearray(response)
#         f = BytesIO(response)
#         print(f.getvalue())

#         print('response 일부', response[:20], type(response))
#         # print('s일부', s, type(s))
#         # print('a일부', a[:20], type(a))
#         # print('response', response[:20], type(response))
#         # b = numpy.array(a, dtype=numpy.int16)
#         # scipy.io.wavfile.write(r"")
#         # (file: {file.file}, filed_name: {file.field_name}, content_type: {file.content_type}, charset: {file.charset}, size: {file.size}')
#         # print(request.FILES.__dir__())
#         print(request.FILES.keys(), request.FILES.values())
#         # audio = request.FILIES.__getattribute__('file')
#         # print('audio', audio, type(audio))
        pass

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
