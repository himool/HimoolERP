<template>
  <div style="margin: 24px auto; width: 900px;">
    <div v-if="loading"  style="text-align: center;">
      <a-spin size="large" />
    </div>

    <div v-else style="text-align: center;">
      <div id="view" style="padding: 24px;">
        <a-row>
          <a-col :span="8" :offset="8">
            <div style="font-size: 26px;">盘点单</div>
          </a-col>
          <a-col :span="8">
            <div style="float: right; color: #777;">{{item.id}}</div>
          </a-col>
        </a-row>
        <a-row style="font-size: 15px; margin-top: 8px;">
          <a-col :span="6">仓库: {{item.warehouse_name}}</a-col>
          <a-col :span="6">盘点总数: {{total.quantity}}</a-col>
          <a-col :span="6">盈亏金额: {{total.profitAmount}}</a-col>
          <a-col :span="6">日期: {{moment(item.date).format('YYYY-MM-DD')}}</a-col>
        </a-row>
        <a-row style="margin-top: 8px;">
          <a-table :columns="columns" :data-source="item.goods_set" size="small" :pagination="false" :loading="loading"
            bordered>
            <div slot="profit_amount" slot-scope="value, item">
              {{NP.round(NP.times(item.purchase_price, NP.minus(item.quantity, item.before_counting)), 2)}}
            </div>
          </a-table>
        </a-row>
      </div>
    </div>
  </div>
</template>

<script>
  import { countingListRetrieve } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'CountingListInvoice',
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
            title: '盘点数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '盘点前数量',
            dataIndex: 'before_counting',
            key: 'before_counting',
          },
          {
            title: '盈亏金额',
            dataIndex: 'profit_amount',
            key: 'profit_amount',
            scopedSlots: { customRender: 'profit_amount' },
          },
        ],
        item: {},
      };
    },
    computed: {
      total() {
        let quantity = 0, profitAmount = 0;
        if (this.item.goods_set) {
          for (let item of this.item.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
            profitAmount = NP.plus(profitAmount, NP.times(item.purchase_price, NP.minus(item.quantity, item.before_counting)))
          }
          profitAmount = NP.round(profitAmount, 2);
        }
        return { quantity, profitAmount }
      },
    },
    methods: {
      initialize() {
        this.loading = true;
        countingListRetrieve({ id: this.$route.query.id })
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