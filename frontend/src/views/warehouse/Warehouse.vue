<template>
  <div>
    <a-card title="公司">
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="update_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="status" slot-scope="value, item">{{item.status ? '启用' : '停用'}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="form = {...item}; visible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-popconfirm :title="`删除公司: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>

        </div>
      </a-table>
      <div style="float: right; margin-top: 24px;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增公司</a-button>
      </div>
    </a-card>

    <a-modal v-model="visible" :title="form.id ? '编辑公司' : '新增公司'" :maskClosable="false"
      :okText="form.id ? '保存' : '新增'" cancelText="取消" @ok="form.id ? update() : create()"
      @cancel="$refs.form.clearValidate()">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="name" label="名称">
          <a-input size="large" v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="type" label="类型">
          <a-select v-model="form.type" size="large">
            <a-select-option value="仓库">仓库</a-select-option>
            <a-select-option value="门店">门店</a-select-option>
            <a-select-option value="公司">公司</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="manager" label="管理人">
          <a-select v-model="form.manager" size="large" :allowClear="true">
            <a-select-option v-for="value in userItems" :key="value" :value="value">{{value}}
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
            title: '#',
            dataIndex: 'index',
            key: 'index',
            width: '64px',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '负责人',
            dataIndex: 'manager',
            key: 'manager',
          },
          {
            title: '类型',
            dataIndex: 'type',
            key: 'type',
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
      };
    },
    methods: {
      initialize() {
        this.loading = true;
        warehouseList()
          .then(resp => {
            this.items = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });

          userList()
          .then(resp => {
            this.userItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
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
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>