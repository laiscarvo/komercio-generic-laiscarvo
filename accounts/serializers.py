from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:

        model = Account

        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = [
            "is_active",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(), message="username alredy exists"
                    )
                ]
            },
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountUpdatedSerializer(serializers.ModelSerializer):
    class Meta:

        model = Account

        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = [
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(), message="username alredy exists"
                    )
                ]
            },
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
