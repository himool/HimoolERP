<template>
  <div>
    <a-row gutter="8">
      <a-col :span="8">
        <a-card>
          <a-row gutter="16">
            <a-col :span="12" style="margin-bottom: 8px">
              <a-select
                v-model="searchForm.warehouse"
                placeholder="仓库"
                style="width: 100%"
                allowClear
              >
                <a-select-option
                  v-for="item in warehouseItems"
                  :key="item.id"
                  :value="item.id"
                  >{{ item.name }}
                </a-select-option>
              </a-select>
            </a-col>
            <a-col :span="12" style="margin-bottom: 8px">
              <a-select
                v-model="searchForm.is_return"
                placeholder="单据类型"
                style="width: 100%"
                allowClear
              >
                <a-select-option :value="false">采购单</a-select-option>
                <a-select-option :value="true">采购退货单</a-select-option>
              </a-select>
            </a-col>
            <a-col :span="24" style="margin-bottom: 16px">
              <a-input-search
                v-model="searchForm.search"
                allowClear
                enter-button
                @search="search"
                placeholder="供应商姓名 / 联系人 / 订单备注"
              />
            </a-col>
          </a-row>
          <a-row>
            <a-table
              :columns="purchaseColumns"
              :data-source="items"
              :loading="loading"
              :pagination="false"
              ref="purchaseColumnsTable"
              :customRow="customRow"
              :rowClassName="rowClassName"
              size="small"
            >
              <div slot="status" slot-scope="value, item">
                {{ item.is_return ? "退货单" : "采购单" }} -
                {{
                  item.is_done
                    ? "已完成"
                    : item.is_return
                    ? "等待出库"
                    : "等待入库"
                }}
              </div>
              <div slot="date" slot-scope="value">
                {{ moment(value).format("YYYY-MM-DD") }}
              </div>
            </a-table>
            <div style="text-align: center; margin-top: 16px">
              <a-pagination
                v-model="searchForm.page"
                :total="totalRows"
                :pageSize="perPage"
                show-less-items
                @change="changePage"
              />
            </div>
          </a-row>
        </a-card>
      </a-col>
      <a-col :span="16">
        <a-card
          :title="
            form.id
              ? form.is_return
                ? `采购退货单 - ${form.id}`
                : `采购单 - ${form.id}`
              : '采购单'
          "
        >
          <!-- <div v-if="form.is_return">
            <div
              v-if="formLoading"
              style="text-align: center; margin-top: 36px"
            >
              <a-spin />
            </div>
            <div v-else>
              <a-row style="margin: 6px 0">
                <a-col :span="24" style="font-size: 15px; font-weight: 500"
                  >关联采购单: {{ purchaseForm.id }}</a-col
                >
                <a-col :span="6"
                  >供应商: {{ purchaseForm.supplier_name }}</a-col
                >
                <a-col :span="6">仓库: {{ purchaseForm.warehouse_name }}</a-col>
                <a-col :span="6"
                  >结算账户: {{ purchaseForm.account_name }}</a-col
                >
                <a-col :span="6">实付金额: {{ purchaseForm.amount }}</a-col>
                <a-col :span="6"
                  >采购员: {{ purchaseForm.contacts_name }}</a-col
                >
                <a-col :span="12">备注: {{ purchaseForm.remark }}</a-col>
              </a-row>
              <a-row style="margin-top: 12px">
                <a-table
                  :columns="purchaseColumns"
                  :data-source="purchaseForm.goods_set"
                  :pagination="false"
                  size="small"
                />
              </a-row>
            </div>
            <a-divider />
          </div> -->
          <a-row style="margin: 6px 0">
            <a-col :span="6">供应商: {{ purchaseForm.supplier_name }}</a-col>
            <a-col :span="6">仓库: {{ purchaseForm.warehouse_name }}</a-col>
            <a-col :span="6">结算账户: {{ purchaseForm.account_name }}</a-col>
            <a-col :span="6">实付金额: {{ purchaseForm.amount }}</a-col>
            <a-col :span="6">采购员: {{ purchaseForm.contacts_name }}</a-col>
            <a-col :span="12">备注: {{ purchaseForm.remark }}</a-col>
          </a-row>
          <a-row style="margin-top: 12px">
            <a-table
              :columns="goodsColumns"
              :data-source="dataSource"
              :pagination="false"
              size="small"
            >
              <div slot="index" slot-scope="value, item, index">
                {{ item.isTotal ? "" : index + 1 }}
              </div>
              <div slot="purchase_price" slot-scope="value, item">
                {{ item.isTotal ? "" : NP.round(value, 2) }}
              </div>
              <div slot="amount" slot-scope="value, item">
                {{
                  item.isTotal
                    ? value
                    : NP.round(NP.times(item.quantity, item.purchase_price), 2)
                }}
              </div>
            </a-table>
          </a-row>
          <a-row style="margin-top: 12px">
            <a-popconfirm title="确定删除吗?" @confirm="destroy">
              <a-button v-if="form.id && !form.is_done" type="danger"
                >删除</a-button
              >
            </a-popconfirm>
            <a-button
              v-if="form.id && form.is_done"
              style="margin-left: 12px"
              @click="printInvoice"
              >生成打印单据</a-button
            >
          </a-row>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { warehouseList } from "@/api/warehouse";
