<template>
  <div>
    <a-card title="销售退货单">
      <div>
        <a-form-model
          ref="form"
          :model="form"
          :rules="rules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 18 }"
        >
          <a-row>
            <a-col :span="8" v-if="false" >
              <a-form-model-item prop="sales_order" label="关联销售单">
                <a-button style="width: 100%" @click="relateOrder">
                  {{ form.sales_order ? form.sales_order : "关联" }}
                </a-button>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="client_name" label="客户">
                <a-button style="width: 100%" @click="addClient">{{
                  form.client_name ? form.client_name : "选择客户"
                }}</a-button>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="warehouse" label="仓库">
                <StorehouseSelected
                  :value="form.warehouse"
                  :disabled="form.sales_order"
                  @change="
                    (nv) => {
                      $set(form, 'warehouse', nv);
                    }
                  "
                ></StorehouseSelected>
              </a-form-model-item>
            </a-col>
              <a-col :span="8">
              <a-form-model-item prop="seller" label="销售员">
                <a-select v-model="form.seller">
                  <a-select-option
                    v-for="item in sellerItems"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col :span="8">
              <a-form-model-item prop="date" label="日期">
                <a-date-picker
                  v-model="form.date"
                  show-time
                  :default-value="moment().local().format(dateTimeFormat)"
                  :format="dateTimeFormat"
                  style="width: 100%"
                />
              </a-form-model-item>
            </a-col>
         <a-col :span="8">
              <a-form-model-item prop="discount" label="整单折扣(%)">
                <a-input-number
                  v-model="form.discount"
                  :precision="1"
                  :step="5"
                  style="width: 100%"
                />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="account" label="结算账户">
                <a-select v-model="form.account">
                  <a-select-option
                    v-for="item in accountItems"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="amount" label="实退金额(元)">
                <a-input-number v-model="form.amount" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-divider />
            <a-col :span="24" v-if="!form.sales_order">
              <a-form-model-item style="float: right">
                <a-button type="primary" icon="plus" @click="addGoods"
                  >添加商品</a-button
                >
              </a-form-model-item>
              <ScanCode v-if="false" @list="selectGoods"></ScanCode>
            </a-col>
          </a-row>
        </a-form-model>
      </div>

      <div>
        <a-table
          :columns="returnColumns"
          :data-source="goodsData"
          :pagination="false"
        >
          <div slot="quantity" slot-scope="value, item">
            <div v-if="item.isTotal">{{ value }}</div>
            <a-input-number v-else v-model="item.quantity" :precision="0" />
          </div>
          <div slot="retail_price" slot-scope="value, item">
            <a-input-number v-if="!item.isTotal" v-model="item.retail_price" />
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button
              v-if="!item.isTotal"
              type="danger"
              @click="removeGoods(item)"
              >删除</a-button
            >
          </div>
        </a-table>
      </div>

      <div style="margin-top: 16px">
        <a-popconfirm title="确定退货吗?" @confirm="createOrder">
          <a-button type="primary" :loading="loading">退货</a-button>
        </a-popconfirm>
      </div>
    </a-card>

    <select-goods-modal v-model="goodsVisible" @select="selectGoods" />
    <select-sales-order-modal v-model="orderVisible" @select="selectOrder" />
    <select-client-modal v-model="clientVisible" @select="selectClient" />
  </div>
</template>

<script>
import { salesColumns, returnColumns } from "./columns";
import { salesOrderCreate } from "@/api/sales";
import { accountList, userList } from "@/api/account";
import NP from "number-precision";
import { rules } from "./rules";
import moment from "moment";

