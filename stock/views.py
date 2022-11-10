from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from .models import Stock
from .serializers import StockModelSerializer, StockCreateSerializer

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



