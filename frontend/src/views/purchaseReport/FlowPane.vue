<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
      <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      <div slot="relation_order" slot-scope="value">
        <a-button type="link" @click="openInvoice(value)">查看</a-button>
      </div>
    </a-table>
  </div>
</template>

<script>
  import moment from 'moment'

  export default {
    name: 'FlowPane',
    props: ['items', 'loading'],
    data() {
      return {
        moment,
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
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '供应商',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
          {
            title: '公司',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '关联单',
            dataIndex: 'relation_order',
            key: 'relation_order',
            scopedSlots: { customRender: 'relation_order' },
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
        ],
      };
    },
    methods: {
      openInvoice(id) {
        window.open(`/invoice/purchase?id=${id}`);
      },
    },
  }
</script>