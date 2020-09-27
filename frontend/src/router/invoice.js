export default {
  path: '/invoice',
  name: 'invoice',
  component: () => import('@/layouts/InvoiceLayout'),
  children: [
    {
      path: 'purchase',
      name: 'purchase',
      meta: { title: '采购单' },
      component: () => import('@/views/purchaseInvoice/PurchaseInvoice'),
    },
    {
      path: 'sales',
      name: 'sales',
      meta: { title: '销售单' },
      component: () => import('@/views/salesInvoice/SalesInvoice'),
    },
    {
      path: 'requisition',
      name: 'requisition',
      meta: { title: '调拨单' },
      component: () => import('@/views/requisitionInvoice/RequisitionInvoice'),
    },
    {
      path: 'counting_list',
      name: 'counting_list',
      meta: { title: '盘点单' },
      component: () => import('@/views/countingListInvoice/CountingListInvoice'),
    },
  ]
}
