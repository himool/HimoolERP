<template>
  <div>
    <a-card title="采购单">
      <div>
        <a-form-model
          ref="form"
          :model="form"
          :rules="rules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 18 }"
        >
          <a-row>
            <a-col :span="8">
              <a-form-model-item prop="supplier" label="供应商">
                <a-select v-model="form.supplier">
                  <a-select-option
                    v-for="item in supplierItems"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="warehouse" label="仓库">
                <a-select v-model="form.warehouse">
                  <a-select-option
                    v-for="item in warehouseItems"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="contacts" label="采购员">
                <a-select v-model="form.contacts">
                  <a-select-option
                    v-for="item in userItems"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
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
              <a-form-model-item prop="total_amount" label="总计金额(元)">
                <a-input-number
                  :disabled="true"
                  v-model="form.total_amount"
                  
                  style="width: 100%"
                />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item prop="amount" label="实付金额(元)">
                <a-input-number
                  v-model="form.amount"
                  
                  style="width: 100%"
                />
              </a-form-model-item>
            </a-col>
            <a-col :span="8">
              <a-form-model-item
                prop="remark"
                label="备注"
              >
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
            <a-divider />
            <a-col :span="24">
              <a-form-model-item style="float: right">
                <a-button type="primary" icon="plus" @click="addGoods"
                  >添加商品</a-button
                >
              </a-form-model-item>
            <ScanCode @list="selectGoods"></ScanCode>
            </a-col>
          </a-row>
        </a-form-model>
        <a-row>
          <a-col :span="24">
          </a-col>
        </a-row>
      </div>

      <div>
        <a-table
          :columns="columns"
          :data-source="goodsData"
          :pagination="false"
        >
          <div slot="quantity" slot-scope="value, item">
            <div v-if="item.isTotal">{{ value }}</div>
            <a-input-number v-else v-model="item.quantity" :precision="0" />
          </div>
          <div slot="purchase_price" slot-scope="value, item">
            <a-input-number
              v-if="!item.isTotal"
              v-model="item.purchase_price"
              
            />
          </div>
          <div slot="discount" slot-scope="value, item">
            <a-input-number
              v-if="!item.isTotal"
              v-model="item.discount"
              :precision="1"
              :step="5"
            />
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
        <a-popconfirm title="确定采购吗?" @confirm="createOrder">
          <a-button type="primary" :loading="loading">采购</a-button>
        </a-popconfirm>
      </div>
    </a-card>

    <select-goods-modal v-model="visible" @select="selectGoods" />
  </div>
</template>

<script>
import { supplierList, purchaseOrderCreate } from "@/api/purchase";
import { accountList, userList } from "@/api/account";
import { warehouseList } from "@/api/warehouse";
import { columns } from "./columns";
import { rules } from "./rules";
import NP from "number-precision";
import moment from "moment";

export default {
  components: {
    SelectGoodsModal: () =>
      import("@/components/SelectGoodsModal/SelectGoodsModal"),
    ScanCode: () => import("@/components/ScanCode/ScanCode"),
  },
  data() {
    return {
      form: {
        date: moment().local().format(this.dateTimeFormat),
      },
      goodsItems: [],
      moment,
      loading: false,
      columns,
      rules,
      visible: false,
      dateTimeFormat: "YYYY-MM-DD HH:mm:ss",
      supplierItems: [],
      warehouseItems: [],
      accountItems: [],
      userItems: [],
    };
  },
  computed: {
    goodsData() {
      // 统计合计
      let totalQuantity = 0,
        totalAmount = 0,
        totalDiscountAmount = 0;
      for (let item of this.goodsItems) {
        totalQuantity = NP.plus(totalQuantity, item.quantity);
        let amount = NP.times(item.quantity, item.purchase_price);
        totalAmount = NP.plus(totalAmount, amount);
        totalDiscountAmount = NP.plus(
          totalDiscountAmount,
          NP.times(amount, item.discount, 0.01)
        );
      }
      this.$set(this.form,'total_amount',totalAmount);
      this.$set(this.form,'amount',totalAmount);
      return [
        ...this.goodsItems,
        {
          isTotal: true,
          name: "合计:",
          quantity: totalQuantity,
          amount: totalAmount,
          discount_amount: totalDiscountAmount,
        },
      ];
    },
  },
  methods: {
    initData() {
      this.resetForm();
      var that = this;
      warehouseList()
        .then((resp) => {
          that.warehouseItems = resp.data;
          // 选择器默认选择第一个
          if (that.warehouseItems && that.warehouseItems.length > 0) {
            that.$set(this.form, "warehouse", that.warehouseItems[0].id);
          }
        })
       

      supplierList()
        .then((resp) => {
          this.supplierItems = resp.data;
        })
        

      accountList()
        .then((resp) => {
          this.accountItems = resp.data;
        })
        
      userList()
        .then((resp) => {
          this.userItems = resp.data;
        })
        
    },
    addGoods() {
      this.visible = true;
    },
    removeGoods(item) {
      let index = this.goodsItems.findIndex((_item) => _item.id == item.id);
      if (index != -1) this.goodsItems.splice(index, 1);
    },
    selectGoods(item) {
      if (Array.isArray(item)) {
        var that = this;
        var items = item;
        items.forEach((item)=>{
         var hasResult = null;
        if ( hasResult = this.goodsItems.find((goodsItem)=>{
          return goodsItem.id == item.id;
        })) {
          hasResult.quantity += 1;
        } else {
          this.goodsItems.push({
            index: this.goodsItems.length + 1,
            id: item.id,
            code: item.code,
            name: item.name,
            spec: item.spec,
            unit: item.unit,
            quantity: 1,
            purchase_price: item.purchase_price,
            discount: 100,
          });
        }
        });
      } else {
        var hasResult = null;
        if ( hasResult = this.goodsItems.find((goodsItem)=>{
          return goodsItem.id == item.id;
        })) {
          hasResult.quantity += 1;
        } else {
          this.goodsItems.push({
            index: this.goodsItems.length + 1,
            id: item.id,
            code: item.code,
            name: item.name,
            spec: item.spec,
            unit: item.unit,
            quantity: 1,
            purchase_price: item.purchase_price,
            discount: 100,
          });
        }
        }
    },
    createOrder() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.goodsItems.length == 0) {
            this.$message.error("请选择条目");
            return;
          }

          this.loading = true;
          let form = { ...this.form, goods_set: this.goodsItems };
          purchaseOrderCreate(form)
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
      this.form = { date: moment().format(this.dateTimeFormat) };
      this.goodsItems = [];
    },
  },
  mounted() {
    this.initData();
  },
};
</script>