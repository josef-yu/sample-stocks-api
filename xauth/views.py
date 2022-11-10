from rest_framework import generics, permissions, status
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer

class RegisterUserView(generics.CreateAPIView):
    """
    Use this endpoint to register new user
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



