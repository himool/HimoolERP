<template>
  <div>
    <a-card title="仓库">
      <div slot="extra" style="margin: -6px 0;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增仓库
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

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        @change="handleTableChange">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="update_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="status" slot-scope="value, item">{{item.status ? '启用' : '停用'}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="form = {...item}; visible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-popconfirm :title="`删除仓库: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </a-table>
    </a-card>

    <a-modal v-model="visible" :title="form.id ? '编辑仓库' : '新增仓库'" :maskClosable="false" :okText="form.id ? '保存' : '新增'"
      cancelText="取消" @ok="form.id ? update() : create()" @cancel="$refs.form.clearValidate()">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="name" label="名称">
          <a-input size="large" v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="manager" label="管理人">
          <a-select v-model="form.manager" size="large" :allowClear="true">
            <a-select-option v-for="item in userItems" :key="item.id" :value="item.id">{{item.username}}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="address" label="地址">
          <a-input size="large" v-model="form.address" />
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
  import { warehouseList, warehouseCreate, warehouseUpdate, warehouseDestroy } from '@/api/warehouse'
  import { userList } from '@/api/account'
  import moment from 'moment'

  export default {
    name: 'Warehouse',
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
            title: '地址',
            dataIndex: 'address',
            key: 'address',
          },
          {
            title: '商品总数',
            dataIndex: 'goods_total',
            key: 'goods_total',
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true,
          },
          {
            title: '创建时间',
            dataIndex: 'create_date',
            key: 'create_date',
            sorter: true,
            scopedSlots: { customRender: 'create_date' },
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
        userItems: [],
        form: { name: '', type: '', manager: '', address: '', status: true, order: 100, remark: '' },
        loading: false,
        visible: false,
        rules: {
          name: [{ required: true, message: '请输入名称', trigger: 'change' }],
          type: [{ required: true, message: '请选择类型', trigger: 'change' }],
        },
        searchForm: {},
      };
    },
    methods: {
      initialize() {
        this.list();
        userList()
          .then(resp => {
            this.userItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
      },
      list() {
        this.loading = true;
        warehouseList(this.searchForm).then(resp => {
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
            warehouseCreate(this.form)
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
            warehouseUpdate(this.form)
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
        warehouseDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {

            this.$message.error(err.response.data.message);
          });
      },
      resetForm() {
        this.form = { name: '', type: '', manager: '', address: '', status: true, order: 100, remark: '' };
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