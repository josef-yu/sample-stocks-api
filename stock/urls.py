from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()

router.register(r'', views.StockViewSet, basename='stock')

urlpatterns += router.urls