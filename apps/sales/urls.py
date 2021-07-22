from django.urls import path
from . import views

urlpatterns = [
    path('sales_order/confirm/', views.SalesOrderViewSet.as_view({'post': 'confirm'})),
    path('sales_order/payment/', views.SalesOrderViewSet.as_view({'post': 'payment'})),
    path('sales_order/', views.SalesOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sales_order/<str:pk>/', views.SalesOrderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('sales_tasks/', views.SalesTaskViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sales_order_profit/total_profit/', views.SalesOrderProfitViewSet.as_view({'get': 'total_profit'})),
    path('sales_order_profit/', views.SalesOrderProfitViewSet.as_view({'get': 'list'})),
    path('sales_order_profit/<int:pk>/', views.SalesOrderProfitViewSet.as_view({'put': 'update'})),
    path('sales_values/', views.SalesValueViewSet.as_view({'get': 'list'})),
    path('sales_top_ten/', views.SalesTopTenViewSet.as_view({'get': 'list'})),
    path('clients/', views.ClientViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('clients/<str:pk>/', views.ClientViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('sales_payment_records/', views.SalesPaymentRecordViewSet.as_view({'get': 'list'})),
]
