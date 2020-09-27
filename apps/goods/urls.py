from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('goods/', views.GoodsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('goods/<int:pk>/', views.GoodsViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]
