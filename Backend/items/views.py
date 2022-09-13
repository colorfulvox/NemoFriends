from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import User_Decoration, Decoration
from .serializers import ItemsUpdateSerializer, ItemsCreateSerializer


# 조경 생성 테스트용
class ItemsCreateView(APIView):
    def post(self, request):
        serializer = ItemsCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class ItemsUpdateView(APIView):
    def put(self, request):
        user_decoration = get_object_or_404(User_Decoration, id=request.data.get("id"))

        if request.user == user_decoration.user_id:
            serializer = ItemsUpdateSerializer(instance=user_decoration, data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True})
        
        return Response({'success': False})


class ItemsBuyView(APIView):
    def post(self, request):
        decoration = get_object_or_404(Decoration, id=request.data.get("id"))

        user_decoration = User_Decoration(user_id=request.user, decoration_id=decoration, is_located=False, location=-1, angle=-1)
        user_decoration.save()

        response = {"success": True, "id": user_decoration.id}

        return Response(response, status=status.HTTP_201_CREATED)