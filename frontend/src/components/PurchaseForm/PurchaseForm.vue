<template>
  <div>
    <a-card :title="form.is_return ? `采购退货单 - ${form.id}` : `采购单 - ${form.id}`">
      <a-row style="margin: 6px 0;">
        <a-col :span="8">供应商: {{form.supplier_name}}</a-col>
        <a-col :span="8">仓库: {{form.warehouse_name}}</a-col>
        <a-col :span="8">结算账户: {{form.account_name}}</a-col>
      </a-row>
      <a-row style="margin: 6px 0;">
        <a-col :span="8">联系人: {{form.contacts}}</a-col>
        <a-col :span="8">日期: {{moment(form.date).format('YYYY-MM-DD')}}</a-col>
        <a-col :span="8">实付金额: {{form.amount}}</a-col>
      </a-row>
      <a-row style="margin: 6px 0;">
        <a-col :span="24">备注: {{form.remark}}</a-col>
      </a-row>
      <div style="margin: 16px 0;">
        <a-table :columns="columns" :data-source="dataSource" :pagination="false" size="small">
          <div slot="index" slot-scope="value, item, index">{{item.isTotal ?  '' : index + 1}}</div>
          <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
          <div slot="discount_amount" slot-scope="value">{{NP.round(value, 2)}}</div>
        </a-table>
      </div>
      <div>
        <a-popconfirm title="确定提交吗?" @confirm="confirm">
          <a-button type="primary" :loading="loading">提交</a-button>
        </a-popconfirm>
        <a-button style="margin-left: 16px;" @click="printInvoice">生成打印单据</a-button>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { purchaseOrderConfirm } from '@/api/purchase'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseForm',
    props: ['form'],
    data() {
      return {
        NP,
        moment,
        loading: false,
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '商品',
            dataIndex: 'name',
            key: 'name',
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
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            customRender: (value, item) => {
              return item.isTotal ? '' : NP.round(value, 2)
            },
          },
          {
            title: '折扣',
            dataIndex: 'discount',
            key: 'discount',
            customRender: (value, item) => {
              return item.isTotal ? '' : `${value} %`
            },
          },
          {
            title: '折后价',
            dataIndex: 'discount_price',
            key: 'discount_price',
            customRender: (value, item) => {
              return item.isTotal ? '' : NP.round(value, 2)
            },
          },
          {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
            scopedSlots: { customRender: 'amount' },
          },
          {
            title: '折后金额',
            dataIndex: 'discount_amount',
            key: 'discount_amount',
            scopedSlots: { customRender: 'discount_amount' },
          },
        ],
      };
    },
    computed: {
      dataSource() {
        let quantity = 0, amount = 0, discount_amount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
            amount = NP.plus(amount, item.amount);
            discount_amount = NP.plus(discount_amount, item.discount_amount);
          }
        }

        let totalItem = { name: '合计:', isTotal: true, quantity, amount, discount_amount };
        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      },
    },
    methods: {
      confirm() {
        let orderId = this.form.id;
        this.loading = true;
        purchaseOrderConfirm({ id: orderId })
          .then(() => {
            this.$emit('confirm', orderId);
            this.$message.success('提交成功');
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      printInvoice() {
        window.open(`/invoice/purchase?id=${this.form.id}`);
      },
    },
  }
</script>