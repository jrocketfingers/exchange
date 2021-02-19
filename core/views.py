from decimal import Decimal
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Wallet
from core.serializers import WalletSerializer, DepositSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

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
