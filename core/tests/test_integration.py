from decimal import Decimal

import pytest
from django.urls import reverse
from model_bakery import baker

from core.models import Wallet


@pytest.mark.django_db
def test_deposit(client):
    wallet: Wallet = baker.make("core.Wallet", balance=Decimal(5))
    old_balance = wallet.balance
    user = wallet.user
    client.force_login(user)
    response = client.post(
        reverse("wallet-deposit", args=[wallet.id]),
        {
            "amount": 10,
        },
        format="json",
    )

    assert response.status_code == 200, response.rendered_content

    wallet.refresh_from_db()

    assert wallet.balance == old_balance + 10
