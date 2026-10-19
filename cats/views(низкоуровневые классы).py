# Обновлённый views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Cat
from .serializers import CatSerializer

class APICat(APIView):
    def get(self, request):
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        if isinstance(request.data, list):
            serializer = CatSerializer(data=request.data, many=True)
        else:
            serializer = CatSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APICatDetail(APIView):
    def _get_cat(self, pk):
        return get_object_or_404(Cat, pk=pk)

    def get(self, request, pk):
        # cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(self._get_cat(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        # cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(self._get_cat(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # cat = get_object_or_404(Cat, pk=pk)
        serializer = CatSerializer(self._get_cat(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # cat = get_object_or_404(Cat, pk=pk)
        self._get_cat(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
