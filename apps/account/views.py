from .serializers import RoleSerializer, SubuserSerializer, AccountSerializer, BookkeepingSerializer
from .paginations import BookkeepingPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import RolePermission, SubuserPermission
from rest_framework import permissions, pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, exceptions
from utils.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Sum, Value
from django.contrib import auth
from user.models import User
from .models import Role
import pendulum
from django.db.models.functions import Coalesce


class RoleViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, RolePermission]

    def get_queryset(self):
        return self.request.user.teams.roles.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)


class SubusertViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = SubuserSerializer
    permission_classes = [IsAuthenticated, SubuserPermission]

    def get_queryset(self):
        return self.request.user.teams.users.filter(is_boss=False, is_delete=False).order_by('create_date')

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        username = self.request.data.get('username')
        roles = self.request.data.get('roles', [])

        if password is None:
            raise exceptions.ValidationError

        if User.objects.filter(username=username).first():
            raise exceptions.ValidationError({'message': '账号已存在'})

        serializer.save(teams=self.request.user.teams, is_boss=False, password=password, roles=roles)

    def perform_update(self, serializer):
        username = self.request.data.get('username')
        roles = self.request.data.get('roles', [])

        if serializer.instance.username != username and User.objects.filter(username=username).first():
            raise exceptions.ValidationError({'message': '账号已存在'})

        serializer.instance.roles.set(roles)
        serializer.save()

    def partial_update(self, request, *args, **kwargs):  # 重置密码
        password = self.request.data.get('password')
        if password is None:
            raise exceptions.ValidationError

        instance = self.get_object()
        instance.set_password(password)
        instance.save()
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class AccountViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name', 'order']

    def get_queryset(self):
        return self.request.user.teams.accounts.filter(is_delete=False).order_by('order')

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class SellerViewSet(viewsets.ModelViewSet):
    """list"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = request.user.teams.users.filter(is_delete=False)
        roles = request.user.roles.all()
        if not roles:  # 没有设置角色默认拥有全部权限
            return Response(queryset.values('id', 'username'))

        for role in roles:
            if 'CHANGE_SELLER' in role.permissions:
                return Response(queryset.values('id', 'username'))

        return Response([{'id': request.user.id, 'username': request.user.username}])


class BookkeepingViewSet(viewsets.ModelViewSet):
    """list, create, destroy"""
    serializer_class = BookkeepingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookkeepingPagination

    def get_queryset(self):
        return self.request.user.teams.bookkeeping_set.all().order_by('-create_datetime')

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams, recorder=self.request.user)


class StatisticalAccountViewSet(viewsets.ModelViewSet):
    """list"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accoutns = self.request.query_params.get('accounts')
        accoutns = accoutns.split(',') if accoutns else []
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        end_date = pendulum.parse(end_date).add(days=1)

        bookkeeping_queryset = self.request.user.teams.bookkeeping_set.filter(
            account_id__in=accoutns)
        purchase_queryset = self.request.user.teams.purchase_order_set.filter(
            account_id__in=accoutns, is_return=False)
        sales_queryset = self.request.user.teams.sales_order_set.filter(
            account_id__in=accoutns, is_return=False)

        if start_date:
            bookkeeping_queryset = bookkeeping_queryset.filter(create_datetime__gte=start_date)
            purchase_queryset = purchase_queryset.filter(date__gte=start_date)
            sales_queryset = sales_queryset.filter(date__gte=start_date)

        if end_date:
            bookkeeping_queryset = bookkeeping_queryset.filter(create_datetime__lte=end_date)
            purchase_queryset = purchase_queryset.filter(date__lte=end_date)
            sales_queryset = sales_queryset.filter(date__lte=end_date)

        return bookkeeping_queryset, purchase_queryset, sales_queryset

    def list(self, request, *args, **kwargs):
        bookkeeping_queryset, purchase_queryset, sales_queryset = self.get_queryset()

        amount_list = bookkeeping_queryset.values_list('amount', flat=True)
        expenditure = purchase_queryset.aggregate(amount=Coalesce(Sum('amount'), Value(0)))['amount']
        revenue = sales_queryset.aggregate(amount=Coalesce(Sum('amount'), Value(0)))['amount']

        for amount in amount_list:
            if amount > 0:
                revenue += amount
            else:
                expenditure -= amount

        return Response({'revenue': revenue, 'expenditure': expenditure})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        results = request.user.teams.users.filter(is_delete=False).values('id', 'username')
        return Response(data=results)
