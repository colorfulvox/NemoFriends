from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import User_Decoration, Decoration
from .serializers import ItemsUpdateRequestSerializer, ItemsCreateRequestSerializer


class ItemsCreateView(APIView):
    def post(self, request):
        serializer = ItemsCreateRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class ItemsUpdateView(APIView):
    def put(self, request):
        response = {"success": False}
        
        user_decoration = get_object_or_404(User_Decoration, id=request.data.get("id"))

        # reqeust를 보낸 user와 user_decoration의 user가 같은지 검증 필요?
        serializer = ItemsUpdateRequestSerializer(instance=user_decoration, data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response["success"] = True

        return Response(response)


class ItemsBuyView(APIView):
    def post(self, request):
        decoration = get_object_or_404(Decoration, id=request.data.get("id"))

        user_decoration = User_Decoration(
            # user_id=,
            decoration_id=decoration,
            is_located=False,
            location=-1,
            angle=-1
        )
        user_decoration.save()

        response = {
            "success": True,
            "id": user_decoration.id
        }

        return Response(response, status=status.HTTP_201_CREATED)