<template>
  <div>
    <a-card title="采购退货单">
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
          <a-row>
            <a-col :span="8">
              <a-form-model-item prop="purchase_order" label="关联采购单">
                <a-button style="width: 100%;" @click="relateOrder">
                  {{ form.purchase_order ? form.purchase_order : '关联' }}
                </a-button>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="supplier" label="供应商">
                <a-input :value="form.supplier_name" disabled />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="warehouse" label="仓库">
                <a-input :value="form.warehouse_name" disabled />
              </a-form-model-item>
            </a-col>
          </a-row>

          <a-table :columns="purchaseColumns" :data-source="purchaseGoodsItems" :pagination="false">
            <div slot="index" slot-scope="value, item, index">{{ index + 1 }}</div>
          </a-table>

          <a-row style="margin-top: 48px;">
            <a-col :span="8">
              <a-form-model-item prop="account" label="结算账户">
                <a-select v-model="form.account">
                  <a-select-option v-for="item in accountItems" :key="item.id" :value="item.id">
                    {{item.name}}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="contacts" label="联系人">
                <a-select v-model="form.contacts">
                  <a-select-option v-for="item in userItems" :key="item.id" :value="item.id">
                    {{item.username}}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="date" label="日期">
                <a-date-picker v-model="form.date" valueFormat="YYYY-MM-DD" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="amount" label="实付金额">
                <a-input-number v-model="form.amount" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item style="float: right;">
                <a-button type="primary" icon="plus" @click="addGoods">添加条目</a-button>
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
      </div>

      <div>
        <a-table :columns="returnColumns" :data-source="goodsData" :pagination="false">
          <div slot="quantity" slot-scope="value, item">
            <div v-if="item.isTotal">{{ value }}</div>
            <a-input-number v-else v-model="item.quantity" :precision="0" />
          </div>
          <div slot="purchase_price" slot-scope="value, item">
            <a-input-number v-if="!item.isTotal" v-model="item.purchase_price" :precision="2" />
          </div>
          <div slot="discount" slot-scope="value, item">
            <a-input-number v-if="!item.isTotal" v-model="item.discount" :precision="1" :step="5" />
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button v-if="!item.isTotal" type="danger" @click="removeGoods(item)">删除</a-button>
          </div>
        </a-table>
      </div>

      <div style="margin-top: 16px;">
        <a-popconfirm title="确定退货吗?" @confirm="createOrder">
          <a-button type="primary" :loading="loading">退货</a-button>
        </a-popconfirm>
      </div>
    </a-card>

    <select-goods-modal v-model="goodsVisible" @select="selectGoods" />
    <select-purchase-order-modal v-model="orderVisible" @select="selectOrder" />
  </div>
</template>

<script>
  import { purchaseColumns, returnColumns } from './columns';
  import { purchaseOrderCreate } from '@/api/purchase';
  import { accountList, userList } from '@/api/account';
  import NP from 'number-precision';
  import { rules } from './rules';
  import moment from 'moment';

  export default {
    components: {
      SelectGoodsModal: () => import('@/components/SelectGoodsModal/SelectGoodsModal'),
      SelectPurchaseOrderModal: () => import('@/components/SelectPurchaseOrderModal/SelectPurchaseOrderModal'),
    },
    data() {
      return {
        form: {},
        purchaseGoodsItems: [],
        returnGoodsItems: [],
        loading: false,
        purchaseColumns,
        returnColumns,
        rules,
        goodsVisible: false,
        orderVisible: false,

        accountItems: [],
        userItems: [],
      };
    },
    computed: {
      goodsData() {
        // 统计合计
        let totalQuantity = 0, totalAmount = 0, totalDiscountAmount = 0;
        for (let item of this.returnGoodsItems) {
          totalQuantity = NP.plus(totalQuantity, item.quantity);
          let amount = NP.times(item.quantity, item.purchase_price);
          totalAmount = NP.plus(totalAmount, amount);
          totalDiscountAmount = NP.plus(totalDiscountAmount, NP.times(amount, item.discount, 0.01));
        }

        return [...this.returnGoodsItems, {
          isTotal: true,
          name: '合计:',
          quantity: totalQuantity,
          amount: totalAmount,
          discount_amount: totalDiscountAmount
        }]
      },
    },
    methods: {
      initData() {
        this.resetForm();

        accountList().then(resp => {
          this.accountItems = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        });

        userList().then(resp => {
          this.userItems = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        });
      },
      relateOrder() {
        this.orderVisible = true;
      },
      selectOrder(item) {
        this.form.purchase_order = item.id;
        this.form.supplier = item.supplier;
        this.form.supplier_name = item.supplier_name;
        this.form.warehouse = item.warehouse;
        this.form.warehouse_name = item.warehouse_name;
        this.purchaseGoodsItems = item.goods_set;
        console.log(item);
      },
      addGoods() {
        this.goodsVisible = true;
      },
      removeGoods(item) {
        let index = this.returnGoodsItems.findIndex(_item => _item.id == item.id);
        if (index != -1) this.returnGoodsItems.splice(index, 1);
      },
      selectGoods(item) {
        this.returnGoodsItems.push({
          index: this.returnGoodsItems.length + 1,
          id: item.id,
          code: item.code,
          name: item.name,
          specification: item.specification,
          unit: item.unit,
          quantity: 1,
          purchase_price: item.purchase_price,
          discount: 100,
        });
      },
      createOrder() {
        this.$refs.form.validate(valid => {
          if (valid) {
            if (this.returnGoodsItems.length == 0) {
              this.$message.error('请选择条目');
              return
            }

            this.loading = true;
            let form = { ...this.form, goods_set: this.returnGoodsItems };
            purchaseOrderCreate(form).then(() => {
              this.$message.success('新增成功');
              this.resetForm();
            }).catch(err => {
              this.$message.error(err.response.data.message);
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      resetForm() {
        this.form = { amount: 0, date: moment().format('YYYY-MM-DD'), is_return: true };
        this.returnGoodsItems = [];
        this.purchaseGoodsItems = [];
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>