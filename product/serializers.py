from rest_framework import serializers
from .models import Producto

class CategoriaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    activo = serializers.BooleanField()


class ProductoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    categoria = serializers.SerializerMethodField()

    def get_categoria(self, obj):
        return {
            "id": obj.categoria.id,
            "nombre": obj.categoria.nombre,
            "activo": obj.categoria.activo
        }

    def create(self, validated_data):
        return Producto.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance
    
    
    


