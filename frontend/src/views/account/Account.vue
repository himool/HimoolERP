<template>
  <div>
    <a-card>
      <div slot="title">
        <span>结算账户</span>
        <span style="margin-left: 36px; margin-right: 4px;">统计时间:</span>
        <a-date-picker v-model="statisticalForm.start_date" :showToday="false" :allowClear="false"
          @change="statisticalAccount" :disabled="statisticalLoading" />
        <span style="margin: 0 4px;">至</span>
        <a-date-picker v-model="statisticalForm.end_date" :showToday="false" :allowClear="false"
          @change="statisticalAccount" :disabled="statisticalLoading" />
        <span style="margin-left: 24px;">收入:</span>
        <a-spin v-if="statisticalLoading" size="small" style="margin-left: 8px;" />
        <span v-else style="margin-left: 8px;">{{revenue}}</span>
        <span style="margin-left: 24px;">支出:</span>
        <a-spin v-if="statisticalLoading" size="small" style="margin-left: 8px;" />
        <span v-else style="margin-left: 8px;">{{expenditure}}</span>

      </div>
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        :row-selection="rowSelection">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="warehouse" slot-scope="value, item">{{item.warehouse_name ? item.warehouse_name : ''}}</div>
        <div slot="status" slot-scope="value, item">{{item.status ? '启用' : '停用'}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="form = {...item}; visible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-popconfirm :title="`删除结算账户: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>

        </div>
      </a-table>
      <div style="float: right; margin-top: 24px;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增结算账户</a-button>
      </div>
    </a-card>

    <a-modal v-model="visible" :title="form.id ? '编辑结算账户' : '新增结算账户'" :maskClosable="false"
      :okText="form.id ? '保存' : '新增'" cancelText="取消" @ok="form.id ? update() : create()"
      @cancel="$refs.form.clearValidate()">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="name" label="名称">
          <a-input size="large" v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="account" label="账号">
          <a-input size="large" v-model="form.account" />
        </a-form-model-item>
        <a-form-model-item prop="holder" label="开户人">
          <a-input size="large" v-model="form.holder" />
        </a-form-model-item>
        <a-form-model-item prop="warehouse" label="仓库">
          <a-select v-model="form.warehouse" size="large" allowClear>
            <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="type" label="类型">
          <a-select v-model="form.type" size="large">
            <a-select-option value="现金">现金</a-select-option>
            <a-select-option value="银行账户">银行账户</a-select-option>
            <a-select-option value="支付宝">支付宝</a-select-option>
            <a-select-option value="微信钱包">微信钱包</a-select-option>
            <a-select-option value="其他">其他</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="status" label="状态">
          <a-select v-model="form.status" size="large">
            <a-select-option :value="true">启用</a-select-option>
            <a-select-option :value="false">停用</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="order" label="排序">
          <a-input size="large" v-model="form.order" />
        </a-form-model-item>
        <a-form-model-item prop="remark" label="备注">
          <a-input size="large" v-model="form.remark" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { accountList, accountCreate, accountUpdate, accountDestroy, statisticalAccountList } from '@/api/account'
  import { warehouseList } from '@/api/warehouse'
  import moment from 'moment'

  export default {
    name: 'Account',
    data() {
      return {
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: '64px',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '账户名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '账号',
            dataIndex: 'account',
            key: 'account',
          },
          {
            title: '开户人',
            dataIndex: 'holder',
            key: 'holder',
          },
          {
            title: '账户类型',
            dataIndex: 'type',
            key: 'type',
          },
          {
            title: '所属仓库',
            dataIndex: 'warehouse',
            key: 'warehouse',
            scopedSlots: { customRender: 'warehouse' },
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
          },
          {
            title: '排序',
            dataIndex: 'order',
            key: 'order',
          },
          {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            scopedSlots: { customRender: 'status' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px',
          },
        ],
        items: [],
        warehouseItems: [],
        form: {},
        loading: false,
        visible: false,
        rules: {
          name: [{ required: true, message: '请输入名称', trigger: 'change' }],
          type: [{ required: true, message: '请选择类型', trigger: 'change' }],
        },
        rowSelection: {
          onChange: (selectedRowKeys, selectedRows) => {
            this.statisticalForm.accounts = selectedRows.map(item => item.id).join(',');
            this.statisticalAccount();
          },
        },

        statisticalLoading: false,
        statisticalForm: {
          accounts: '',
          start_date: moment().startOf('day'),
          end_date: moment().startOf('day'),
        },
        revenue: 0.0,
        expenditure: 0.0,
      }
    },
    methods: {
      initialize() {
        this.resetForm();
        this.statisticalAccount();
        this.loading = true;
        accountList()
          .then(resp => {
            this.items = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });

      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            accountCreate(this.form)
              .then(resp => {
                this.$message.success('新增成功');
                this.items.push(resp.data);
                this.visible = false;
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      update() {
        this.$refs.form.validate(valid => {
          if (valid) {
            accountUpdate(this.form)
              .then(resp => {
                this.$message.success('修改成功');
                this.items.splice(this.items.findIndex(item => item.id === resp.data.id), 1, resp.data);
                this.visible = false;
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      destroy(item) {
        let form = { ...item };
        accountDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      statisticalAccount() {
        if (this.statisticalForm.accounts.length === 0) {
          this.revenue = 0;
          this.expenditure = 0;
          return
        }

        let form = {...this.statisticalForm};
        form.start_date = form.start_date.format();
        form.end_date = form.end_date.format();
        this.statisticalLoading = true;

        statisticalAccountList(form)
          .then(resp => {
            this.revenue = resp.data.revenue;
            this.expenditure = resp.data.expenditure;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          }).finally(() => {
            this.statisticalLoading = false;
          });
      },
      resetForm() {
        this.form = { name: '', account: '', holder: '', status: true, order: 100, remark: '', warehouse: null, type: '现金' };
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>