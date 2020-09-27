<template>
  <div style="margin: 24px auto; width: 900px;">
    <div v-if="loading"  style="text-align: center;">
      <a-spin size="large" />
    </div>
    
    <div v-else style="text-align: center;">
      <div id="invoice" style="padding: 24px;">
        <a-row>
          <a-col :span="8" :offset="8">
            <div style="font-size: 26px;">{{item.is_return ? '采购退货单' : '采购单'}}</div>
          </a-col>
          <a-col :span="8">
            <div style="float: right; color: #777;">{{item.id}}</div>
          </a-col>
        </a-row>
        <a-row style="font-size: 15px; margin-top: 8px;">
          <a-col :span="6">供应商: {{item.supplier_name}}</a-col>
          <a-col :span="6">收货人: {{item.contacts_name}}</a-col>
          <a-col :span="6">联系方式: {{item.contacts_phone}}</a-col>
          <a-col :span="6">日期: {{moment(item.date).format('YYYY-MM-DD')}}</a-col>
        </a-row>
        <a-row style="margin-top: 8px;">
          <a-table :columns="columns" :data-source="item.goods_set" size="small" :pagination="false" :loading="loading"
            bordered />
        </a-row>
        <a-row style="margin: 16px;">
          <a-col :span="20">
            <div style="float: left; font-size: 15px;">收货地址: {{item.warehouse_address}}</div>
          </a-col>
          <a-col :span="4">
            <div style="float: right; font-size: 15px;">总合计: ¥ {{totalAmount}}</div>
          </a-col>
        </a-row>
      </div>
    </div>
  </div>
</template>

<script>
  import { purchaseOrderRetrieve } from '@/api/purchase'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseInvoice',
    data() {
      return {
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
            title: '规格A',
            dataIndex: 'spec1',
            key: 'spec1',
          },
          {
            title: '规格B',
            dataIndex: 'spec2',
            key: 'spec2',
          },
          {
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '单价',
            dataIndex: 'discount_price',
            key: 'discount_price',
          },
          {
            title: '合计',
            dataIndex: 'discount_amount',
            key: 'discount_amount',
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
            totalAmount = NP.plus(totalAmount, NP.times(goods.quantity, goods.purchase_price));
          }
        }
        return NP.round(totalAmount, 2)
      }
    },
    methods: {
      initialize() {
        this.loading = true;
        purchaseOrderRetrieve({ id: this.$route.query.id })
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