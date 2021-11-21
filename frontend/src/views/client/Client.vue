<template>
  <div>
    <a-card title="客户">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="手机号, 名称" allowClear @pressEnter="handleSearch" />
        </a-col>
        <a-col :span="24" :md="16" :xl="18" style=" margin-bottom: 12px;display:flex; justify-content:space-between;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
           <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增客户
        </a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="tableLoading"
        @change="handleTableChange">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="phone" slot-scope="value">
          <a-button type="link" @click="$router.push({path: '/sales_record', query: {search: value}})">
            {{value}}
          </a-button>
        </div>
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

      <div style="text-align: center; margin-top: 24px;">
        <a-pagination :value="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>

    <a-modal v-model="visible" :title="form.id ? '编辑客户' : '新增客户'" :maskClosable="false" :okText="form.id ? '保存' : '新增'"
      cancelText="取消" @ok="form.id ? update() : create()" @cancel="$refs.form.clearValidate()">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="name" label="客户名称">
          <a-input v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="number" label="客户编号">
          <a-input v-model="form.number" />
        </a-form-model-item>
          <a-form-model-item prop="level" label="等级">
          <a-select v-model="form.level">
            <a-select-option :value="0">1</a-select-option>
          <a-select-option :value="1">2</a-select-option>
          <a-select-option :value="2">3</a-select-option>
          <a-select-option :value="3">4</a-select-option>
          </a-select>
        </a-form-model-item>
       <a-form-model-item prop="category" label="客户分类">
         <ClientCategoriesSelect v-model="form.category"></ClientCategoriesSelect>
        </a-form-model-item>
        <a-form-model-item prop="contact" label="联系人">
          <a-input v-model="form.contact" />
        </a-form-model-item>
        <a-form-model-item prop="phone" label="手机号">
          <a-input v-model="form.phone" />
        </a-form-model-item>
        <a-form-model-item prop="email" label="邮箱">
          <a-input v-model="form.email" />
        </a-form-model-item>
        <a-form-model-item prop="address" label="地址">
          <a-input v-model="form.address" />
        </a-form-model-item>
        <a-form-model-item prop="is_active" label="激活状态">
             <a-switch checked-children="开" un-checked-children="关" 
             v-model="form.is_active" />
        </a-form-model-item>
        <a-form-model-item prop="order" label="排序">
          <a-input-number v-model="form.order" />
        </a-form-model-item>
        <a-form-model-item prop="remark" label="备注">
          <a-input v-model="form.remark" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { clientList, clientCreate, clientUpdate, clientDestroy } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'Client',
    data() {
      return {
        moment,
        form: {},
        searchForm: {},
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '客户名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
          },
          {
            title: '客户编号',
            dataIndex: 'number',
            key: 'number',
            sorter: true,
          },
          {
            title: '客户等级',
            dataIndex: 'level_display',
            key: 'level_display',
            sorter: true,
          },
          {
            title: '客户分类',
            dataIndex: 'category_name',
            key: 'category_name',
            sorter: true,
          },
          {
            title: '联系人',
            dataIndex: 'contacts',
            key: 'contacts',
          },
          {
            title: '手机号',
            dataIndex: 'phone',
            key: 'phone',
            scopedSlots: { customRender: 'phone' },
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
          },
        ],
        items: [],
        tableLoading: false,
        totalRows: 0,
        perPage: 16,
        currentPage: 1,
        rules: {
          name: [
            { required: true, message: '请输入名称', trigger: 'change' },
          ],
        },
        visible: false,
      };
    },
    components:{
      ClientCategoriesSelect: () => import("@/components/Fields/ClientCategoriesSelect"),
    },
    methods: {
      initailize() {
        this.resetForm();
        this.list();
      },
      list() {
        this.tableLoading = true;
        clientList(this.searchForm).then(resp => {
          this.totalRows = resp.data.count;
          this.items = resp.data.results;
        }).finally(() => {
          this.tableLoading = false;
        });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            clientCreate(this.form).then(resp => {
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
            clientUpdate(this.form)
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
        clientDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
            this.visible = false;
          })
         
      },
      search() {
        this.currentPage = 1;
        this.initailize();
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      resetForm() {
        this.form = {
          status: true, order: 100
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
      this.initailize();
    },
  }
</script>

<style scoped>
</style>