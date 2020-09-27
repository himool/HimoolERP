<template>
  <div>
    <a-card title="订单收款明细" hoverable style="height: calc(50vh - 64px);">
      <a-table :columns="columns" :data-source="items" :loading="loading" :pagination="false" size="small"
        @change="changeOrder" :scroll="{x: 800,y: tableHeight}">
        <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      </a-table>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesPaymentRecord } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'SalesDetail',
    data() {
      return {
        moment,
        searchForm: { page: 1, is_return: false, ordering: '-date' },
        totalRows: 0,
        perPage: 10,
        loading: false,
        items: [],
        columns: [
          {
            title: '单号',
            dataIndex: 'sales_order',
            key: 'sales_order',
            sorter: true,
            width: '180px',
            fixed: 'left',
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            sorter: true,
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '付款方',
            dataIndex: 'client_name',
            key: 'client_name',
          },
          {
            title: '收款金额',
            dataIndex: 'amount',
            key: 'amount',
            sorter: true,
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true,
          },
        ],
        tableHeight: window.innerHeight / 2 - 256,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        salesPaymentRecord(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      changeOrder(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'ascend' ? '' : '-'}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>