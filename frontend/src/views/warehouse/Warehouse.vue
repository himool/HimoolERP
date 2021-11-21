<template>
  <div>
    <a-card title="仓库">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style=" margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="名称" allowClear @pressEnter="handleSearch" />
        </a-col>
          <a-col :span="24" :md="16" :xl="18" style=" margin-bottom: 12px;display:flex; justify-content:space-between;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
           <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增仓库
        </a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        @change="handleTableChange">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
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
        <a-form-model-item prop="name" label="仓库名称">
          <a-input v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="number" label="仓库编号">
          <a-input v-model="form.number" />
        </a-form-model-item>
        <a-form-model-item prop="manager" label="管理人">
          <!-- <a-select v-model="form.manager" :allowClear="true">
            <a-select-option v-for="item in userItems" :key="item.id" :value="item.id">{{item.username}}
            </a-select-option>
          </a-select> -->
          <UserSelected v-model="form.manager" @change="(value)=>{
            $set(form,'manager',value);
            }"
            @detailInfo="(value)=>{
              $set(form,'phone',value.phone);
            }"
            ></UserSelected>
        </a-form-model-item>
        <a-form-model-item prop="phone" label="座机">
          <a-input v-model="form.phone" />
        </a-form-model-item>
        <a-form-model-item prop="address" label="地址">
          <a-input v-model="form.address" />
        </a-form-model-item>
        <a-form-model-item prop="status" label="状态">
          <a-select v-model="form.status">
            <a-select-option :value="true">启用</a-select-option>
            <a-select-option :value="false">停用</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="order" label="排序">
          <a-input v-model="form.order" />
        </a-form-model-item>
        <a-form-model-item prop="remark" label="备注">
          <a-input v-model="form.remark" />
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
    components: {
       UserSelected: () => import("@/components/Fields/UserSelected"),
    },
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
            title: '管理人',
            dataIndex: 'manager_name',
            key: 'manager_name',
          },
          {
            title: '手机号',
            dataIndex: 'phone',
            key: 'phone',
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
        userItems: [],
        form: { name: '', type: '', manager: '', address: '', status: true, order: 100, remark: '' },
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
        this.list();
        userList()
          .then(resp => {
            this.userItems = resp.data;
          })
       
      },
      list() {
        this.loading = true;
        warehouseList(this.searchForm).then(resp => {
          this.items = resp.data;
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