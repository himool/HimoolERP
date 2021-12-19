from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.goods.serializers import *
from apps.goods.permissions import *
from apps.goods.filters import *
from apps.goods.schemas import *
from apps.goods.models import *
from apps.data.models import *


class GoodsCategoryViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """商品分类"""

    serializer_class = GoodsCategorySerializer
    permission_classes = [IsAuthenticated, GoodsCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsCategory.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(GoodsCategoryExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(GoodsCategoryImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: GoodsCategorySerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        goods_categories = []
        for import_serializer in self.load_data(validated_data['file'], GoodsCategoryImportSerializer):
            validated_data = import_serializer.validated_data
            if goods_category := GoodsCategory.objects.filter(name=validated_data['name'],
                                                              team=self.team).first():
                serializer = GoodsCategorySerializer(instance=goods_category, data=validated_data,
                                                     context=self.context)
            else:
                serializer = GoodsCategorySerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            goods_category = serializer.save()
            goods_categories.append(goods_category)

        serializer = GoodsCategorySerializer(instance=goods_categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GoodsUnitViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """商品单位"""

    serializer_class = GoodsUnitSerializer
    permission_classes = [IsAuthenticated, GoodsUnitPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsUnit.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(GoodsUnitExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(GoodsUnitImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: GoodsUnitSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        goods_units = []
        for import_serializer in self.load_data(validated_data['file'], GoodsUnitImportSerializer):
            validated_data = import_serializer.validated_data
            if goods_unit := GoodsUnit.objects.filter(name=validated_data['name'],
                                                      team=self.team).first():
                serializer = GoodsUnitSerializer(instance=goods_unit, data=validated_data,
                                                 context=self.context)
            else:
                serializer = GoodsUnitSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            goods_unit = serializer.save()
            goods_units.append(goods_unit)

        serializer = GoodsUnitSerializer(instance=goods_units, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GoodsViewSet(ModelViewSet, DataProtectMixin, ExportMixin, ImportMixin):
    """商品"""

    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, GoodsPermission]
    filterset_fields = ['number', 'category', 'is_active']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category', 'unit']
    prefetch_related_fields = ['inventories', 'inventories__batchs']
    queryset = Goods.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Goods.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


class GoodsImageViewSet(ModelViewSet):
    """商品图片"""

    serializer_class = GoodsImageSerializer
    permission_classes = [IsAuthenticated, GoodsPermission]
    search_fields = ['name']
    queryset = GoodsImage.objects.all()


class BatchViewSet(BaseViewSet, ReadOnlyMixin):
    """批次"""

    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated, BatchPermission]
    filterset_fields = ['number', 'warehouse', 'goods', 'has_stock']
    search_fields = ['number', 'goods__number', 'goods__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'production_date',
                       'expiration_date', 'create_time']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Batch.objects.all()


class InventoryViewSet(BaseViewSet, ReadOnlyMixin):
    """库存"""

    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission]
    filterset_fields = ['warehouse', 'goods', 'has_stock']
    search_fields = ['goods__number', 'goods__name']
    ordering_fields = ['id', 'total_quantity']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Inventory.objects.all()


__all__ = [
    'GoodsCategoryViewSet', 'GoodsUnitViewSet', 'GoodsViewSet', 'GoodsImageViewSet',
    'BatchViewSet', 'InventoryViewSet',
]
