export default [
  {
    title: '商品编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '商品名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '商品单位',
    dataIndex: 'unit_name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]