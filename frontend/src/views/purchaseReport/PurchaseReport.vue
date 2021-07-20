<template>
  <div>
    <a-card :tab-list="tabList" :active-tab-key="currentTab" @tabChange="changeTab">
      <a-row gutter="24">
        <a-col :span="8">
          <a-form-model-item :wrapper-col="{ span: 24 }">
            <a-radio-group v-model="radioValue" button-style="solid" @change="changeRadio" style="width: 100%;">
              <a-radio-button value="0" style="width: 25%;">今日</a-radio-button>
              <a-radio-button value="1" style="width: 25%;">昨天</a-radio-button>
              <a-radio-button value="-7" style="width: 25%;">近7天</a-radio-button>
              <a-radio-button value="-30" style="width: 25%;">近30天</a-radio-button>
            </a-radio-group>
          </a-form-model-item>
        </a-col>
        <a-col :span="8">
          <a-form-model-item label="自定义时间" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
            <a-range-picker v-model="searchForm.dateRange" @change="changeDate" style="width: 100%;" />
          </a-form-model-item>
        </a-col>
        <a-col :span="8">
          <a-form-model-item label="分类" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-select v-model="searchForm.category" allowClear style="width: 100%;" @change="changeCategory">
              <a-select-option v-for="item in categoryItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-col>
      </a-row>

      <a-descriptions style="text-align: center;">
        <a-descriptions-item label="采购次数"><span class="total">{{totalTimes}}</span></a-descriptions-item>
        <a-descriptions-item label="采购总数"><span class="total">{{totalQuantity}}</span></a-descriptions-item>
        <a-descriptions-item label="采购金额"><span class="total">{{totalAmount}}</span></a-descriptions-item>
      </a-descriptions>

      <div>
        <flow-pane v-show="currentTab === 'flow'" :items="items" :loading="loading" />
        <goods-pane v-show="currentTab === 'goods'" :items="items" :loading="loading" />
        <product-pane v-show="currentTab === 'product'" :items="items" :loading="loading" />
      </div>
      <div style="text-align: center; margin-top: 12px;">
        <a-spin :spinning="loading && searchForm.page > 1" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { purchaseReportList } from '@/api/report'
  import { categoryList } from '@/api/goods'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseReport',
    components: {
      FlowPane: () => import('./FlowPane'),
      GoodsPane: () => import('./GoodsPane'),
    },
    data() {
      return {
        currentTab: 'flow',
        radioValue: '0',
        tabList: [
          {
            key: 'flow',
            tab: '采购明细',
          },
          {
            key: 'goods',
            tab: '按商品汇总',
          },
        ],
        searchForm: {
          dateRange: [moment().startOf('day'), moment().startOf('day')],
          category: null,
          page: 1,
        },
        loading: true,
        categoryItems: [],
        total: {
          quantity: 0,
          times: 0,
          amount: 0,
        },
        items: [],
        perPage: 20,
        moreData: false,
      };
    },
    computed: {
      totalQuantity() {
        return this.total.quantity ? this.total.quantity : 0
      },
      totalTimes() {
        return this.total.times ? this.total.times : 0
      },
      totalAmount() {
        return this.total.amount ? NP.round(this.total.amount, 2) : 0
      },
    },
    methods: {
      initailize() {
        if (this.$route.query.type) {
          this.currentTab = this.$route.query.type;
        } else {
          this.$router.replace({ query: { type: this.currentTab } })
        }

        this.list();

        categoryList()
          .then(resp => {
            this.categoryItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });

        window.onscroll = () => {
          let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
          let windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
          let scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
          if (scrollTop + windowHeight == scrollHeight) {
            this.loadMore();
          }
        }
      },
      list() {
        this.loading = true;
        let form = {
          start_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[0].format() : null,
          end_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[1].format() : null,
          category: this.searchForm.category,
          page: this.searchForm.page,
          type: this.currentTab,
        }

        purchaseReportList(form)
          .then(resp => {
            this.total = resp.data.total;
            if (form.page == 1) {
              this.items = resp.data.results;
            } else {
              this.items.push(...resp.data.results);
            }

            if (resp.data.results.length >= this.perPage) {
              this.moreData = true;
            }
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      loadMore() {
        if (this.moreData && !this.loading) {
          this.searchForm.page += 1;
          this.list();
        }
      },
      changeTab(key) {
        this.currentTab = key;
        this.$router.replace({ query: { type: this.currentTab } })
        this.resetForm();
        this.search();
      },
      changeRadio(evt) {
        let value = evt.target.value;
        if (value < 0) {
          this.searchForm.dateRange = [moment().startOf('day').add(value, 'day'), moment().startOf('day')]
        } else {
          this.searchForm.dateRange = [moment().startOf('day').subtract(value, 'day'), moment().startOf('day').subtract(value, 'day'),]
        }
        this.search();
      },
      changeDate() {
        this.radioValue = null;
        this.search();
      },
      changeCategory() {
        this.search();
      },
      resetForm() {
        this.radioValue = '0';
        this.moreData = true;
        this.searchForm = {
          dateRange: [moment().startOf('day'), moment().startOf('day')],
          category: null,
          page: 1,
        };
      },
    },
    mounted() {
      this.initailize();
    },
  }
</script>

<style scoped>
  .total {
    color: #a94442;
  }
</style>