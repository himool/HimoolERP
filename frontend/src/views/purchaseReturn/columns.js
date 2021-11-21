import NP from 'number-precision';

export const purchaseColumns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    scopedSlots: { customRender: 'index' },
  },
  {
    title: '编号',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '商品',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '规格',
    dataIndex: 'spec',
    key: 'spec',
  },
  {
    title: '单位',
    dataIndex: 'unit',
    key: 'unit',
  },
  {
    title: '数量',
    dataIndex: 'quantity',
    key: 'quantity',
  },
  {
    title: '单价',
    dataIndex: 'purchase_price',
    key: 'purchase_price',
  },
  {
    title: '金额(元)',
    dataIndex: 'amount',
    key: 'amount',
    customRender: (value) => {
      return NP.round(value, 2)
    },
  },
]

export const returnColumns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
  },
  {
    title: '编号',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '商品',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '规格',
    dataIndex: 'spec',
    key: 'spec',
  },
  {
    title: '单位',
    dataIndex: 'unit',
    key: 'unit',
  },
  {
    title: '数量',
    dataIndex: 'quantity',
    key: 'quantity',
    scopedSlots: { customRender: 'quantity' },
  },
  {
    title: '单价(元)',
    dataIndex: 'purchase_price',
    key: 'purchase_price',
    scopedSlots: { customRender: 'purchase_price' },
  },
  {
    title: '金额',
    dataIndex: 'amount',
    key: 'amount',
    customRender: (value, item) => {
      if (item.isTotal) return value;
      value = NP.times(item.quantity, item.purchase_price);
      return item.id ? NP.round(value, 2) : ''
    },
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]