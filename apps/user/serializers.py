from rest_framework import serializers
from .models import Teams


class ConfigSerializer(serializers.ModelSerializer):
    """配置"""

    class Meta:
        model = Teams
        fields = ['auto_stock_in', 'auto_stock_out']
