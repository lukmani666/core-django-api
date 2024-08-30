from rest_framework import serializers
from .models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "product", "total_price", "created_at", "updated_at"]

    def validate(self, data):
        # product_id = data.get("product").id
        product = self.context.get('product')
        quantity = data.get("quantity")
        request_user = self.context.get("request").user

        if product.user == request_user:
            raise serializers.ValidationError("You cannot order your own product")
        
        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError("Quantity must not be zero(0)")
        
        if product.stock <= 0:
            raise serializers.ValidationError("This product is out of stock")
        
        if quantity is not None and quantity > product.stock:
            raise serializers.ValidationError(f"Quantity exceeds the stock product. {product.stock} is available on product stock")
        
        return data
    
    def create(self, validated_data):
        request_user = self.context.get("request").user
        product = self.context.get('product')
        quantity = validated_data.get("quantity")

        order = Order.objects.create(
            user=request_user,
            product=product,
            quantity=quantity
        )
        product.stock -= quantity
        product.save()
        return order

    
        