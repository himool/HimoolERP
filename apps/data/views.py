from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.data.serializers import *
from apps.data.permissions import *
from apps.data.filters import *
from apps.data.schemas import *
from apps.data.models import *
from apps.goods.models import *


class WarehouseViewSet(ModelViewSet, DataProtectMixin, ExportMixin, ImportMixin):
    """仓库"""

    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['manager', 'is_active', 'is_locked']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'number']
    select_related_fields = ['manager']
    queryset = Warehouse.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        warehouse = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for goods in Goods.objects.filter(team=self.team)])

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Warehouse.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'])
    def lock(self, request, *args, **kwargs):
        """锁定仓库"""

        warehouse = self.get_object()
        warehouse.is_locked = False
        warehouse.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=warehouse)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'])
    def unlock(self, request, *args, **kwargs):
        """解锁仓库"""

        warehouse = self.get_object()
        warehouse.is_locked = True
        warehouse.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=warehouse)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(WarehouseExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(WarehouseImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: WarehouseSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        warehouses = []
        for import_serializer in self.load_data(validated_data['file'], WarehouseImportSerializer):
            validated_data = import_serializer.validated_data
            if warehouse := Warehouse.objects.filter(name=validated_data['name'],
                                                     team=self.team).first():
                serializer = WarehouseSerializer(instance=warehouse, data=validated_data,
                                                 context=self.context)
            else:
                serializer = WarehouseSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            warehouse = serializer.save()
            warehouses.append(warehouse)

        serializer = WarehouseSerializer(instance=warehouses, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ClientViewSet(ModelViewSet, DataProtectMixin, ExportMixin, ImportMixin):
    """客户"""

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    filterset_fields = ['level', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    queryset = Client.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Client.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(ClientExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(ClientImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: ClientSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        clients = []
        for import_serializer in self.load_data(validated_data['file'], ClientImportSerializer):
            validated_data = import_serializer.validated_data
            if client := Client.objects.filter(name=validated_data['name'],
                                               team=self.team).first():
                serializer = ClientSerializer(instance=client, data=validated_data,
                                              context=self.context)
            else:
                serializer = ClientSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            client = serializer.save()
            clients.append(client)

        serializer = ClientSerializer(instance=clients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SupplierViewSet(ModelViewSet, DataProtectMixin, ExportMixin, ImportMixin):
    """供应商"""

    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermission]
    filterset_fields = ['is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    queryset = Supplier.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Supplier.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(SupplierExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(SupplierImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: SupplierSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        suppliers = []
        for import_serializer in self.load_data(validated_data['file'], SupplierImportSerializer):
            validated_data = import_serializer.validated_data
            if supplier := Supplier.objects.filter(name=validated_data['name'],
                                                   team=self.team).first():
                serializer = SupplierSerializer(instance=supplier, data=validated_data,
                                                context=self.context)
            else:
                serializer = SupplierSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            supplier = serializer.save()
            suppliers.append(supplier)

        serializer = SupplierSerializer(instance=suppliers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccountViewSet(ModelViewSet, DataProtectMixin, ExportMixin, ImportMixin):
    """结算账户"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]
    filterset_fields = ['type', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    queryset = Account.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Account.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(AccountExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(AccountImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: AccountSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        accounts = []
        for import_serializer in self.load_data(validated_data['file'], AccountImportSerializer):
            validated_data = import_serializer.validated_data
            if account := Account.objects.filter(name=validated_data['name'],
                                                 team=self.team).first():
                serializer = AccountSerializer(instance=account, data=validated_data,
                                               context=self.context)
            else:
                serializer = AccountSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            accounts.append(account)

        serializer = AccountSerializer(instance=accounts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChargeItemViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """收支项目"""

    serializer_class = ChargeItemSerializer
    permission_classes = [IsAuthenticated, ChargeItemPermission]
    filterset_fields = ['type']
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ChargeItem.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(ChargeItemExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(ChargeItemImportSerializer)

    @extend_schema(request=UploadRequest, responses={200: ChargeItemSerializer(many=True)})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        charge_items = []
        for import_serializer in self.load_data(validated_data['file'], ChargeItemImportSerializer):
            validated_data = import_serializer.validated_data
            if charge_item := ChargeItem.objects.filter(name=validated_data['name'],
                                                        team=self.team).first():
                serializer = ChargeItemSerializer(instance=charge_item, data=validated_data,
                                                  context=self.context)
            else:
                serializer = ChargeItemSerializer(data=validated_data, context=self.context)

            serializer.is_valid(raise_exception=True)
            charge_item = serializer.save()
            charge_items.append(charge_item)

        serializer = ChargeItemSerializer(instance=charge_items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'WarehouseViewSet', 'ClientViewSet', 'SupplierViewSet',
    'AccountViewSet', 'ChargeItemViewSet',
]
