from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.anuncio.models import Categoria, Anuncio
from apps.usuario.models import Usuario #para forzar el usuario al agregar (POST) un nuevo anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from django.utils import timezone
#from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime #para usar fechas


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


#vista para obtener las categorias y agregar una categoria
class CategoriaListaAPIView(APIView):

    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#vista para obtener, modificar, eliminar una categoria
class CategoriaDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#vista para obtener los anuncios y agregar uno
class AnuncioListaAPIView(APIView):
    def get(self, request, format=None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():

            #ESTOY FORZANDO EL USO CON EL USUARIO ADMINISTRADOR SOLO PARA PRUEBAS
            usuario=Usuario.objects.get(username='ceciga')

            serializer.save(publicado_por=usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#vista para obtener, modificar y eliminar un anuncio
class AnuncioDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##################################### vistas genericas para categoria y anuncio

from rest_framework.generics import (
get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

#vistas concretas para categoria y vistas genericas para anuncio
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioListGenericView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        user = Usuario.objects.get(username='ceciga')
        serializer.save(publicado_por=user)


class AnuncioDetalleGenericView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

##################################### vistas con ViewSet para categoria y anuncio

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()#consulta a la db
    serializer_class = AnuncioSerializer#indico el serializador que debe usar

    #sobrescribo el metodo perform_create de ModelViewSet para forzar el usuario
    def perform_create(self, serializer):
        user = Usuario.objects.get(id=1)
        serializer.save(publicado_por=user)

    #accion personalizada
    @action(methods=['get'], detail=True)
    def tiempo_restante(self, request, pk=None):
        try:
            anuncio = self.get_object()
        except Http404:
            return Response(
                {"error": "El anuncio buscado no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        #validar si el anuncio tiene fecha de fin
        if not anuncio.fecha_fin:
            return Response({"error":"este anuncio no tiene fecha de cierre"})

        #calculo el tiempo que falta
        hoy=timezone.now()
        tiempo_faltante=anuncio.fecha_fin - hoy

        #notifico si el anuncio ya finalizo
        if tiempo_faltante.total_seconds() <= 0:
            return  Response({"info":"el anuncio ya finalizo"})

        #obtener dias, horas y minutos para el json
        dias=tiempo_faltante.days
        segundos=tiempo_faltante.seconds
        horas=segundos/3600
        minutos=(segundos/3600) // 60

        return Response({
            "dias": dias,
            "horas": horas,
            "minutos": minutos
        })