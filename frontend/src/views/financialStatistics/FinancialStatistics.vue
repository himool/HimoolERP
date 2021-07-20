<template>
  <div>
    <a-row gutter="8">
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="订单收入" :value="statistics.sales_amount" :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="销售退款" :value="statistics.sales_return_amount" :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="采购支出" :value="statistics.purchase_amount" :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="采购退款" :value="statistics.purchase_return_amount" :loading="loading" />
        </a-card>
      </a-col>
    </a-row>
    <a-row gutter="8" style="margin-top: 8px;">
      <a-col :span="12">
        <sales-detail />
      </a-col>
      <a-col :span="12">
        <sales-return-detail />
      </a-col>
    </a-row>
    <a-row gutter="8" style="margin-top: 8px;">
      <a-col :span="12">
        <purchase-detail />
      </a-col>
      <a-col :span="12">
        <purchase-return-detail />
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { financialStatistics } from '@/api/report'

  export default {
    name: 'FinancialStatistics',
    components: {
      SalesDetail: () => import('./SalesDetail.vue'),
      SalesReturnDetail: () => import('./SalesReturnDetail.vue'),
      PurchaseDetail: () => import('./PurchaseDetail.vue'),
      PurchaseReturnDetail: () => import('./PurchaseReturnDetail.vue'),
    },
    data() {
      return {
        loading: false,
        statistics: {},
      };
    },
    methods: {
      initialize() {
        this.loading = true;
        financialStatistics()
          .then(resp => {
            this.statistics = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>