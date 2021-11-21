<template>
  <div>
    <a-card :loading="loading">
      <div slot="title">
        <div style="float: left;">{{`${order.warehouse_name} | ${moment(order.date).format('YYYY-MM-DD')}`}}</div>
        <div style="float: right;">
          <div style="width: 156px; display: inline-block;">整单折扣(%): {{order.discount}} %</div>
          <div style="width: 156px; display: inline-block;">表单利润(元): {{orderProfit}}</div>
        </div>
      </div>
      <a-table :columns="columns" :data-source="order.goods_set" size="small" :pagination="false" :loading="loading">
        <div slot="action" slot-scope="value, item">
          <a-button type="primary" size="small" @click="form = {...item}; visible = true;">修改成本
          </a-button>
        </div>
      </a-table>
    </a-card>

    <a-modal v-model="visible" title="修改成本" okText="保存" :maskClosable="false" @ok="changePurchasePrice"
      @cancel="resetForm">
      <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item label="成本价">
          <a-input-number v-model="form.purchase_price"  style="width: 100%;" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { salesOrderProfitUpdate } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'OrderCard',
    props: ['order', 'loading'],
    data() {
      return {
        NP,
        moment,
        columns: [
          {
            title: '编号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '规格',
            dataIndex: 'spec',
            key: 'spec',
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
            title: '成本价(元)',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
          },
          {
            title: '销售价(元)',
            dataIndex: 'retail_price',
            key: 'retail_price',
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        changeCostVisible: false,
        visible: false,
        changeForm: {
          purchase_price: 0,
        },
        form: { purchase_price: 0 },
        targetProduct: null,
      };
    },
    computed: {
      orderProfit() {
        let totalProfit = 0;
        for (let item of this.order.goods_set) {
          let retailPrice = NP.times(item.retail_price, this.order.discount, 0.01);
          totalProfit = NP.plus(totalProfit, NP.times(item.quantity, NP.minus(retailPrice, item.purchase_price)));
        }
        return NP.round(totalProfit, 2)
      }
    },
    methods: {
      changePurchasePrice() {
        salesOrderProfitUpdate({ id: this.form.id, purchase_price: this.form.purchase_price })
          .then(() => {
            this.$message.success('修改成功');
            this.$emit('update');
            for (let item of this.order.goods_set) {
              if (item.id == this.form.id) {
                item.purchase_price = this.form.purchase_price;
              }
            }
            this.visible = false;

          })
          ;
      },
      resetForm() {
        this.form = { purchase_price: 0 };
      },
    },
  }
</script>

<style scoped>
</style>