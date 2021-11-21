<template>
  <div>
    <a-card>
      <a-row>
        <a-col :span="8">
          <a-form-model-item label="仓库" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" style="margin: 0;">
            <a-select v-model="searchForm.warehouse" allowClear :disabled="loading" style="width: 100%;" @change="search">
              <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-col>
        <a-col :span="8">
          <a-form-model-item label="时间" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }" style="margin: 0;">
            <a-range-picker v-model="searchForm.dateRange" @change="search" style="width: 100%;" :disabled="loading" />
          </a-form-model-item>
        </a-col>
        <a-col :span="8">
          <a-form-model-item label="利润总计" :label-col="{ span: 12 }" :wrapper-col="{ span: 12 }"
            style="float: right; margin: 0;">
            <div style="width: 156px; font-size: 20px; font-weight: bold;">{{NP.round(totalProfit, 2)}}</div>
          </a-form-model-item>
        </a-col>
      </a-row>
    </a-card>

    <div v-if="items.length != 0">

      <div v-for="item in items" :key="item.id">
        <order-card :order="item" :loading="loading" style="margin-top: 16px;" @create="create" @update="update" @destroy="destroy" />
      </div>

      <div style="text-align: center; margin: 16px 0;">
        <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </div>
    <a-empty v-else description="暂无数据" style="margin-top: 24px;"/>


  </div>
</template>

<script>
  import { salesProfitList } from '@/api/sales'
  import { warehouseList } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesProfit',
    components: {
      OrderCard: () => import('./OrderCard'),
    },
    data() {
      return {
        NP,
        searchForm: {
          warehouse: null,
          dateRange: [moment().startOf('day'), moment().startOf('day')],
        },
        currentPage: 1,
        perPage: 5,
        totalRows: 0,
        loading: false,
        warehouseItems: [],
        items: [],
        totalProfit: 0,
      };
    },
    methods: {
      initailize() {
        this.list();

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
          ;
      },
      list() {
        let form = {
          start_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[0].format('YYYY-MM-DD') : null,
          end_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[1].format('YYYY-MM-DD') : null,
          warehouse: this.searchForm.warehouse,
          page: this.currentPage,
        }

        this.loading = true;
        salesProfitList(form)
          .then(resp => {
            this.totalProfit = resp.data.total_profit;
            this.items = resp.data.results;
            this.totalRows = resp.data.count;
          })
          
          .finally(() => {
            this.loading = false;
          });
      },
      create(orderId, item) {
        this.totalProfit += item.amount;
        let order = this.items[this.items.findIndex(i => i.id == orderId)];
        order.extra_profits.push(item);
      },
      update(orderId, item) {
        let order = this.items[this.items.findIndex(i => i.id == orderId)];
        let productIndex = order.products.findIndex(i => i.id == item.id);
        let product = order.products[productIndex];
        this.totalProfit -= NP.times((item.purchase_price - product.purchase_price), item.quantity);
        order.products.splice(productIndex, 1, item);
      },
      destroy(orderId, item) {
        let order = this.items[this.items.findIndex(i => i.id == orderId)];
        let extraProfitIndex = order.extra_profits.findIndex(i => i.id == item.id);
        this.totalProfit -= order.extra_profits[extraProfitIndex].amount;
        order.extra_profits.splice(order.extra_profits.findIndex(i => i.id == item.id), 1);
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      search() {
        this.currentPage = 1;
        this.list();
      }
    },
    mounted() {
      this.initailize();
    },
  }
</script>

<style scoped>
</style>