from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria,Anuncio

class AnuncioFilter(filters.FilterSet):

    #filtro por titulo, lookup_expr='icontains' indica que dara resultados que coincidan parcialmente
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')

    #filtro por categorias, uso __ en categorias__nombre para indicar que quieres acceder a algo dentre de ese campo porque categoria es otro modelo
    categoria_nombre=filters.CharFilter(field_name='categorias__nombre', lookup_expr='icontains')
    #categorias = filters.NumberFilter(field_name="categorias__id") #filtra categoria por id

    #filtrar segun un rango de precios, gte=mayor o igual a, lte=menor a igual que
    precio_min = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')

    #filtrar por rango de fecha de finalizacion
    fecha_fin_min = filters.DateFilter(field_name='fecha_fin', lookup_expr='gte')
    fecha_fin_max = filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')


class OfertaAnuncioFilter(filters.FilterSet):

    #filtro segun anuncio
    anuncio_nombre=filters.CharFilter(field_name='anuncio__titulo', lookup_expr='icontains')

    #filtro segun rango de fechas fecha de oferta
    fecha_oferta_min=filters.DateFilter(field_name='fecha_oferta', lookup_expr='gte')
    fecha_oferta_max=filters.DateFilter(field_name='fecha_oferta', lookup_expr='lte')