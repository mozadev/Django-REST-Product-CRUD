from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    activo = serializers.BooleanField()

    def create(self, validate_data):
        return Categoria.objects.create(**validate_data)


class ProductoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    #categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source="categoria")
    categoria_id =serializers.IntegerField()
    categoria = serializers.SerializerMethodField()

    def get_categoria(self, obj):
        if obj.categoria is not None:
            return {
                # "id": obj.categoria.id,
                "nombre": obj.categoria.nombre.upper(),
                "activo": "si" if obj.categoria.activo else "No"
            }
        return None
    
    def validate_categoria_id(self, value):
        if not Categoria.objects.filter(id=value, activo=True).exists():
            raise serializers.ValidationError("La categoria proporcionada no existe.")
        return value
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El error debe ser mayor que 0")
        return value

    def create(self, validated_data):
        return Producto.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.save()
        return instance
    
    
    