import {
  purchaseOrderList,
  purchaseOrderRetrieve,
  purchaseOrderDestroy,
} from "@/api/purchase";
import NP from "number-precision";
import moment from "moment";

export default {
  name: "PurchaseRecord",
  data() {
    return {
      NP,
      moment,
      searchForm: {
        search: "",
        is_return: undefined,
        warehouse: undefined,
        page: 1,
      },
      totalRows: 0,
      perPage: 16,
      loading: false,
      warehouseItems: [],
      form: {},
      purchaseForm: {},
      formLoading: false,
      purchaseColumns: [
        {
          title: "状态",
          dataIndex: "status",
          key: "status",
          scopedSlots: { customRender: "status" },
        },
        {
          title: "日期",
          dataIndex: "date",
          key: "date",
          scopedSlots: { customRender: "date" },
        },
        {
          title: "供应商",
          dataIndex: "supplier_name",
          key: "supplier_name",
        },
      ],
      goodsColumns: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          scopedSlots: { customRender: "index" },
        },
        {
          title: "编号",
          dataIndex: "code",
          key: "code",
        },
        {
          title: "商品",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "规格",
          dataIndex: "spec",
          key: "spec",
        },
        {
          title: "单位",
          dataIndex: "unit",
          key: "unit",
        },
        {
          title: "数量",
          dataIndex: "quantity",
          key: "quantity",
        },
        {
          title: "单价(元)",
          dataIndex: "purchase_price",
          key: "purchase_price",
        },
        {
          title: "金额(元)",
          dataIndex: "amount",
          key: "amount",
          customRender: (value) => {
            return NP.round(value, 2);
          },
        },
      ],
    };
  },
  computed: {
    dataSource() {
      if (!this.form.goods_set) return;
      // 统计合计
      let totalQuantity = 0,
        totalAmount = 0,
        totalDiscountAmount = 0;
      for (let item of this.form.goods_set) {
        totalQuantity = NP.plus(totalQuantity, item.quantity);
        let amount = NP.times(item.quantity, item.purchase_price);
        totalAmount = NP.plus(totalAmount, amount);
        totalDiscountAmount = NP.plus(
          totalDiscountAmount,
          NP.times(amount, item.discount, 0.01)
        );
      }

      return [
        ...this.form.goods_set,
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
    initialize() {
      if (this.$route.query.search) {
        this.searchForm.search = this.$route.query.search;
      }

      var that = this;
      this.list();
      warehouseList().then((resp) => {
        that.warehouseItems = resp.data;
      });
    },
    list() {
      this.loading = true;
      var that = this;
      purchaseOrderList(this.searchForm)
        .then((resp) => {
          that.totalRows = resp.data.count;
          that.items = resp.data.results;
        })

        .finally(() => {
          that.loading = false;
          that.clickFristRow();
        });
    },
    clickFristRow() {
      if (this.$refs["purchaseColumnsTable"]) {
        let $e = this.$refs["purchaseColumnsTable"];
        if (this.items && this.items.length > 0) {
          if (
            $e.$el.getElementsByClassName("ant-table-row") &&
            $e.$el.getElementsByClassName("ant-table-row").length > 0
          ) {
            $e.$el.getElementsByClassName("ant-table-row")[0].click();
          }
        }
      }
    },
    retrieve() {
      this.purchaseForm = {};
      this.formLoading = true;
      var that = this;
      purchaseOrderRetrieve({ id: this.form.id }).then((resp) => {
        if (resp.data.id == that.form.id) {
          that.purchaseForm = resp.data;
          that.formLoading = false;
        }
      });
    },
    destroy() {
      let form = { ...this.form };
      var that = this;
      purchaseOrderDestroy(form).then(() => {
        that.$message.success("删除成功");
        that.items.splice(
          that.items.findIndex((item) => item.id === form.id),
          1
        );
        that.form = {};
      });
    },
    search() {
      this.searchForm.page = 1;
      this.list();
    },
    changePage(value) {
      this.searchForm.page = value;
      this.list();
    },
    printInvoice() {
      window.open(`/invoice/purchase?id=${this.form.id}`);
    },
    customRow(item) {
      var that = this;
      return {
        on: {
          click: () => {
            that.form = { ...item };
            that.retrieve();
          },
        },
      };
    },
    rowClassName(item) {
      if (item.id == this.form.id) {
        return "table-selected";
      }
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scope>
.table-selected {
  background: #e6f7ff;
}
</style>