from rest_framework import serializers

from accounts.serializers import AccountSerializer
from .models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:

        model = Product

        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]
        read_only_fields = ["is_active"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:

        model = Product

        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
        read_only_fields = ["is_active", "seller_id"]
