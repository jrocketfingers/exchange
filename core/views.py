from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action

from core.models import Wallet
from core.serializers import WalletSerializer


class Wallet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        deposit_amount = serializer.data["amount"]
        asset_name = serializer.data["asset_name"]
        Wallet.objects.filter(pk=pk).update(balance=F("balance") + deposit_amount)
