from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, me_view, logout_view, CalendarEventViewSet, PettyCashViewSet, BillViewSet, SaleViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from api.views import LoginView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'calendar-events', CalendarEventViewSet, basename='calendar-event')
router.register(r'petty-cash', PettyCashViewSet, basename='petty-cash')
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'sales', SaleViewSet, basename='sale')


urlpatterns = router.urls

urlpatterns += [
    path("me/", me_view, name="me"),
    path("logout/", logout_view, name="logout"),
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]