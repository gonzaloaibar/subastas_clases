from rest_framework import routers
from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet, OfertaAnuncioViewSet

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()


# Registrar un ViewSet
router.register(prefix='categoria', viewset=CategoriaViewSet)
router.register(prefix='anuncio', viewset=AnuncioViewSet)

router.register(prefix='oferta_anuncio', viewset=OfertaAnuncioViewSet)
