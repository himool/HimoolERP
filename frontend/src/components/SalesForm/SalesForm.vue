<template>
  <div>
    <a-card :title="form.is_return ? `销售退货单 - ${form.id}` : `销售单 - ${form.id}`">
      <a-row style="margin: 6px 0;">
        <a-col :span="8">仓库: {{form.warehouse_name}}</a-col>
        <a-col :span="8">结算账户: {{form.account_name}}</a-col>
        <a-col :span="8">销售员: {{form.seller_name}}</a-col>
      </a-row>
      <a-row style="margin: 6px 0;">
        <a-col :span="8">日期: {{moment(form.date).format('YYYY-MM-DD')}}</a-col>
        <a-col :span="8">整单折扣(%): {{form.discount}}</a-col>
        <a-col :span="8">实收金额: {{form.amount}}</a-col>
      </a-row>
      <a-row style="margin: 6px 0;">
        <a-col :span="8">客户名称: {{form.client_name}}</a-col>
        <a-col :span="8">联系人: {{form.client_contacts}}</a-col>
        <a-col :span="8">电话: {{form.client_phone}}</a-col>
      </a-row>
      <a-row style="margin: 6px 0;">
        <a-col :span="12">地址: {{form.client_address}}</a-col>
        <a-col :span="12">备注: {{form.remark}}</a-col>
      </a-row>
      <div style="margin: 16px 0;">
        <a-table :columns="columns" :data-source="dataSource" :pagination="false" size="small">
          <div slot="index" slot-scope="value, item, index">{{item.isTotal ? '' : index + 1}}</div>
        </a-table>
      </div>
      <div>
        <a-popconfirm title="确定提交吗?" @confirm="confirm">
          <a-button type="primary" :loading="loading">确认发货</a-button>
        </a-popconfirm>
        <a-button style="margin-left: 16px;" @click="printInvoice">生成打印单据</a-button>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesOrderConfirm } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesForm',
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
            title: '编号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '商品',
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
            title: '单价(元)',
            dataIndex: 'retail_price',
            key: 'retail_price',
            customRender: (value, item) => {
              return item.isTotal ? '' : NP.round(value, 2)
            },
          },
          {
            title: '金额(元)',
            dataIndex: 'amount',
            key: 'amount',
            customRender: (value, item) => {
              return item.isTotal ? value : NP.round(NP.times(item.quantity, item.retail_price), 2)
            },
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
          },
        ],
      };
    },
    computed: {
      dataSource() {
        let totalQuantity = 0, totalAmount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            totalQuantity += item.quantity;
            totalAmount = NP.times(item.quantity, item.retail_price);
          }
        }

        let totalItem = {
          name: '合计:',
          quantity: totalQuantity,
          amount: NP.times(totalAmount, this.form.discount, 0.01),
          isTotal: true,
        };

        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      },
    },
    methods: {
      confirm() {
        let orderId = this.form.id;
        this.loading = true;
        salesOrderConfirm({ id: orderId })
          .then(() => {
            this.$emit('confirm', orderId);
            this.$message.success('提交成功');
          })
          .finally(() => {
            this.loading = false;
          });
      },
      printInvoice() {
        window.open(`/invoice/sales?id=${this.form.id}`);
      },
    },
  }
</script>
