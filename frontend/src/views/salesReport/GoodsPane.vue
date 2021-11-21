<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
      <div slot="avg_retail_price" slot-scope="value">{{NP.round(value, 2)}}</div>
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
            title: '编号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '名称',
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
            title: '分类',
            dataIndex: 'category_name',
            key: 'category_name',
          },
          {
            title: '销量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '最低售价',
            dataIndex: 'min_retail_price',
            key: 'min_retail_price',
          },
          {
            title: '最高售价',
            dataIndex: 'max_retail_price',
            key: 'max_retail_price',
          },
          {
            title: '平均售价',
            dataIndex: 'avg_retail_price',
            key: 'avg_retail_price',
            scopedSlots: { customRender: 'avg_retail_price' },
          },
        ],
      };
    },
  }
</script>