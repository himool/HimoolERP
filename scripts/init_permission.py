from apps.system.models import PermissionType, Permission


PERMISSIONS = [
    {
        'name': '数据报表',
        'permissions': [
            {'name': '库存报表', 'code': 'warehouse_inventory'},
        ],
    },
]


def run(*args):
    PermissionType.objects.all().delete()

    for permission_type_item in PERMISSIONS:
        permission_type = PermissionType.objects.create(name=permission_type_item['name'])
        Permission.objects.bulk_create([Permission(type=permission_type, name=item['name'], code=item['code'])
                                        for item in permission_type_item['permissions']])
