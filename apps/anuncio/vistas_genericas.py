from rest_framework.generics import (
    get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from .models import Categoria
from .serializers import CategoriaSerializer

#crea y muestra usando como modelo las categorias
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    
#muestra,actualiza o destruye una categoria
class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

#Desarrollo del TP 3