<template>
  <div>
    <a-card title="供应商">
      <div slot="extra" style="margin: -6px 0;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增供应商
        </a-button>
      </div>

      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="名称" allowClear @pressEnter="handleSearch" />
        </a-col>
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="update_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="status" slot-scope="value, item">{{item.status ? '启用' : '停用'}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="form = {...item}; visible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-popconfirm :title="`删除供应商: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </a-table>
    </a-card>

    <a-modal v-model="visible" :title="form.id ? '编辑供应商' : '新增供应商'" :maskClosable="false"
      :okText="form.id ? '保存' : '新增'" cancelText="取消" width="756px" @ok="form.id ? update() : create()"
      @cancel="$refs.form.clearValidate()">

      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4, md: 6 }"
        :wrapper-col="{ span: 20, md: 18 }">
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="name" label="名称">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="address" label="地址">
              <a-input v-model="form.address" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="manager" label="负责人">
              <a-input v-model="form.manager" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="url" label="网址">
              <a-input v-model="form.url" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="phone" label="电话">
              <a-input v-model="form.phone" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="mailbox" label="邮箱">
              <a-input v-model="form.mailbox" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="bank_account" label="银行账户">
              <a-input v-model="form.bank_account" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="status" label="状态">
              <a-select v-model="form.status" size="large">
                <a-select-option :value="true">启用</a-select-option>
                <a-select-option :value="false">停用</a-select-option>
              </a-select>
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="bank_name" label="开户行">
              <a-input v-model="form.bank_name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="order" label="排序">
              <a-input size="large" v-model="form.order" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="remark" label="备注">
              <a-input v-model="form.remark" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="default_discount" label="默认折扣">
              <a-input-number v-model="form.default_discount" :precision="0" :min="0" :max="100" :step="5"
                :formatter="value => `${value}%`" :parser="value => value.replace('%', '')" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { supplierList, supplierCreate, supplierUpdate, supplierDestroy } from '@/api/purchase'
  import moment from 'moment'

  export default {
    name: 'Supplier',
    data() {
      return {
        moment,
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: '64px',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
          },
          {
            title: '负责人',
            dataIndex: 'manager',
            key: 'manager',
          },
          {
            title: '电话',
            dataIndex: 'phone',
            key: 'phone',
          },
          {
            title: '邮箱',
            dataIndex: 'mailbox',
            key: 'mailbox',
          },
          {
            title: '地址',
            dataIndex: 'address',
            key: 'address',
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true,
          },
          {
            title: '更新时间',
            dataIndex: 'update_date',
            key: 'update_date',
            scopedSlots: { customRender: 'update_date' },
          },
          {
            title: '排序',
            dataIndex: 'order',
            key: 'order',
            sorter: true,
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
        form: {},
        loading: false,
        visible: false,
        rules: {
          name: [{ required: true, message: '请输入名称', trigger: 'change' }],
        },
        searchForm: {},
      };
    },
    methods: {
      initialize() {
        this.resetForm();
        this.list();
      },
      list() {
        this.loading = true;
        supplierList(this.searchForm).then(resp => {
          this.items = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        }).finally(() => {
          this.loading = false;
        });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            supplierCreate(this.form)
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
            supplierUpdate(this.form)
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
        supplierDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {

            this.$message.error(err.response.data.message);
          });
      },
      resetForm() {
        this.form = {
          name: '', manager: '', phone: '', bank_account: '', bank_name: '', mailbox: '',
          address: '', url: '', default_discount: 100, status: true, order: 100, remark: '',
        };
      },
      handleSearch() {
        this.list();
      },
      handleTableChange(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>