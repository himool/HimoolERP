export default {
  path: '/finance',
  name: 'finance',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/finance/warehouse_dict',
  children: [
    {
      path: 'payment_record',
      meta: { title: '打款记录', permission: 'payment_record' },
      component: () => import('@/views/finance/paymentRecord/index'),
    },
    {
      path: 'purchase_statement',
      meta: { title: '采购对账单', permission: 'purchase_statement' },
      component: () => import('@/views/finance/purchaseStatement/index'),
    },
    {
      path: 'transaction_record',
      meta: { title: '往来记录', permission: 'transaction_record' },
      component: () => import('@/views/finance/transactionRecord/index'),
    },
    {
      path: 'sales_statement',
      meta: { title: '销售对账单', permission: 'sales_statement' },
      component: () => import('@/views/finance/salesStatement/index'),
    },
  ],
}