from django.db import transaction
from django.db.models import F, Sum
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response

from .models import Stock, OrderItem
from .serializers import (
    StockModelSerializer, 
    StockCreateSerializer,
    OrderCreateSerializer,
    PortfolioReadSerializer
)

# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    """
    list: Use this endpoint to retrieve list of stocks.

    create: Use this endpoint to create a new stock.

    retrieve: Use this endpoint to retrieve list of stocks with specified ID.

    update: Use this endpoint to update stock information.

    partial_update: Use this endpoint to partially update a stock.

    destroy: Use this endpoint to delete a stock.
    """
    queryset = Stock.objects.all()
    
    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated] 
        if not self.action in ('list', 'retrieve'):
            permission_classes.append(permissions.IsAdminUser)
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Swagger passes request=None. Return create serializer because
        GET requests don't have request body fields.
        See get_serializer_fields()
        """
        if self.request is None:
            return StockCreateSerializer

        if self.request.method == 'POST':
            return StockCreateSerializer
        else:
            return StockModelSerializer


class OrderCreateView(generics.GenericAPIView):
    """
    post: Use this endpoint to place an order of stock(s)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer

    @transaction.atomic()
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(
            {'order_id': order.id, 'total_price': order.total_price}, 
            status=status.HTTP_201_CREATED
        )

class PortfolioReadView(generics.GenericAPIView):
    """
    get: Use this endpoint to get user's portfolio information
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioReadSerializer


    def _aggregate(self, queryset):
        return queryset\
            .aggregate(
                Sum('stock__price', default=0),
                Sum('price', default=0)
            )
    
    def _get_stocks(self, queryset):
        return queryset\
            .values(
                'quantity',
                'stock_id',
                stock_name=F('stock__name'),
                current_price=F('stock__price'),
            )
    
    def get_queryset(self):
        base_queryset = OrderItem.objects\
            .select_related('order')\
            .select_related('stock')\
            .filter(order__user=self.request.user)

        aggregate_queryset = self._aggregate(base_queryset)

        total_value = aggregate_queryset\
            .get('stock__price__sum')

        bought_value = aggregate_queryset\
            .get('price__sum')

        items = self._get_stocks(base_queryset)

        return {
            'total_current_value': total_value,
            'bought_value': bought_value,
            'stocks': items
        }
    
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)

        return Response(serializer.data)



