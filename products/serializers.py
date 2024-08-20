from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "description",
            "image",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product