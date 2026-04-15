from xml.etree.ElementInclude import include

from apps.anuncio.api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioDetalleAPIView
from apps.anuncio.api import AnuncioListaAPIView
from django.urls import path
from .api import CategoriaListaGenericView, CategoriaDetalleGenericView, AnuncioListGenericView, AnuncioDetalleGenericView


app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncios/', AnuncioListaAPIView.as_view()),
    path('api-view/anuncios/<pk>/', AnuncioDetalleAPIView.as_view()),

    #urls vistas genericas para categoria y anuncio

    path('mixin-view/anuncios/', AnuncioListGenericView.as_view()),
    path('mixin-view/anuncios/<int:pk>/', AnuncioDetalleGenericView.as_view()),
]