<template>
  <div>
    <a-card title="供应商">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="名称" allowClear @pressEnter="handleSearch" />
        </a-col>
         <a-col :span="24" :md="16" :xl="18" style=" margin-bottom: 12px;display:flex; justify-content:space-between;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
           <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增供应商
        </a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
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
            <a-form-model-item prop="name" label="供应商名称">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="number" label="供应商编号">
              <a-input v-model="form.number" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="contacts" label="联系人">
              <a-input v-model="form.contacts" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="phone" label="电话">
              <a-input v-model="form.phone" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="email" label="邮箱">
              <a-input v-model="form.email" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="address" label="地址">
              <a-input v-model="form.address" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="bank_account" label="银行账户">
              <a-input v-model="form.bank_account" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="bank_name" label="开户行">
              <a-input v-model="form.bank_name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="status" label="状态">
              <a-select v-model="form.status">
                <a-select-option :value="true">启用</a-select-option>
                <a-select-option :value="false">停用</a-select-option>
              </a-select>
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="order" label="排序">
              <a-input-number v-model="form.order" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="remark" label="备注">
              <a-input v-model="form.remark" />
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
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
          },
          {
            title: '编号',
            dataIndex: 'number',
            key: 'number',
            sorter: true,
          },
          {
            title: '联系人',
            dataIndex: 'contacts',
            key: 'contacts',
          },
          {
            title: '电话',
            dataIndex: 'phone',
            key: 'phone',
          },
          {
            title: '邮箱',
            dataIndex: 'email',
            key: 'email',
          },
          {
            title: '地址',
            dataIndex: 'address',
            key: 'address',
          },
          {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            scopedSlots: { customRender: 'status' },
          },
          {
            title: '排序',
            dataIndex: 'order',
            key: 'order',
            sorter: true,
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
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
          this.items = resp.data.result;
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
        
      },
      resetForm() {
        this.form = {
          name: '', manager: '', phone: '', bank_account: '', bank_name: '', email: '',
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