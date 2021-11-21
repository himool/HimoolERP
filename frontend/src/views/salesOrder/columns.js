import NP from 'number-precision';

export const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
  },
  {
    title: '商品名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '商品编号',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '规格',
    dataIndex: 'spec',
    key: 'spec',
  },
  {
    title: '数量',
    dataIndex: 'quantity',
    key: 'quantity',
    scopedSlots: { customRender: 'quantity' },
  },
  {
    title: '单位',
    dataIndex: 'unit',
    key: 'unit',
  },
  {
    title: '单价(元)',
    dataIndex: 'retail_price',
    key: 'retail_price',
    scopedSlots: { customRender: 'retail_price' },
  },
  {
    title: '金额(元)',
    dataIndex: 'amount',
    key: 'amount',
    customRender: (value, item) => {
      if (item.isTotal) return value;
      value = NP.times(item.quantity, item.retail_price);
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