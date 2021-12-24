export default {
  path: '/delivery',
  name: 'delivery',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/delivery/packing_list',
  children: [
    {
      path: 'packing_list',
      meta: { title: '装箱清单', permission: 'packing_list' },
      component: () => import('@/views/delivery/packingList/index'),
    },
    {
      path: 'packing_create',
      meta: { title: '装箱清单新增', permission: 'packing_create' },
      component: () => import('@/views/delivery/packingCreate/index'),
    },
    {
      path: 'packing_edit',
      meta: { title: '装箱清单编辑', permission: 'packing_edit' },
      component: () => import('@/views/delivery/packingEdit/index'),
    },
    {
      path: 'packing_detail',
      meta: { title: '装箱清单详情', permission: 'packing_detail' },
      component: () => import('@/views/delivery/packingDetail/index'),
    }
  ],
}