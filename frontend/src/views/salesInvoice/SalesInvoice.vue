<template>
  <div style="margin: 24px auto; width: 900px;">
    <div v-if="loading"  style="text-align: center;">
      <a-spin size="large" />
    </div>
    
    <div v-else style="text-align: center;">
      <div id="invoice" style="padding: 24px;">
        <a-row>
          <a-col :span="8" :offset="8">
            <div style="font-size: 26px;">{{item.is_return ? '销售退货单' : '销售单'}}</div>
          </a-col>
          <a-col :span="8">
            <div style="float: right; color: #777;">{{item.id}}</div>
          </a-col>
        </a-row>
        <a-row style="font-size: 15px; margin-top: 8px;">
          <a-col :span="6">仓库: {{item.warehouse_name}}</a-col>
          <a-col :span="6">销售员: {{item.seller_username}}</a-col>
          <a-col :span="6">结算账户: {{item.account_name}}</a-col>
          <a-col :span="6">日期: {{moment(item.date).format('YYYY-MM-DD')}}</a-col>
        </a-row>
        <a-row style="margin-top: 8px;">
          <a-table :columns="columns" :data-source="item.goods_set" size="small" :pagination="false" :loading="loading"
            bordered />
        </a-row>
        <a-row style="margin: 16px;">
          <a-col :span="12">
            <div style="font-size: 15px; float: left;">整单折扣: {{item.discount}} %</div>
          </a-col>
          <a-col :span="12">
            <div style="font-size: 15px; float: right;">总合计: ¥ {{NP.times(totalAmount, item.discount, 0.01)}}</div>
          </a-col>
        </a-row>
      </div>
    </div>
  </div>
</template>

<script>
  import { salesOrderRetrieve } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesInvoice',
    data() {
      return {
        NP,
        moment,
        loading: false,
        columns: [
          {
            title: '商品名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '规格型号',
            dataIndex: 'specification',
            key: 'specification',
          },
          {
            title: '单位',
            dataIndex: 'unit',
            key: 'unit',
          },
          {
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '单价',
            dataIndex: 'retail_price',
            key: 'retail_price',
          },
          {
            title: '合计',
            dataIndex: 'amount',
            key: 'amount',
          },
        ],
        item: {},
      };
    },
    computed: {
      totalAmount() {
        let totalAmount = 0;
        if (this.item.goods_set && this.item.goods_set.length > 0) {
          for (let goods of this.item.goods_set) {
            totalAmount = NP.plus(totalAmount, NP.times(goods.quantity, goods.retail_price));
          }
        }
        return NP.round(totalAmount, 2)
      }
    },
    methods: {
      initialize() {
        this.loading = true;
        salesOrderRetrieve({ id: this.$route.query.id })
          .then(resp => {
            this.item = resp.data;
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