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
    categorias = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
    )

    categorias_detalle = serializers.SerializerMethodField()

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

    def get_categorias_detalle(self, obj):
        return [
            {"id": cat.id, "nombre": cat.nombre}
            for cat in obj.categorias.all()
        ]


    def create(self, validated_data):
        #obtengo la lista de categorias existentes serializada y verfificada
        categorias_data = validated_data.pop('categorias', [])

        #obtengo el usuario asociado al anuncio desde la vista
        user = validated_data.pop('publicado_por', None)
        #si la vista no me lo envia lo obtengo desde el request (caso improbable)
        if user is None:
            user = self.context['request'].user

        #creo el anuncio con toda la informacion verificada y el usuario
        anuncio = Anuncio.objects.create(publicado_por=user, **validated_data)

        #lista vacia para categorias nuevas
        categorias_obj = []
        #recorro la lista de categorias del anuncio
        for categoria in categorias_data:
            #get_or_create me devuelve una tupla (la categoria, True si se creo la categoria False caso contrario(osea ya existia))
            categoria, creado = Categoria.objects.get_or_create(nombre=categoria['nombre'])
            #agrego la categoria a la lista
            categorias_obj.append(categoria)

        #se agregan la lista de categorias al anuncio si no esta vacia
        if categorias_obj:
            anuncio.categorias.set(categorias_obj)

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
