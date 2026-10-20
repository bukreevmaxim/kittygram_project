# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def create(self, request, *args, **kwargs):
            if isinstance(request.data, list):
                serializer = CatSerializer(data=request.data, many=True)
            else:
                serializer = CatSerializer(data=request.data)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
