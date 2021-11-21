export const columns = [
  {
    title: '单号',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: '日期',
    dataIndex: 'date',
    key: 'date',
  },
  {
    title: '仓库',
    dataIndex: 'warehouse_name',
    key: 'warehouse_name',
  },
  {
    title: '供应商',
    dataIndex: 'supplier_name',
    key: 'supplier_name',
  },
  {
    title: '选择',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]