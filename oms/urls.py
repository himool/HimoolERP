"""oms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import ccccc, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from . import views


urlpatterns = [
    re_path('user/', include('user.urls')),

    path('api/', include('account.urls')),
    path('api/', include('goods.urls')),
    path('api/', include('warehouse.urls')),
    path('api/', include('purchase.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('report.urls')),

    re_path('^.*$', views.index),
]
