from rest_framework import routers

from core import views


router = routers.SimpleRouter()

router.register("/wallet", views.WalletViewSet, "wallet")

urlpatterns = router.urls
