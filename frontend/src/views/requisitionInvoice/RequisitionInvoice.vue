<template>
  <div style="margin: 24px auto; width: 900px;">
    <div v-if="loading" style="text-align: center;">
      <a-spin size="large" />
    </div>

    <div v-else style="text-align: center;">
      <div id="view" style="padding: 24px;">
        <a-row>
          <a-col :span="8" :offset="8">
            <div style="font-size: 26px;">调拨单</div>
          </a-col>
          <a-col :span="8">
            <div style="float: right; color: #777;">{{item.id}}</div>
          </a-col>
        </a-row>
        <a-row style="font-size: 15px; margin-top: 8px;">
          <a-col :span="6">调出仓库: {{item.out_warehouse_name}}</a-col>
          <a-col :span="6">调入仓库: {{item.into_warehouse_name}}</a-col>
          <a-col :span="6">调拨总数: {{totalQuantity}}</a-col>
          <a-col :span="6">日期: {{moment(item.date).format('YYYY-MM-DD')}}</a-col>
        </a-row>
        <a-row style="margin-top: 8px;">
          <a-table :columns="columns" :data-source="item.goods_set" size="small" :pagination="false" :loading="loading"
            bordered />
        </a-row>
      </div>
    </div>
  </div>
</template>

<script>
  import { requisitionRetrieve } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'RequisitionInvoice',
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
            title: '调拨数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
        ],
        item: {},
      };
    },
    computed: {
      totalQuantity() {
        let quantity = 0;
        if (this.item.goods_set) {
          for (let item of this.item.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
          }
        }
        return quantity
      }
    },
    methods: {
      initialize() {
        this.loading = true;
        requisitionRetrieve({ id: this.$route.query.id })
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