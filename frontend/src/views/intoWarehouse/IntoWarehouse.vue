<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="8">
        <a-card>
          <a-row gutter="8" style="margin-bottom: 8px;">
            <a-col :span="24" :xl="12" style="margin-bottom: 8px;">
              <a-select v-model="searchForm.warehouse" placeholder="仓库" style="width: 100%;" allowClear
                @change="search">
                <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                </a-select-option>
              </a-select>
            </a-col>
            <a-col :span="24" :xl="12" style="margin-bottom: 8px;">
              <a-select v-model="orderType" placeholder="单据类型" style="width: 100%;" @change="search">
                <a-select-option value="purchase">采购单</a-select-option>
                <a-select-option value="salesReturn">销售退货单</a-select-option>
              </a-select>
            </a-col>
            <a-col :span="24" style="margin-bottom: 8px;">
              <a-input-search v-model="searchForm.search" placeholder="单号" enter-button @search="search" />
            </a-col>
          </a-row>
          <a-table :columns="columns" :data-source="items" :loading="loading" :pagination="false" :customRow="customRow"
            :rowClassName="rowClassName" size="small">
            <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          </a-table>
          <div style="text-align: center; margin-top: 16px;">
            <a-pagination :value="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
              @change="changePage" />
          </div>
        </a-card>
      </a-col>
      <a-col :span="24" :lg="16">
        <div v-if="form.id">
          <purchase-form v-if="orderType == 'purchase'" :form="form" @confirm="confirm" />
          <sales-form v-else :form="form" @confirm="confirm" />
        </div>
        <a-card v-else style="height: 70vh;">
          <a-empty :description="false" style="margin-top: 128px;" />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { purchaseOrderList } from '@/api/purchase'
  import { salesOrderList } from '@/api/sales'
  import { warehouseList } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'IntoWarehouse',
    components: {
      PurchaseForm: () => import('@/components/PurchaseForm/PurchaseForm'),
      SalesForm: () => import('@/components/SalesForm/SalesForm'),
    },
    data() {
      return {
        NP,
        moment,
        items: [],
        warehouseItems: [],
        form: {},
        searchForm: { page: 1, warehouse: undefined, search: undefined, is_done: false },
        loading: false,
        totalRows: 0,
        perPage: 16,
        orderType: 'purchase',
        columns: [
          {
            title: '单号',
            dataIndex: 'id',
            key: 'id',
          },
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
        ],
      };
    },
    methods: {
      initialize() {
        this.list();

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
         
      },
      list() {
        this.orderType == 'purchase' ? this.getPurchase() : this.getSalesReturn();
      },
      getPurchase() {
        
        this.loading = true;
        console.log(this.searchForm);
        purchaseOrderList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
            if (this.items.length === 1) {
              this.form = { ...this.items[0] };
            }
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
            if (this.items.length === 1) {
              this.form = this.items[0];
            }
          })
         
          .finally(() => {
            this.loading = false;
          });
      },
      confirm(orderId) {
        this.items.splice(this.items.findIndex(order => order.id == orderId), 1);
      },
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      customRow(item) {
        return {
          on: {
            click: () => {
              this.form = { ...item };
            },
          },
        }
      },
      rowClassName(item) {
        if (item.id == this.form.id) {
          return 'table-selected'
        }
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
  .table-selected {
    background: #e6f7ff;
  }
</style>