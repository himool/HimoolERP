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
                <a-select-option :value="false">销售单</a-select-option>
                <a-select-option :value="true">销售退货单</a-select-option>
              </a-select>
            </a-col>
            <a-col :span="24" style="margin-bottom: 16px">
              <a-input-search
                v-model="searchForm.search"
                allowClear
                enter-button
                @search="search"
                placeholder="客户姓名 / 联系电话 / 销售员/ 订单备注"
              />
            </a-col>
          </a-row>
          <a-row>
            <a-table
              :columns="salesColumns"
              :data-source="items"
              :loading="loading"
              :pagination="false"
              :customRow="customRow"
              :rowClassName="rowClassName"
              size="small"
              ref="salesColumnsTable"
            >
              <div slot="status" slot-scope="value, item">
                {{ item.is_return ? "退货单" : "销售单" }} -
                {{
                  item.is_done
                    ? "已完成"
                    : item.is_return
                    ? "等待入库"
                    : "等待出库"
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
                ? `销售退货单 - ${form.id}`
                : `销售单 - ${form.id}`
              : '销售单'
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
                  >关联销售单: {{ salesForm.id }}</a-col
                >
              </a-row>
              <a-row style="margin: 6px 0">
                <a-col :span="6">仓库: {{ salesForm.warehouse_name }}</a-col>
                <a-col :span="6">结算账户: {{ salesForm.account_name }}</a-col>
                <a-col :span="6">整单折扣(%): {{ salesForm.discount }}</a-col>
                <a-col :span="6">实收金额: {{ salesForm.amount }}</a-col>
              </a-row>
              <a-row style="margin: 6px 0">
                <a-col :span="6">销售员: {{ salesForm.seller_name }}</a-col>
                <a-col :span="6">客户名称: {{ salesForm.client_name }}</a-col>
                <a-col :span="6">销售员: {{ salesForm.client_contacts }}</a-col>
                <a-col :span="6">电话: {{ salesForm.client_phone }}</a-col>
              </a-row>
              <a-row style="margin: 6px 0">
                <a-col :span="12">地址: {{ salesForm.client_address }}</a-col>
                <a-col :span="12">备注: {{ salesForm.remark }}</a-col>
              </a-row>
              <a-row style="margin-top: 12px">
                <a-table
                  :columns="goodsColumns"
                  :data-source="salesForm.goods_set"
                  :pagination="false"
                  size="small"
                >
                  <div slot="index" slot-scope="value, item, index">
                    {{ index + 1 }}
                  </div>
                  <div slot="retail_price" slot-scope="value">
                    {{ NP.round(value, 2) }}
                  </div>
                  <div slot="amount" slot-scope="value, item">
                    {{
                      NP.round(NP.times(item.quantity, item.retail_price), 2)
                    }}
                  </div>
                </a-table>
              </a-row>
            </div>
            <a-divider />
          </div> -->
          <a-row style="margin: 6px 0">
            <a-col :span="6">仓库: {{ form.warehouse_name }}</a-col>
            <a-col :span="6">结算账户: {{ form.account_name }}</a-col>
            <a-col :span="6">整单折扣(%): {{ form.discount }}</a-col>
            <a-col :span="6">实收金额(元): {{ form.amount }}</a-col>
          </a-row>
          <a-row style="margin: 6px 0">
            <a-col :span="6">销售员: {{ form.seller_name }}</a-col>
            <a-col :span="6">客户名称: {{ form.client_name }}</a-col>
            <a-col :span="6">联系人: {{ form.client_contacts }}</a-col>
            <a-col :span="6">电话: {{ form.client_phone }}</a-col>
          </a-row>
          <a-row style="margin: 6px 0">
            <a-col :span="12">地址: {{ form.client_address }}</a-col>
            <a-col :span="12">备注: {{ form.remark }}</a-col>
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
              <div slot="retail_price" slot-scope="value, item">
                {{ item.isTotal ? "" : NP.round(value, 2) }}
              </div>
              <div slot="amount" slot-scope="value, item">
                {{
                  item.isTotal
                    ? value
                    : NP.round(NP.times(item.quantity, item.retail_price), 2)
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
  salesOrderList,
  salesOrderRetrieve,
  salesOrderDestroy,
} from "@/api/sales";
import NP from "number-precision";
import moment from "moment";

export default {
  name: "SalesRecord",
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
      salesForm: {},
      formLoading: false,
      salesColumns: [
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
          title: "销售员",
          dataIndex: "seller_name",
          key: "seller_name",
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
          dataIndex: "retail_price",
          key: "retail_price",
          scopedSlots: { customRender: "retail_price" },
        },
        {
          title: "金额(元)",
          dataIndex: "amount",
          key: "amount",
          scopedSlots: { customRender: "amount" },
        },
        {
          title: "备注",
          dataIndex: "remark",
          key: "remark",
        },
      ],
    };
  },
  computed: {
    dataSource() {
      let totalQuantity = 0,
        totalAmount = 0;
      if (this.form.goods_set) {
        for (let item of this.form.goods_set) {
          totalQuantity += item.quantity;
          totalAmount = NP.times(item.quantity, item.retail_price);
        }
      }

      let totalItem = {
        name: "合计:",
        quantity: totalQuantity,
        amount: NP.times(
          totalAmount,
          this.form.discount ? this.form.discount : 100,
          0.01
        ),
        isTotal: true,
      };

      return this.form.goods_set
        ? [...this.form.goods_set, totalItem]
        : [totalItem];
    },
  },
  methods: {
    initialize() {
      if (this.$route.query.search) {
        this.searchForm.search = this.$route.query.search;
      }

      this.list();
      warehouseList().then((resp) => {
        this.warehouseItems = resp.data;
      });
    },
    list() {
      this.loading = true;
      salesOrderList(this.searchForm)
        .then((resp) => {
          this.totalRows = resp.data.count;
          this.items = resp.data.results;
        })

        .finally(() => {
          this.loading = false;
          this.clickFristRow();
        });
    },
    clickFristRow() {
      if (this.$refs["salesColumnsTable"]) {
        let $e = this.$refs["salesColumnsTable"];
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
      this.salesForm = {};
      this.formLoading = true;
      salesOrderRetrieve({ id: this.form.sales_order }).then((resp) => {
        if (resp.data.id == this.form.sales_order) {
          this.salesForm = resp.data;
          this.formLoading = false;
        }
      });
    },
    destroy() {
      let form = { ...this.form };
      salesOrderDestroy(form).then(() => {
        this.$message.success("删除成功");
        this.items.splice(
          this.items.findIndex((item) => item.id === form.id),
          1
        );
        this.form = {};
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
      window.open(`/invoice/sales?id=${this.form.id}`);
    },
    customRow(item) {
      return {
        on: {
          click: () => {
            this.form = { ...item };
            if (this.form.is_return) {
              // this.retrieve();
            }
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