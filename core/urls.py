from rest_framework import routers

from core import views


router = routers.SimpleRouter()

router.register("/wallet", views.WalletViewSet, "wallet")
router.register("/order", views.OrderViewSet, "order")

urlpatterns = router.urls
