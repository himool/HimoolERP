from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('roles/<int:pk>/', views.RoleViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('subusers/', views.SubusertViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('subusers/<str:pk>/', views.SubusertViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('accounts/', views.AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('accounts/<str:pk>/', views.AccountViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('sellers/', views.SellerViewSet.as_view({'get': 'list'})),
    path('bookkeeping/', views.BookkeepingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('bookkeeping/<str:pk>/', views.BookkeepingViewSet.as_view({'delete': 'destroy'})),
    path('statistical_account/', views.StatisticalAccountViewSet.as_view({'get': 'list'})),
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
]
