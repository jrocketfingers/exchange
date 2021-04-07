from decimal import Decimal
from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Wallet, Order
from core.serializers import WalletSerializer, DepositSerializer, OrderSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "currency"

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        request_serializer = DepositSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        deposit_amount: Decimal = request_serializer.data["amount"]

        wallet = Wallet.objects.get(pk=pk)
        wallet.balance = F("balance") + Decimal(deposit_amount)
        wallet.save()

        # serializer = self.get_serializer(wallet)
        return Response(request_serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "symbol"
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data={**request.data, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
