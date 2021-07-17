<template>
  <div>
    <a-card style="height: calc(50vh - 48px);">
      <div slot="title" style="height: 24px;">
        <span>出入库任务提醒</span>
        <a-select v-model="taskType" size="small" @change="changeTask"
          style="width: 160px; float: right;">
          <a-select-option value="purchase">采购入库</a-select-option>
          <a-select-option value="purchaseReturn">采购退货</a-select-option>
          <a-select-option value="sales">销售出库</a-select-option>
          <a-select-option value="salesReturn">销售退货</a-select-option>
        </a-select>
      </div>
      
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        :scroll="{y: tableHeight}">
        <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button type="link" @click="viewTask(item)">查看</a-button>
        </div>
      </a-table>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { purchaseOrderList } from '@/api/purchase'
  import { salesOrderList } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'WarehouseTask',
    data() {
      return {
        moment,
        taskType: 'purchase',
        items: [],
        perPage: 10,
        totalRows: 0,
        searchForm: { page: 1, page_size: 10, is_done: false },
        loading: false,
        columns: [
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        tableHeight: window.innerHeight / 2 - 240,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        if (this.taskType === 'purchase') {
          this.getPurchase();
        } else if (this.taskType === 'purchaseReturn') {
          this.getPurchaseReturn();
        } else if (this.taskType === 'sales') {
          this.getSales();
        } else if (this.taskType === 'salesReturn') {
          this.getSalesReturn();
        }
      },
      getPurchase() {
        this.loading = true;
        purchaseOrderList(this.searchForm)
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
      getPurchaseReturn() {
        this.loading = true;
        purchaseOrderList({ ...this.searchForm, is_return: true })
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
      getSales() {
        this.loading = true;
        salesOrderList(this.searchForm)
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
      getSalesReturn() {
        this.loading = true;
        salesOrderList({ ...this.searchForm, is_return: true })
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
      viewTask(item) {
        if (this.taskType === 'purchase' || this.taskType === 'salesReturn') {
          this.$router.push({ path: '/into_warehouse', query: { search: item.id } });
        } else {
          this.$router.push({ path: '/out_warehouse', query: { search: item.id } });
        }
      },
      changeTask() {
        this.searchForm.page = 1;
        this.list();
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