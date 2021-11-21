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
    title: '客户',
    dataIndex: 'client_name',
    key: 'client_name',
  },
  {
    title: '选择',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]