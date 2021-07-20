<template>
  <div>
    <a-card>
      <a-row gutter="12">
        <a-col :span="8" :xl="6" style="line-height: 40px;">
          <div class="field" style="width: 96px;">仓库:</div>
          <a-select v-model="searchForm.warehouse" allowClear :disabled="loading" style="width: calc(100% - 96px);"
            @change="search()">
            <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
            </a-select-option>
          </a-select>
        </a-col>
        <a-col :span="8" :xl="6" style="line-height: 40px;">
          <div class="field" style="width: 54px;">日期:</div>
          <a-range-picker v-model="dateRange" :ranges="ranges" @change="search()" style="width: calc(100% - 54px);"
            :disabled="loading" />
        </a-col>
        <a-col :span="2" :xl="6" style="line-height: 40px;">
          <a-button type="primary" @click="search()" style="margin-left: 12px;">查询</a-button>
        </a-col>
        <a-col :span="6" :xl="6">
          <a-form-model-item label="利润总计" :label-col="{ span: 12 }" :wrapper-col="{ span: 12 }"
            style="float: right; margin: 0;">
            <div style="width: 126px; font-size: 20px; font-weight: bold;">
              <a-spin v-if="computeLoading" size="small" />
              <span v-else>{{NP.round(totalProfit, 2)}}</span>
            </div>
          </a-form-model-item>
        </a-col>
      </a-row>
    </a-card>

    <div v-if="loading" style="text-align: center;">
      <a-spin style="margin-top: 36px;" size="large" />
    </div>
    <div v-else>
      <div v-if="items.length != 0">
        <div v-for="item in items" :key="item.id">
          <order-card :order="item" :loading="loading" style="margin-top: 16px;" @update="getTotalProfit" />
        </div>

        <div style="text-align: center; margin: 16px 0;">
          <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
            @change="value => search(value)" />
        </div>
      </div>
      <a-empty v-else description="暂无数据" style="margin-top: 36px;" />
    </div>
  </div>
</template>

<script>
  import { salesOrderProfitList, salesOrderTotalProfit } from '@/api/sales'
  import { warehouseList } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesOrderProfit',
    components: {
      OrderCard: () => import('./OrderCard'),
    },
    data() {
      return {
        NP,
        searchForm: {
          warehouse: undefined,
          page: 1,
        },
        ranges: {
          '7天': [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
          '15天': [moment().add(-15, 'days').startOf('day'), moment().startOf('day')],
          '30天': [moment().add(-30, 'days').startOf('day'), moment().startOf('day')],
        },
        dateRange: [moment().startOf('day'), moment().startOf('day')],
        perPage: 5,
        totalRows: 0,
        loading: false,
        computeLoading: false,
        warehouseItems: [],
        items: [],
        totalProfit: 0,
      };
    },
    methods: {
      initailize() {
        this.search();

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.loading = true;
        salesOrderProfitList(this.searchForm)
          .then(resp => {
            this.items = resp.data.results;
            this.totalRows = resp.data.count;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      getTotalProfit() {
        this.computeLoading = true;
        salesOrderTotalProfit(this.searchForm)
          .then(resp => {
            this.totalProfit = resp.data.total_profit;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.computeLoading = false;
          });
      },
      search(page = 1) {
        this.searchForm.start_date = this.dateRange.length > 0 ? this.dateRange[0].format() : null;
        this.searchForm.end_date = this.dateRange.length > 0 ? this.dateRange[1].format() : null;
        this.searchForm.page = page;
        this.list();
        this.getTotalProfit();
      }
    },
    mounted() {
      this.initailize();
    },
  }
</script>

<style scoped>
  .field {
    display: inline-block;
    text-align: right;
    padding-right: 6px;
  }
</style>