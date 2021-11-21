<template>
  <div>
    <a-card style="padding-bottom:0px;">
      <a-row>
        <a-col :span="24">
          <ButtonsPicker
            :radioValue="radioValue"
            :dateRange="searchForm.dateRange"
            @aRangePickerChange="
              (value) => {
                $set(searchForm, 'dateRange', value);
                radioValue = null;
                search();
              }
            "
            @aRadioGroupChange="
              (value) => {
                radioValue = value;
              }
            "
          ></ButtonsPicker>
        </a-col>
      </a-row>
    </a-card>
    <a-row gutter="8" style="margin-top:8px;">
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="订单收入(元)"
            :value="statistics.sales_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="销售退款(元)"
            :value="statistics.sales_return_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="日常收入(元)"
            :value="statistics.income_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="采购支出(元)"
            :value="statistics.purchase_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="采购退款(元)"
            :value="statistics.purchase_return_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="日常支出(元)"
            :value="statistics.expenditure_amount"
            :loading="loading"
          />
        </a-card>
      </a-col>
    </a-row>

    <a-row gutter="8" style="margin-top: 8px">
      <a-col :span="12">
        <sales-detail />
      </a-col>
      <a-col :span="12">
        <sales-return-detail />
      </a-col>
    </a-row>
    <a-row gutter="8" style="margin-top: 8px">
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
import { financialStatistics } from "@/api/report";
import moment from "moment";
export default {
  name: "FinancialStatistics",
  components: {
    SalesDetail: () => import("./SalesDetail.vue"),
    SalesReturnDetail: () => import("./SalesReturnDetail.vue"),
    PurchaseDetail: () => import("./PurchaseDetail.vue"),
    PurchaseReturnDetail: () => import("./PurchaseReturnDetail.vue"),
    ButtonsPicker: () => import("@/components/Fields/ButtonsPicker"),
  },
  data() {
    return {
      searchForm: {
        dateRange: [moment().startOf("day"), moment().startOf("day")],
        category: null,
        page: 1,
      },
      moment,
      radioValue: "0",
      loading: false,
      statistics: {},
    };
  },
  methods: {
    search() {
      this.searchForm.page = 1;
      this.list();
    },
    changeDate() {
      this.radioValue = null;
      this.search();
    },
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      let form = {
        start_date:
          this.searchForm.dateRange.length > 0
            ? this.searchForm.dateRange[0].format("YYYY-MM-DD")
            : null,
        end_date:
          this.searchForm.dateRange.length > 0
            ? this.searchForm.dateRange[1].format("YYYY-MM-DD")
            : null,
        category: this.searchForm.category,
        page: this.searchForm.page,
        type: this.currentTab,
      };
      financialStatistics(form)
        .then((resp) => {
          this.statistics = resp.data;
        })

        .finally(() => {
          this.loading = false;
        });
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped>
</style>