import NP from 'number-precision';

export const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
  },
  {
    title: '货号',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '商品',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '规格型号',
    dataIndex: 'specification',
    key: 'specification',
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
    title: '单价',
    dataIndex: 'purchase_price',
    key: 'purchase_price',
    scopedSlots: { customRender: 'purchase_price' },
  },
  {
    title: '折扣(%)',
    dataIndex: 'discount',
    key: 'discount',
    scopedSlots: { customRender: 'discount' },
  },

  {
    title: '折后价',
    dataIndex: 'discount_price',
    key: 'discount_price',
    customRender: (value, item) => {
      value = NP.times(item.purchase_price, item.discount, 0.01);
      return item.id ? NP.round(value, 2) : ''
    },
  },
  {
    title: '金额',
    dataIndex: 'amount',
    key: 'amount',
    customRender: (value, item) => {
      value = NP.times(item.quantity, item.purchase_price);
      return item.id ? NP.round(NP.times(item.quantity, item.purchase_price), 2) : ''
    },
  },
  {
    title: '折后金额',
    dataIndex: 'discount_amount',
    key: 'discount_amount',
    customRender: (value, item) => {
      value = NP.times(item.quantity, item.purchase_price, item.discount, 0.01);
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