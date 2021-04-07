from decimal import Decimal

import pytest
from django.urls import reverse
from model_bakery import baker

from core.models import Wallet, Symbol


@pytest.mark.django_db
def test_deposit(client):
    wallet: Wallet = baker.make("core.Wallet", balance=Decimal(5))
    old_balance = wallet.balance
    client.force_login(wallet.user)
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


@pytest.mark.django_db
def test_get_balance(client):
    wallet: Wallet = baker.make("core.Wallet", balance=Decimal(5))

    client.force_login(wallet.user)
    response = client.get(
        reverse("wallet-detail", args=[wallet.currency]),
        format="json",
    )

    assert response.status_code == 200, response.rendered_content
    assert Decimal(response.data["balance"]) == Decimal(5)

    assert response.data == {
        "id": wallet.pk,
        "user": wallet.user.pk,
        "balance": "5.00000000",
    }


@pytest.mark.django_db
def test_order(client):
    wallet: Wallet = baker.make("core.Wallet", balance=Decimal(100))
    msft: Symbol = baker.make("core.Symbol", ticker="MSFT")

    request_data = {
        "symbol": msft.ticker,
        "side": "BUY",
        "quantity": "1",
        "price": "100",
    }

    client.force_login(wallet.user)
    response = client.post(
        reverse("order-list"),
        request_data,
        format="json",
    )

    assert response.status_code == 201, response.rendered_content

    expected = {
        "symbol": msft.ticker,
        "side": "BUY",
        "quantity": "1.00000000",
        "price": "100.00000000",
    }

    assert expected == {k: v for k, v in response.data.items() if k in expected}
