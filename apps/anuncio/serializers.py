from rest_framework import serializers
from .models import Categoria, Anuncio

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
        'id',
        'nombre',
        'activa',
        ]


class AnuncioSerializer(serializers.ModelSerializer):
    #obtengo la lista de categorias del anuncio
    categorias = serializers.ListField(
        child=serializers.DictField(),#DictField me devuelve cada elemento {'nombre':'valor'}
        required=False,#le indico que no es necesario en caso de PATCH
        write_only=True,#indico que solo se usa para entradas PATCH/POST
    )

    categorias_detalle = serializers.SerializerMethodField() #para salida, Rebuscado, llama al metodo get_categorias_detalle

    class Meta:
        model = Anuncio
        fields = [
        'id',
        'titulo',
        'descripcion',
        'precio_inicial',
        'imagen',
        'fecha_inicio',
        'fecha_fin',
        'activo',
        'categorias',
        'categorias_detalle',
        'publicado_por',
        'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

    #recorre las categorias y las transforma a JSON
    def get_categorias_detalle(self, obj):
        return [
            {"id": cat.id, "nombre": cat.nombre}
            for cat in obj.categorias.all()
        ]

    def create(self,validated_data):
        #traigo la lista de categorias que existen
        categorias_data = validated_data.pop('categorias',[])

        usuario = validated_data.pop('publicado_por',None)

        '''
        if usuario is None:
            usuario.self.context['request'].usuario
        '''
        #creo un anuncio
        anuncio = Anuncio.objects.create(publicado_por=usuario,**validated_data)

        lista_categorias = []

        for categoria in categorias_data:

            categoria ,creado = Categoria.objects.get_or_create(nombre=categoria['nombre'])

            lista_categorias.append(categoria)

        if lista_categorias:
            anuncio.categorias.set(lista_categorias)

        return anuncio

    #instance es el objeto actual a cambiar, validated_data contiene el json ya verificado para la modificacion del objeto actual
    def update(self, instance, validated_data):
        #obtengo todas las categorias del anuncio
        categorias_data = validated_data.pop('categorias', None)

        #validated_data.items me devuelve la tupla (dato, valor) serializado de cada atributo del anuncio porque es como si estuviera recorriendo el json
        for attr, value in validated_data.items():
            #setattr de forma dinamica toma la instancia del modelo que estoy modificando y modifica los atributos
            setattr(instance, attr, value)

        instance.save()

        #manejo las categorias (M2M) solo si vienen en el request (por la operacion PATCH)
        if categorias_data is not None:
            #lista vacia para nuevas categorias si es necesario
            categoras_obj = []

            #recorro las categorias del request para verificar si ya existen o habra que crearlas
            for categoria in categorias_data:
                categoria, creado = Categoria.objects.get_or_create(nombre=categoria['nombre'])
                categoras_obj.append(categoria)
            instance.categorias.set(categoras_obj)

        return instance
