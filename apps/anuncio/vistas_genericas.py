from rest_framework.generics import (
    get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from .models import Categoria,Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from apps.usuario.models import Usuario #para poder usar un suario


#crea y muestra usando como modelo las categorias
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    
#muestra,actualiza o destruye una categoria
class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

#Desarrollo del TP 3
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
