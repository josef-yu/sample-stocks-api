from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls.authtoken')),
    path('register', views.RegisterUserView.as_view(), name='register')
]