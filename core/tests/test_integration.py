import pytest
from django.urls import reverse

from model_mommy import mommy

from core.models import Wallet


@pytest.mark.django_db
def test_deposit(client):
    wallet = mommy.make(Wallet)
    old_balance = wallet.balance
    user = wallet.user
    client.force_login(user)
    client.post(
        reverse("deposit"),
        {
            "amount": 10,
            "asset": wallet.asset,
        }
    )

    wallet.reload()

    assert wallet.balance == old_balance + 10
