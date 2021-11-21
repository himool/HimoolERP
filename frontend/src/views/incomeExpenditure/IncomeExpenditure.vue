<template>
  <div>
    <a-card title="日常收支">
      <a-tabs v-model="currentTabKey" @change="initailize">
        <a-tab-pane key="income" tab="日常收入">
          <a-row gutter="16">
            <a-col :span="24" :md="6" :xl="6" style="margin-bottom: 12px">
              <a-range-picker
                @change="onSearchChange"
                :default-value="[
                  moment().subtract(1, 'months').add(1,'days').format(dateFormat),
                  moment().format(dateFormat),
                ]"
                :format="dateFormat"
              />
            </a-col>
            <a-col :span="24" :md="6" :xl="6" style="margin-bottom: 12px">
              <a-input
                v-model="searchForm.search"
                placeholder="单号，备注"
                allowClear
                @pressEnter="handleSearch"
              />
            </a-col>
            <a-col :span="24" :md="5" :xl="5" style="margin-bottom: 12px">
              <a-button type="primary" icon="search" @click="handleSearch"
                >查询</a-button
              >
              <a-divider type="vertical" />
               <a-button
              disabled
                @click="
                  $message.warning('功能待完善');
                "
              >
                <a-icon type="plus" />导出
              </a-button>
            </a-col>
            <a-col
              :span="24"
              :md="7"
              :xl="7"
              style="
                margin-bottom: 12px;
                display: flex;
                justify-content: flex-end;
              "
            >
             
              <a-button
                type="primary"
                @click="
                  resetForm();
                  visible = true;
                "
              >
                <a-icon type="plus" />新增收入
              </a-button>
            </a-col>
          </a-row>
          <a-table
            :columns="getColumns"
            :data-source="items"
            size="small"
            :pagination="false"
            :loading="tableLoading"
            @change="handleTableChange"
          >
            <div slot="index" slot-scope="value, item, index">
              {{ index + 1 }}
            </div>
            <div slot="phone" slot-scope="value">
              <a-button
                type="link"
                @click="
                  $router.push({
                    path: '/sales_record',
                    query: { search: value },
                  })
                "
              >
                {{ value }}
              </a-button>
            </div>
            <div slot="status" slot-scope="value, item">
              {{ item.status ? "启用" : "停用" }}
            </div>
            <div slot="action" slot-scope="value, item">
              <a-button-group>
                <a-button
                  size="small"
                  @click="
                    form = { ...item };
                    visible = true;
                  "
                >
                  <a-icon type="edit" />编辑
                </a-button>
                <a-popconfirm
                  :title="`删除仓库: ${item.name}`"
                  ok-text="确认"
                  cancel-text="取消"
                  @confirm="destroy(item)"
                >
                  <a-button type="danger" size="small">
                    <a-icon type="delete" />删除
                  </a-button>
                </a-popconfirm>
              </a-button-group>
            </div>
          </a-table>
          <div style="text-align: center; margin-top: 24px">
            <a-pagination
              :value="searchForm.page"
              :total="totalRows"
              :pageSize="perPage"
              show-less-items
              @change="changePage"
            />
          </div>
        </a-tab-pane>
        <a-tab-pane key="expenditure" tab="日常支出" force-render>
          <a-row gutter="16">
            <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px">
              <a-range-picker
                @change="onSearchChange"
                :default-value="[
                   moment().subtract(1, 'months').add(1,'days').format(dateFormat),
                  moment().format(dateFormat),
                ]"
                :format="dateFormat"
              />
            </a-col>
            <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px">
              <a-input
                v-model="searchForm.number"
                placeholder="单号，备注"
                allowClear
                @pressEnter="handleSearch"
              />
            </a-col>
             <a-col :span="24" :md="5" :xl="5" style="margin-bottom: 12px">
              <a-button type="primary" icon="search" @click="handleSearch"
                >查询</a-button
              >
              <a-divider type="vertical" />
               <a-button
                @click="
                  $message.warning('功能待完善');
                "
                disabled
              >
                <a-icon type="plus" />导出
              </a-button>
            </a-col>
            <a-col
              :span="24"
              :md="7"
              :xl="7"
              style="
                margin-bottom: 12px;
                display: flex;
                justify-content: flex-end;
              "
            >
             
              <a-button
                type="primary"
                @click="
                  resetForm();
                  visible = true;
                "
              >
                <a-icon type="plus" />新增支出
              </a-button>
            </a-col>
          </a-row>
          <a-table
            :columns="getColumns"
            :data-source="items"
            size="small"
            :pagination="false"
            :loading="tableLoading"
            @change="handleTableChange"
          >
            <div slot="index" slot-scope="value, item, index">
              {{ index + 1 }}
            </div>
            <div slot="phone" slot-scope="value">
              <a-button
                type="link"
                @click="
                  $router.push({
                    path: '/sales_record',
                    query: { search: value },
                  })
                "
              >
                {{ value }}
              </a-button>
            </div>
            <div slot="status" slot-scope="value, item">
              {{ item.status ? "启用" : "停用" }}
            </div>
            <div slot="action" slot-scope="value, item">
              <a-button-group>
                <a-button
                  size="small"
                  @click="
                    form = { ...item };
                    visible = true;
                  "
                >
                  <a-icon type="edit" />编辑
                </a-button>
                <a-popconfirm
                  :title="`删除仓库: ${item.name}`"
                  ok-text="确认"
                  cancel-text="取消"
                  @confirm="destroy(item)"
                >
                  <a-button type="danger" size="small">
                    <a-icon type="delete" />删除
                  </a-button>
                </a-popconfirm>
              </a-button-group>
            </div>
          </a-table>
          <div style="text-align: center; margin-top: 24px">
            <a-pagination
              :value="searchForm.page"
              :total="totalRows"
              :pageSize="perPage"
              show-less-items
              @change="changePage"
            />
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-card>

    <a-modal
      v-model="visible"
      :title="getDialogTitle"
      :maskClosable="false"
      :okText="form.id ? '保存' : '新增'"
      cancelText="取消"
      @ok="form.id ? update() : create()"
      @cancel="$refs.form.clearValidate()"
    >
      <a-form-model
        ref="form"
        :model="form"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-model-item prop="number" label="编号">
          <a-input v-model="form.number" />
        </a-form-model-item>
        <a-form-model-item prop="business_time" label="业务日期">
          <a-date-picker
            v-model="form.business_time"
            placeholder="业务日期"
            style="width:100%;"
            show-time
            :format="dateTimeFormat"
            :default-value="moment().format(dateTimeFormat)"
          />
        </a-form-model-item>
        <a-form-model-item
          :prop="currentTabKey == 'income' ? 'client' : 'supplier'"
          :label="currentTabKey == 'income' ? ' 客户' : '供应商'"
        >
          <a-select v-model="form.client" v-if="currentTabKey == 'income'">
            <a-select-option
              v-for="(client, key) in clientList"
              :key="key"
              :value="client.id"
            >
              {{ client.name }}
            </a-select-option>
          </a-select>
          <a-select v-model="form.supplier" v-else>
            <a-select-option
              v-for="(supplier, key) in supplierList"
              :key="key"
              :value="supplier.id"
            >
              {{ supplier.name }}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="operator" label="经手人">
          <a-select v-model="form.operator">
            <a-select-option
              v-for="(user, key) in userList"
              :key="key"
              :value="user.id"
            >
              {{ user.name }}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="project" label="收支项目">
          <a-select v-model="form.project">
            <template
              v-for="(
                incomeExpenditureProject, key
              ) in incomeExpenditureProjectsList"
            >
              <a-select-option
                :key="key"
                :value="incomeExpenditureProject.id"
                v-if="incomeExpenditureProject.category == currentTabKey"
              >
                {{ incomeExpenditureProject.type }}
              </a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
        <a-form-model-item
          prop="account"
          :label="currentTabKey == 'income' ? '结算账户' : '支出账户'"
        >
          <a-select v-model="form.account">
            <a-select-option
              v-for="(account, key) in accountList"
              :key="key"
              :value="account.id"
            >
              {{ account.name }}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item
          prop="total_amount"
          :label="currentTabKey == 'income' ? '应收金额(元)' : '应付金额(元)'"
        >
          <a-input-number   style="width:100%;" v-model="form.total_amount" />
        </a-form-model-item>
        <a-form-model-item
          prop="payment_amount"
          :label="currentTabKey == 'income' ? '实收金额(元)' : '实付金额(元)'"
        >
          <a-input-number
                  style="width:100%;"
           v-model="form.payment_amount" />
        </a-form-model-item>
        <a-form-model-item prop="remark" label="备注">
          <a-input v-model="form.remark" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
