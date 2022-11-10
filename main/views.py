from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SwaggerSchemaView = get_schema_view(
   openapi.Info(
      title="Stocks API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="test@email.com"),
      license=openapi.License(name="Sample License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

