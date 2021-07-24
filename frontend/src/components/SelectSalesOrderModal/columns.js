export const columns = [
  {
    title: '名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '货号',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '选择',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]