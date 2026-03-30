from django.contrib import admin
from apps.anuncio.models import Categoria, Anuncio

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa']

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'precio_inicial', 'fecha_publicacion', 'fecha_inicio', 'activo']
    list_filter = ['activo']