import {
  incomeExpendituresList,
  incomeExpendituresCreate,
  incomeExpendituresUpdate,
  incomeExpendituresDestroy,
} from "@/api/incomeExpenditures";
import { clientList } from "@/api/sales";
import { supplierList } from "@/api/purchase";
import { subuserList, accountList } from "@/api/account";
import {
  incomeExpenditureProjectsList,
  incomeExpendituresNumber,
} from "@/api/incomeExpenditures";
import { userList, getInfo } from "@/api/user";
import moment from "moment";
import locale from "ant-design-vue/es/date-picker/locale/zh_CN";

export default {
  name: "IncomeExpenditures",
  data() {
    var that = this;
    clientList()
      .then((resp) => {
        that.clientList = resp.data.results;
      })
     
    supplierList()
      .then((resp) => {
        that.supplierList = resp.data;
      })
     
    subuserList()
      .then((resp) => {
        that.subuserList = resp.data;
      })
      
    userList().then((resp) => {
      that.userList = resp.data;
    });
    getInfo()
      .then((resp) => {
        that.userInfo = resp.data;
        console.log(that.getInfo);
      })
     
    incomeExpenditureProjectsList()
      .then((resp) => {
        that.incomeExpenditureProjectsList = resp.data.results;
      })
      
    accountList()
      .then((resp) => {
        that.accountList = resp.data;
      })
  
    // 表格field
    return {
      pagination: {
        position: "both",
      },
      currentTabKey: "income",
      locale,
      dateFormat: "YYYY-MM-DD",
      dateTimeFormat: "YYYY-MM-DD HH:mm:ss",
      moment,
      form: {
      },
      searchForm: {},
      items: [],
      tableLoading: false,
      totalRows: 0,
      perPage: 16,
      currentPage: 1,
      rules: {
        number: [{ required: true, message: "请输入", trigger: "change" }],
        category: [{ required: true, message: "请输入", trigger: "change" }],
        operator: [{ required: true, message: "请输入", trigger: "change" }],
        project: [{ required: true, message: "请输入", trigger: "change" }],
        account: [{ required: true, message: "请输入", trigger: "change" }],
        total_amount: [
          { required: true, message: "请输入", trigger: "change" },
        ],
        payment_amount: [
          { required: true, message: "请输入", trigger: "change" },
        ],
      },
      visible: false,
    };
  },
  watch: {
    visible(oldV, newV) {
      if (newV != true) {
        var that = this;
        this.$set(this.form, "category", this.currentTabKey);
        this.$set(this.form, "operator", this.userInfo.id);
        if (!this.form.business_time) {
          this.$set(this.form,'business_time',moment().format(this.dateTimeFormat));
        }
        incomeExpendituresNumber()
          .then((resp) => {
            that.$set(that.form, "number", resp.data.number);
          })
       
      }
    },
  },
  methods: {
    onSearchChange(date, dateString) {
      this.searchForm.timeRange = dateString;
    },
    initailize() {
      this.resetForm();
      this.list();
    },
    list() {
      this.tableLoading = true;
      let searchForm = JSON.parse(JSON.stringify(this.searchForm));
      if (searchForm && searchForm.timeRange) {
        var timeRange = searchForm.timeRange;
        if (timeRange) {
          var start_time = timeRange[0];
          var end_time = timeRange[1];
          searchForm.start_time = start_time;
          searchForm.end_time = end_time;
          delete searchForm.timeRange;
        }
      }
      incomeExpendituresList({
        ...searchForm,
        page: this.currentPage,
        category: this.currentTabKey,
      })
        .then((resp) => {
          this.totalRows = resp.data.count;
          this.items = resp.data.results;
        })
       
        .finally(() => {
          this.tableLoading = false;
        });
    },
    getDateTime(date) {
      if (date && typeof date == "object") {
        date = date.format("YYYY-MM-DD HH:mm:ss");
      }
      return date;
    },
    create() {
      var that = this;
      this.$refs.form.validate((valid) => {
        if (valid) {
          // if (this.form.business_time) {
          //   this.form.business_time = this.getDateTime(this.form.business_time);
          // }
          incomeExpendituresCreate(that.form)
            .then((resp) => {
              that.$message.success("新增成功");
              that.items.push(resp.data);
              that.visible = false;
            })
           
        }
      });
    },
    update() {
      var that = this;
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (that.form.business_time) {
            that.form.business_time = that.getDateTime(that.form.business_time);
          }
          incomeExpendituresUpdate(that.form)
            .then((resp) => {
              that.$message.success("修改成功");
              that.items.splice(
                that.items.findIndex((item) => item.id === resp.data.id),
                1,
                resp.data
              );
              that.visible = false;
            })
          
        }
      });
    },
    destroy(item) {
      let form = { ...item };
      incomeExpendituresDestroy(form)
        .then(() => {
          this.$message.success("删除成功");
          this.items.splice(
            this.items.findIndex((item) => item.id === form.id),
            1
          );
          this.visible = false;
        })
        
    },
    search() {
      this.currentPage = 1;
      this.initailize();
    },
    changePage(value) {
      this.currentPage = value;
      this.initailize();
    },
    resetForm() {
      this.form = {
        status: true,
        order: 100,
        start_time:moment().subtract(1, 'months').format(this.dateFormat),
        end_time: moment().format(this.dateFormat),
        
      };
    },
    handleSearch() {
      this.list();
    },
    handleTableChange(pagination, filters, sorter) {
      this.searchForm.ordering = `${sorter.order == "descend" ? "-" : ""}${
        sorter.field
      }`;
      this.list();
    },
  },
  computed: {
    getColumns() {
      if (this.currentTabKey == "income") {
        return [
          {
            title: "序号",
            dataIndex: "index",
            key: "index",
            scopedSlots: { customRender: "index" },
          },
          {
            title: "业务日期",
            dataIndex: "business_time",
            key: "business_time",
          },
          {
            title: "单据编号",
            dataIndex: "number",
            key: "number",
          },
          {
            title: "付款单位（元）",
            dataIndex: "payment_unit",
            key: "payment_unit",
          },
          {
            title: "收支项目",
            dataIndex: "project_type",
            key: "project_type",
            scopedSlots: { customRender: "project_type" },
          },
          {
            title: "应收金额(元)",
            dataIndex: "total_amount",
            key: "total_amount",
          },
          {
            title: "实收金额(元)",
            dataIndex: "payment_amount",
            key: "payment_amount",
          },
          {
            title: "收入账户",
            dataIndex: "account_name",
            key: "account_name",
            scopedSlots: { customRender: "account_name" },
          },
          {
            title: "备注",
            dataIndex: "remark",
            key: "remark",
          },
          {
            title: "操作",
            dataIndex: "action",
            key: "action",
            scopedSlots: { customRender: "action" },
          },
        ];
      } else {
        return [
          {
            title: "序号",
            dataIndex: "index",
            key: "index",
            scopedSlots: { customRender: "index" },
          },
          {
            title: "业务日期",
            dataIndex: "business_time",
            key: "business_time",
          },
          {
            title: "单据编号",
            dataIndex: "number",
            key: "number",
          },
          {
            title: "收款单位(元)",
            dataIndex: "payment_unit",
            key: "payment_unit",
          },
          {
            title: "收支项目",
            dataIndex: "project_type",
            key: "project_type",
            scopedSlots: { customRender: "project_type" },
          },
          {
            title: "应付金额(元)",
            dataIndex: "total_amount",
            key: "total_amount",
          },
          {
            title: "实付金额(元)",
            dataIndex: "payment_amount",
            key: "payment_amount",
          },
          {
            title: "支出账户",
            dataIndex: "account_name",
            key: "account_name",
            scopedSlots: { customRender: "account_name" },
          },
          {
            title: "备注",
            dataIndex: "remark",
            key: "remark",
          },
          {
            title: "操作",
            dataIndex: "action",
            key: "action",
            scopedSlots: { customRender: "action" },
          },
        ];
      }
    },
    getDialogTitle() {
      var opt = "";
      var obj = "";
      if (this.form.id) {
        opt = "编辑";
      } else {
        opt = "新增";
      }
      if (this.currentTabKey == "income") {
        obj = "收入";
      } else {
        obj = "支出";
      }
      return opt + obj;
    },
  },
  mounted() {
    this.initailize();
  },
};
</script>

<style scoped>
</style>