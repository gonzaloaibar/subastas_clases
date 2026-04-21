from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.anuncio.filters import AnuncioFilter
from apps.anuncio.models import Categoria, Anuncio
from apps.usuario.models import Usuario #para forzar el usuario al agregar (POST) un nuevo anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer
from rest_framework import viewsets
from django.utils import timezone
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters


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

#vistas genericas para anuncio y categoria
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    '''este metodo hace que no necesite agregar un usaurio manualmente'''
    def perform_create(self, serializer):
        usuario = Usuario.objects.get(username='ceciga')
        serializer.save(publicado_por=usuario)

#muestra,actualiza o destruye un anuncio
class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer


#vista con viewset para categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nombre', 'activa']
    ordering_fields = ['nombre', 'activa']

#vista con viewset para Anuncio
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
            return Response({"error":"este anuncio no tiene fecha de cierre",
                             "anuncio": anuncio.titulo,})

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
            "anuncio": anuncio.titulo,
            "dias": dias,
            "horas": horas,
            "minutos": minutos
        })

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
    ordering_fields = ['nombre', 'activa', 'precio_inicial', 'fecha_fin']