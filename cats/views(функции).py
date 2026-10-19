from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cat
from .serializers import CatSerializer


@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'POST':
        # Создаём объект сериализатора 
        # и передаём в него данные из POST-запроса
        if isinstance(request.data, list):
            serializer = CatSerializer(data=request.data, many=True)
        else:
            serializer = CatSerializer(data=request.data)

        if serializer.is_valid():
            # Если полученные данные валидны —
            # сохраняем данные в базу через save().
            serializer.save()
            # Возвращаем JSON со всеми данными нового объекта
            # и статус-код 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные не прошли валидацию — 
        # возвращаем информацию об ошибках и соответствующий статус-код:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def cat_detail(request, pk):
    cat = Cat.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = CatSerializer(cat)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CatSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        serializer = CatSerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cat.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
