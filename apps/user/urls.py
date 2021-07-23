from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('get_info/', views.get_info),
    path('configs/', views.ConfigViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    # path('set_password/', views.set_password),
]
