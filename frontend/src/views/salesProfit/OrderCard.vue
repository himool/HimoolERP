<template>
  <div>
    <a-card :title="`${order.warehouse_name} | ${moment(order.date).format('YYYY-MM-DD')}`" :loading="loading">
      <a-table :columns="columns" :data-source="dataSource" size="small" :pagination="false" :loading="loading">
        <div slot="goods_name" slot-scope="value, item">
          <div v-if="item.quantity">{{value}}</div>
          <div v-else style="color: #777; font-weight: bold;">{{value}}</div>
        </div>

        <div slot="action" slot-scope="value, item">
          <a-button v-if="item.quantity" type="primary" size="small"
            @click="changeCostVisible = true; targetProduct = item;">修改成本</a-button>
          <a-popconfirm v-else title="确定删除吗?" ok-text="确认" cancel-text="取消" @confirm="deleteExtraProfit(item)">
            <a-button type="danger" size="small">删除</a-button>
          </a-popconfirm>
        </div>
      </a-table>

      <a-row style="margin-top: 12px;">
        <a-col :span="16">
          <a-button type="primary" size="small" @click="addExtraProfitVisible = true">额外利润</a-button>
        </a-col>
        <a-col :span="4">
          <span v-if="order.zero_amount && order.zero_amount != 0">
            抹零金额: {{order.zero_amount}}
          </span>
        </a-col>
        <a-col :span="4">
          表单利润: {{orderProfit}}
        </a-col>
      </a-row>
    </a-card>

    <a-modal v-model="changeCostVisible" title="修改成本" okText="保存" cancelText="取消" :maskClosable="false" @ok="changeCost"
      @cancel="resetForm">
      <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item label="成本价">
          <a-input-number v-model="changeForm.purchase_price" :precision="2" style="width: 100%;" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>

    <a-modal v-model="addExtraProfitVisible" title="添加额外利润" okText="添加" cancelText="取消" :maskClosable="false"
      @ok="addExtraProfit" @cancel="resetForm">
      <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item label="利润">
          <a-input-number v-model="addForm.amount" :precision="2" style="width: 100%;" />
        </a-form-model-item>
        <a-form-model-item label="备注">
          <a-input v-model="addForm.remark" allowClear />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { salesProfitCreate, salesProfitUpdate, salesProfitDestroy } from '@/api/sales'
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
            title: '商品名',
            dataIndex: 'goods_name',
            key: 'goods_name',
            scopedSlots: { customRender: 'goods_name' },
          },
          {
            title: '规格A',
            dataIndex: 'spec1',
            key: 'spec1',
            scopedSlots: { customRender: 'spec1' },
            customRender: (text, row) => {
              return row.quantity ? text : {
                children: <div style="color: #777; font-weight: bold;">{text}</div>,
                attrs: { colSpan: 6 },
              }
            },
          },
          {
            title: '规格B',
            dataIndex: 'spec2',
            key: 'spec2',
            customRender: (text, row) => {
              return row.quantity ? text : { children: text, attrs: { colSpan: 0 } }
            },
          },
          {
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
            customRender: (text, row) => {
              return row.quantity ? text : { children: text, attrs: { colSpan: 0 } }
            },
          },
          {
            title: '成本价',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            customRender: (text, row) => {
              return row.quantity ? NP.round(text, 2) : { children: text, attrs: { colSpan: 0 } }
            },
          },
          {
            title: '销售价',
            dataIndex: 'unit_price',
            key: 'unit_price',
            customRender: (text, row) => {
              return row.quantity ? NP.round(text, 2) : { children: text, attrs: { colSpan: 0 } }
            },
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
            customRender: (text, row) => {
              return row.quantity ? text : { children: text, attrs: { colSpan: 0 } }
            },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        changeCostVisible: false,
        addExtraProfitVisible: false,
        changeForm: {
          purchase_price: 0,
        },
        addForm: {
          amount: 0,
          remark: '',
        },
        targetProduct: null,
      };
    },
    computed: {
      dataSource() {
        let products = [...this.order.products];
        for (let ep of this.order.extra_profits) {
          products.push({
            id: ep.id,
            goods_name: `额外利润: ${ep.amount}`,
            spec1: ep.remark ? `备注: ${ep.remark}` : '',
          })
        }
        return products
      },
      orderProfit() {
        let totalProfit = 0;
        for (let item of this.order.products) {
          totalProfit += NP.times(item.quantity, NP.minus(item.unit_price, item.purchase_price));
        }
        for (let item of this.order.extra_profits) {
          totalProfit += item.amount;
        }
        return NP.round(totalProfit, 2)
      }
    },
    methods: {
      changeCost() {
        salesProfitUpdate({ id: this.targetProduct.id, purchase_price: this.changeForm.purchase_price })
          .then((resp) => {
            this.$message.success('修改成功');
            this.$emit('update', this.order.id, resp.data);
            this.changeCostVisible = false;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      addExtraProfit() {
        salesProfitCreate({ id: this.order.id, ...this.addForm })
          .then((resp) => {
            this.$message.success('添加成功');
            this.$emit('create', this.order.id, resp.data);
            this.addExtraProfitVisible = false;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      deleteExtraProfit(item) {
        salesProfitDestroy({ id: item.id })
          .then(() => {
            this.$message.success('删除成功');
            this.$emit('destroy', this.order.id, item);
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      resetForm() {
        this.changeForm = {
          purchase_price: 0,
        };

        this.addForm = {
          amount: 0,
          remark: '',
        };
      },
    },
  }
</script>

<style scoped>
</style>