export default {
  components: {
    SelectGoodsModal: () =>
      import("@/components/SelectGoodsModal/SelectGoodsModal"),
    SelectSalesOrderModal: () =>
      import("@/components/SelectSalesOrderModal/SelectSalesOrderModal"),
    ScanCode: () => import("@/components/ScanCode/ScanCode"),
    StorehouseSelected: () => import("@/components/Fields/StorehouseSelected"),
    SelectClientModal: () =>
      import("@/components/SelectClientModal/SelectClientModal"),
  },
  data() {
    return {
      clientVisible: false,
      moment,
      dateTimeFormat: "YYYY-MM-DD HH:mm:ss",
      form: { discount: 100 },
      salesGoodsItems: [],
      loading: false,
      salesColumns,
      returnColumns,
      rules,
      goodsVisible: false,
      orderVisible: false,

      accountItems: [],
      sellerItems: [],
    };
  },
  computed: {
    goodsData() {
      // 统计合计
      let totalQuantity = 0,
        totalAmount = 0;
      for (let item of this.salesGoodsItems) {
        totalQuantity = NP.plus(totalQuantity, item.quantity);
        let amount = NP.times(item.quantity, item.retail_price);
        totalAmount = NP.plus(totalAmount, amount);
      }
      this.$set(this.form, "amount", NP.times(
            totalAmount,
            this.form.discount,
            0.01
          ));
      return [
        ...this.salesGoodsItems,
        {
          isTotal: true,
          name: "合计:",
          quantity: totalQuantity,
          amount: `${totalAmount} * ${this.form.discount}% = ${NP.times(
            totalAmount,
            this.form.discount,
            0.01
          )}`,
        },
      ];
    },
  },
  methods: {
    addClient() {
      this.clientVisible = true;
    },
    selectClient(item) {
      this.$set(this.form, "client_contacts", item.contacts);
      this.$set(this.form, "client_phone", item.phone);
      this.$set(this.form, "client_name", item.name);
      this.$set(this.form, "client_address", item.address);
    },
    initData() {
      this.resetForm();

      accountList().then((resp) => {
        this.accountItems = resp.data;
      });

      userList().then((resp) => {
        this.sellerItems = resp.data;
      });
    },
    relateOrder() {
      this.orderVisible = true;
    },
    selectOrder(item) {
      this.$set(this.form, "sales_order", item.id);
      this.$set(this.form, "client_contacts", item.client_contacts);
      this.$set(this.form, "client_name", item.client_name);
      this.$set(this.form, "client_phone", item.client_phone);
      this.$set(this.form, "client_address", item.client_address);
      this.$set(this.form, "warehouse", item.warehouse);
      this.$set(this.form, "warehouse_name", item.warehouse_name);
      this.salesGoodsItems = item.goods_set;
    },
    addGoods() {
      this.goodsVisible = true;
    },
    removeGoods(item) {
      let index = this.salesGoodsItems.findIndex(
        (_item) => _item.id == item.id
      );
      if (index != -1) this.salesGoodsItems.splice(index, 1);
    },
    selectGoods(item) {
      if (Array.isArray(item)) {
        var that = this;
        var items = item;
        items.forEach((item) => {
          var hasResult = null;
          if (
            (hasResult = this.salesGoodsItems.find((goodsItem) => {
              return goodsItem.id == item.id;
            }))
          ) {
            hasResult.quantity += 1;
          } else {
            this.salesGoodsItems.push({
              index: this.salesGoodsItems.length + 1,
              id: item.id,
              code: item.code,
              name: item.name,
              spec: item.spec,
              unit: item.unit,
              quantity: 1,
              retail_price: item.retail_price,
            });
          }
        });
      } else {
        var hasResult = null;
        if (
          (hasResult = this.salesGoodsItems.find((goodsItem) => {
            return goodsItem.id == item.id;
          }))
        ) {
          hasResult.quantity += 1;
        } else {
          this.salesGoodsItems.push({
            index: this.salesGoodsItems.length + 1,
            id: item.id,
            code: item.code,
            name: item.name,
            spec: item.spec,
            unit: item.unit,
            quantity: 1,
            retail_price: item.retail_price,
            discount: 100,
          });
        }
      }
    },
    createOrder() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.salesGoodsItems.length == 0) {
            this.$message.error("请选择条目");
            return;
          }

          this.loading = true;
          let form = { ...this.form, goods_set: this.salesGoodsItems };
          console.log(form);
          salesOrderCreate(form)
            .then(() => {
              this.$message.success("新增成功");
              this.resetForm();
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    resetForm() {
      this.form = {
        discount: 100,
        date: moment().format(this.dateTimeFormat),
        is_return: true,
      };
      this.salesGoodsItems = [];
    },
  },
  watch:{
      'form.discount': {
    handler(newVal,oldVal) {
      var currentAmount = this.form.amount / (oldVal / 100) * (newVal / 100);
      this.$set(this.form,'amount',currentAmount);
    },
    deep: true
  },
  'form.amount': {
    handler(newVal,oldVal) {
      
    },
    deep: true
  },
  },
  mounted() {
    this.initData();
  },
};
</script>