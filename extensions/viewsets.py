from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from extensions.paginations import BasePagination, OptionPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Value, F, Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from extensions.exceptions import ValidationError
from django.db.models.functions import Coalesce
from drf_spectacular.types import OpenApiTypes
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from openpyxl import Workbook, load_workbook
from rest_framework.viewsets import ViewSet
from django.db import transaction
from rest_framework import status
from django.conf import settings
from number_precision import NP
import pendulum
import re


class ActionViewSet(ViewSet):

    @property
    def team(self):
        return self.request.user.team

    @property
    def user(self):
        return self.request.user


class BaseViewSet(GenericViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['id']
    ordering = ['-id']
    select_related_fields = []
    prefetch_related_fields = []

    @property
    def team(self):
        return self.request.user.team

    @property
    def user(self):
        return self.request.user

    @property
    def context(self):
        return self.get_serializer_context()

    def get_queryset(self):
        queryset = super().get_queryset().filter(team=self.team)
        queryset = queryset.select_related(*self.select_related_fields)
        queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset


class OptionViewSet(BaseViewSet, ListModelMixin):
    """选项"""

    pagination_class = OptionPagination


class ReadOnlyMixin(RetrieveModelMixin, ListModelMixin):
    """只读"""


class ReadWriteMixin(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    """读写"""


class ExportMixin:
    """导出"""

    def get_export_response(self, serializer_class, data=None):
        """获取导出Excel文件响应

        Args:
            serializer_class (BaseSerializer): 序列化类
            data (list): 数据

            serializer (BaseSerializer): 序列化器
            field_items (List): 字段属性

        Returns:
            HttpResponse: 文件响应
        """

        workbook = Workbook()
        work_sheet = workbook.active

        if data:
            results = data
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = serializer_class(instance=queryset, many=True)
            results = serializer.data
        field_items = serializer_class().get_fields().items()

        # 创建表头
        work_sheet.cell(row=1, column=1, value='序号')
        for index, (field_name, field_class) in enumerate(field_items, start=2):
            work_sheet.cell(row=1, column=index, value=field_class.label)

        # 填充数据
        for row, item in enumerate(results, start=2):
            work_sheet.cell(row=row, column=1, value=row - 1)

            for column, (field_name, field_class) in enumerate(field_items, start=2):
                work_sheet.cell(row=row, column=column, value=item.get(field_name, ''))

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=data.xlsx'
        workbook.save(response)

        return response


class ImportMixin:
    """导入"""

    def get_template_response(self, serializer_class):
        """获取Excel模板响应

        Args:
            serializer_class (BaseSerializer): 序列化类

        Returns:
            HttpResponse: 文件响应
        """

        workbook = Workbook()
        work_sheet = workbook.active

        # 创建表头
        field_items = serializer_class().get_fields().items()
        for index, (_, field_class) in enumerate(field_items, start=1):
            work_sheet.cell(row=1, column=index, value=field_class.label)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=data.xlsx'
        workbook.save(response)

        return response

    def load_data(self, file, serializer_class):
        workbook = load_workbook(file)
        work_sheet = workbook.active

        field_items = serializer_class().get_fields().items()
        for row in range(2, work_sheet.max_row + 1):
            data = {}

            for column, (field_name, field_class) in enumerate(field_items):
                if work_sheet[1][column].value != field_class.label:
                    raise ValidationError('格式错误')

                if work_sheet[row][column].value is not None:
                    data[field_name] = work_sheet[row][column].value

            else:
                serializer = serializer_class(data=data, context=self.context)
                serializer.is_valid(raise_exception=True)
                yield serializer


__all__ = [
    'GenericViewSet', 'ViewSet', 'ActionViewSet', 'BaseViewSet', 'OptionViewSet',
    'ListModelMixin', 'RetrieveModelMixin', 'CreateModelMixin', 'UpdateModelMixin', 'DestroyModelMixin',
    'ReadOnlyMixin', 'ReadWriteMixin', 'ExportMixin', 'ImportMixin',
    'action', 'transaction', 'status', 'Response', 'pendulum', 'NP', 'settings', 're',
    'Sum', 'Count', 'Value', 'F', 'Q', 'Prefetch', 'Coalesce',
    'extend_schema', 'OpenApiParameter', 'OpenApiResponse', 'OpenApiTypes',
]
