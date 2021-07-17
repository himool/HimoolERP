<template>
  <div>
    <a-card title="销售任务提醒" style="height: calc(50vh - 48px);">
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        :scroll="{y: tableHeight}" />
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesTaskList } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'SalesTask',
    data() {
      return {
        searchForm: {
          page: 1,
          page_size: 10,
          datetime: moment().format(),
        },
        perPage: 10,
        totalRows: 0,
        loading: false,
        columns: [
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '任务商品',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '任务数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '完成数量',
            dataIndex: 'completed_quantity',
            key: 'completed_quantity',
          },
        ],
        items: [],
        tableHeight: window.innerHeight / 2 - 240,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        salesTaskList(this.searchForm)
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
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>