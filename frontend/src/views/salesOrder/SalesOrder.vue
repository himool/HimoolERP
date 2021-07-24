<template>
  <div>
    <a-card title="销售单">
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
          <a-row>
            <a-col :span="8">
              <a-form-model-item prop="discount" label="整单折扣(%)">
                <a-input-number v-model="form.discount" :precision="1" :step="5" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="date" label="日期">
                <a-date-picker v-model="form.date" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="seller" label="销售员">
                <a-select v-model="form.seller">
                  <a-select-option v-for="item in sellerItems" :key="item.id" :value="item.id">{{item.username}}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="warehouse" label="仓库">
                <a-select v-model="form.warehouse">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                    {{item.name}}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
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
              <a-form-model-item prop="amount" label="实收金额">
                <a-input-number v-model="form.amount" :precision="2" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client" label="客户">
                <a-button type="primary" style="width: 100%;" @click="addClient">选择已有客户</a-button>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client_contacts" label="联系人">
                <a-input v-model="form.client_contacts" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client_phone" label="客户手机">
                <a-input v-model="form.client_phone" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client_name" label="客户名称">
                <a-input v-model="form.client_name" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client_address" label="客户地址">
                <a-input v-model="form.client_address" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="remark" label="客户备注">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
            <a-col :span="24">
              <a-form-model-item style="float: right;">
                <a-button type="primary" icon="plus" @click="addGoods">添加条目</a-button>
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>
      </div>

      <div>
        <a-table :columns="columns" :data-source="goodsData" :pagination="false">
          <div slot="quantity" slot-scope="value, item">
            <div v-if="item.isTotal">{{ value }}</div>
            <a-input-number v-else v-model="item.quantity" :precision="0" />
          </div>
          <div slot="retail_price" slot-scope="value, item">
            <a-input-number v-if="!item.isTotal" v-model="item.retail_price" :precision="2" />
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button v-if="!item.isTotal" type="danger" @click="removeGoods(item)">删除</a-button>
          </div>
        </a-table>
      </div>

      <div style="margin-top: 16px;">
        <a-popconfirm title="确定销售吗?" @confirm="createOrder">
          <a-button type="primary" :loading="loading">销售</a-button>
        </a-popconfirm>
      </div>
    </a-card>

    <select-goods-modal v-model="goodsVisible" @select="selectGoods" />
    <select-client-modal v-model="clientVisible" @select="selectClient" />
  </div>
</template>

<script>
  import { accountList, sellertList } from '@/api/account';
  import { warehouseList } from '@/api/warehouse';
  import { salesOrderCreate } from '@/api/sales';
  import { columns } from './columns';
  import { rules } from './rules';
  import NP from 'number-precision';

  export default {
    components: {
      SelectGoodsModal: () => import('@/components/SelectGoodsModal/SelectGoodsModal'),
      SelectClientModal: () => import('@/components/SelectClientModal/SelectClientModal'),
    },
    data() {
      return {
        form: {},
        goodsItems: [],
        loading: false,
        columns,
        rules,
        goodsVisible: false,
        clientVisible: false,

        warehouseItems: [],
        accountItems: [],
        sellerItems: [],
      };
    },
    computed: {
      goodsData() {
        // 统计合计
        let totalQuantity = 0, totalAmount = 0;
        for (let item of this.goodsItems) {
          totalQuantity = NP.plus(totalQuantity, item.quantity);
          let amount = NP.times(item.quantity, item.retail_price);
          totalAmount = NP.plus(totalAmount, amount);
        }

        return [...this.goodsItems, {
          isTotal: true,
          name: '合计:',
          quantity: totalQuantity,
          amount: totalAmount,
        }]
      },
    },
    methods: {
      initData() {
        this.resetForm();

        warehouseList().then(resp => {
          this.warehouseItems = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        });

        accountList().then(resp => {
          this.accountItems = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        });

        sellertList().then(resp => {
          this.sellerItems = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        });
      },
      addGoods() {
        this.goodsVisible = true;
      },
      removeGoods(item) {
        let index = this.goodsItems.findIndex(_item => _item.id == item.id);
        if (index != -1) this.goodsItems.splice(index, 1);
      },
      selectGoods(item) {
        this.goodsItems.push({
          index: this.goodsItems.length + 1,
          id: item.id,
          code: item.code,
          name: item.name,
          specification: item.specification,
          unit: item.unit,
          quantity: 1,
          retail_price: item.retail_price,
        });
      },
      addClient() {
        this.clientVisible = true;
      },
      selectClient(item) {
        this.form.client_contacts = item.contacts;
        this.form.client_phone = item.phone;
        this.form.client_name = item.name;
        this.form.client_address = item.address;
      },
      createOrder() {
        this.$refs.form.validate(valid => {
          if (valid) {
            if (this.goodsItems.length == 0) {
              this.$message.error('请选择条目');
              return
            }

            this.loading = true;
            let form = { ...this.form, goods_set: this.goodsItems };
            salesOrderCreate(form).then(() => {
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
        this.form.discount = 100;
        this.goodsItems = [];
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>