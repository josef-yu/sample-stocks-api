from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('order', views.OrderCreateView.as_view(), name='place-order'),
    path('portfolio', views.PortfolioReadView.as_view(), name='view-portfolio')
]

router = DefaultRouter()

router.register(r'', views.StockViewSet, basename='stock')


urlpatterns += router.urls