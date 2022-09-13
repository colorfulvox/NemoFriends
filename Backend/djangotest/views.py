from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import TestSerializer, ArraySerializer
# Create your views here.


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