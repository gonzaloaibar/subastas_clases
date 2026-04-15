from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.anuncio.models import Categoria, Anuncio
from apps.usuario.models import Usuario #para forzar el usuario al agregar (POST) un nuevo anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer
from rest_framework import viewsets
#from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime #para usar fechas

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    #Accion personalizada para obtener el tiempo restante para que finalice un anuncio
    @action(detail=True) #Solo detail, porque impolicatamente es un metodo GET
    def tiempo_restante_anuncio(self,request, pk=None):
        try:
            anuncio = self.get_object()
        except Http404:
            return Response(
                {"error": "El anuncio buscado no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        fecha_actual = datetime.now()

        dias = anuncio.fecha_fin.day - fecha_actual.day
        horas = abs(anuncio.fecha_fin.hour - fecha_actual.hour)
        minutos = abs(anuncio.fecha_fin.minute - fecha_actual.minute)

        return Response({"dias":dias,
                         "horas":horas,
                         "minutos":minutos})



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