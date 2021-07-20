<template>
  <div>
    <a-card>
      <a-row gutter="16">
        <a-col :span="8">
          <a-select v-model="searchForm.supplier" placeholder="供应商" :disabled="tableLoading || cardLoading"
            style="width: 100%;" @change="search" allowClear>
            <a-select-option v-for="item in supplierItems" :key="item.id" :value="item.id">{{item.name}}
            </a-select-option>
          </a-select>
        </a-col>
        <a-col :span="8">
          <a-range-picker :ranges="ranges" :disabled="tableLoading || cardLoading" @change="changeDateRange"
            style="width: 100%;" />
        </a-col>
        <a-col :span="8">
          <a-input-search v-model="searchForm.search" placeholder="单号" :disabled="tableLoading || cardLoading"
            enter-button @search="search" allowClear />
        </a-col>
      </a-row>
    </a-card>
    <a-row gutter="8" style="margin-top: 8px;">
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="应付金额" :value="statistics.total_amount" :loading="cardLoading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="已付金额" :value="statistics.amount" :loading="cardLoading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="待付金额" :value="NP.minus(statistics.total_amount, statistics.amount)"
            :loading="cardLoading" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card hoverable>
          <a-statistic title="退款金额" :value="statistics.return_amount" :loading="cardLoading" />
        </a-card>
      </a-col>
    </a-row>
    <a-row style="margin-top: 8px;">
      <a-card title="采购付款统计">
        <a-table :columns="columns" :data-source="items" :loading="tableLoading" :pagination="false" size="small"
          @change="changeOrder">
          <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          <div slot="is_return" slot-scope="value">{{value ? '退货单' : '采购单'}}</div>
          <div slot="remain_amount" slot-scope="value, item">{{NP.minus(item.total_amount, item.amount)}}</div>
          <div slot="action" slot-scope="value, item">
            <a-button size="small" type="primary" @click="payment(item)">付款</a-button>
          </div>
        </a-table>

        <div style="text-align: center; margin: 16px 0;">
          <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
            @change="changePage" />
        </div>
      </a-card>
    </a-row>

    <payment-modal v-model="visible" :order="targetItem" @payment="create" />
  </div>
</template>

<script>
  import { supplierList, purchaseOrderList, paymentRecordCreate } from '@/api/purchase'
  import { purchaseStatistics } from '@/api/report'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseStatistics',
    components: {
      PaymentModal: () => import('@/components/PaymentModal/PaymentModal'),
    },
    data() {
      return {
        NP,
        moment,
        searchForm: { page: 1, ordering: '-date', search: '', supplier: undefined },
        supplierItems: [],
        items: [],
        ranges: {
          '7天': [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
          '15天': [moment().add(-15, 'days').startOf('day'), moment().startOf('day')],
          '30天': [moment().add(-30, 'days').startOf('day'), moment().startOf('day')],
        },
        tableLoading: false,
        cardLoading: false,
        totalRows: 0,
        perPage: 15,
        columns: [
          {
            title: '单号',
            dataIndex: 'id',
            key: 'id',
            sorter: true,
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
            sorter: true,
          },
          {
            title: '联系人',
            dataIndex: 'contacts_name',
            key: 'contacts_name',
          },
          {
            title: '供应商',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
          {
            title: '单据类型',
            dataIndex: 'is_return',
            key: 'is_return',
            scopedSlots: { customRender: 'is_return' },
          },
          {
            title: '总金额',
            dataIndex: 'total_amount',
            key: 'total_amount',
            sorter: true,
          },
          {
            title: '付款金额',
            dataIndex: 'amount',
            key: 'amount',
            sorter: true,
          },
          {
            title: '待付金额',
            dataIndex: 'remain_amount',
            key: 'remain_amount',
            scopedSlots: { customRender: 'remain_amount' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        targetItem: {},
        visible: false,
        statistics: { total_amount: 0, amount: 0, return_amount: 0 },
      };
    },
    methods: {
      initialize() {
        this.list();
        supplierList()
          .then(resp => {
            this.supplierItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.tableLoading = true;
        this.cardLoading = true;
        purchaseOrderList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.tableLoading = false;
          });

        purchaseStatistics(this.searchForm)
          .then(resp => {
            this.statistics = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.cardLoading = false;
          });
      },
      create(form) {
        paymentRecordCreate(form)
          .then(resp => {
            this.$message.success('支付成功');
            this.visible = false;
            for (let item of this.items) {
              if (item.id == resp.data.id) {
                item.amount = resp.data.amount;
                break
              }
            }
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.tableLoading = false;
          });
      },
      payment(item) {
        this.targetItem = { ...item };
        this.visible = true;
      },
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      changeOrder(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'ascend' ? '' : '-'}${sorter.field}`;
        this.list();
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      changeDateRange(dateRange) {
        this.searchForm.start_date = moment(dateRange[0]).format();
        this.searchForm.end_date = moment(dateRange[1]).format();
        this.search();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>