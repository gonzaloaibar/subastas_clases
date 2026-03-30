from apps.anuncio.api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioDetalleAPIView
from apps.anuncio.api import AnuncioListaAPIView
from django.urls import path

app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncio/', AnuncioListaAPIView.as_view()),
    path('api-view/anuncio/<pk>/', AnuncioDetalleAPIView.as_view()),
]