<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
      <div slot="avg_purchase_price" slot-scope="value">{{NP.round(value, 2)}}</div>
    </a-table>
  </div>
</template>

<script>
  import NP from 'number-precision'

  export default {
    name: 'GoodsPane',
    props: ['items', 'loading'],
    data() {
      return {
        NP,
        columns: [
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '名称',
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
            title: '分类',
            dataIndex: 'category_name',
            key: 'category_name',
          },
          {
            title: '采购量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '最低进价',
            dataIndex: 'min_purchase_price',
            key: 'min_purchase_price',
          },
          {
            title: '最高进价',
            dataIndex: 'max_purchase_price',
            key: 'max_purchase_price',
          },
          {
            title: '平均进价',
            dataIndex: 'avg_purchase_price',
            key: 'avg_purchase_price',
            scopedSlots: { customRender: 'avg_purchase_price' },
          },
        ],
      };
    },
  }
</script>