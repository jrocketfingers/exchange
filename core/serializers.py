from rest_framework import serializers

from core.models import Wallet, User, Order, Symbol


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance", "user"]


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=21, decimal_places=8)

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be less than 0")

        return value


class OrderSerializer(serializers.ModelSerializer):
    symbol = serializers.SlugRelatedField(
        slug_field="ticker", queryset=Symbol.objects.all()
    )

    class Meta:
        model = Order
        fields = ["id", "symbol", "user", "quantity", "price", "side"]
