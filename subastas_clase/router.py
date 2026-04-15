from rest_framework import routers
from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()
# Registrar un ViewSet
router.register(prefix='categoria', viewset=CategoriaViewSet)
router.register(prefix='anuncios',viewset=AnuncioViewSet) #urls de anuncios