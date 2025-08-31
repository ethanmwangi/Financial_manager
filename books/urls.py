from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListCreateView


urlpatterns = [

    path('books/', BookListCreateView.as_view(), name='book-list-create'),
]
