from apps.system.models import PermissionGroup, Permission


PERMISSIONS = [
    {
        'name': '报表统计',
        'permissions': [
            {'name': '销售报表', 'code': 'warehouse_inventory'},
            {'name': '采购报表', 'code': 'warehouse_inventory'},
            {'name': '库存报表', 'code': 'warehouse_inventory'},
            {'name': '收支统计', 'code': 'warehouse_inventory'},
            {'name': '库存报表', 'code': 'warehouse_inventory'},
        ],
    },
]


def run(*args):
    PermissionGroup.objects.all().delete()

    for permission_group_item in PERMISSIONS:
        permission_group = PermissionGroup.objects.create(name=permission_group_item['name'])
        Permission.objects.bulk_create([Permission(group=permission_group, name=item['name'], code=item['code'])
                                        for item in permission_group_item['permissions']])
