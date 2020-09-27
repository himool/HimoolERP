from django.urls import path
from . import views

urlpatterns = [
    path('supplier/', views.SupplierViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('supplier/<int:pk>/', views.SupplierViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('purchase_order/confirm/', views.PurchaseOrderViewSet.as_view({'post': 'confirm'})),
    path('purchase_order/payment/', views.PurchaseOrderViewSet.as_view({'post': 'payment'})),
    path('purchase_order/', views.PurchaseOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('purchase_order/<str:pk>/', views.PurchaseOrderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('change_records/', views.ChangeRecordViewSet.as_view({'get': 'list'})),
    path('purchase_payment_records/', views.PurchasePaymentRecordViewSet.as_view({'get': 'list'})),
]
