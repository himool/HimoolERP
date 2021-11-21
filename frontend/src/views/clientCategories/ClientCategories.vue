<template>
  <div>
    <a-card title="客户类型">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="手机号, 名称" allowClear @pressEnter="handleSearch" />
        </a-col>
        <a-col :span="24" :md="16" :xl="18" style=" margin-bottom: 12px;display:flex; justify-content:space-between;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
           <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增客户类型
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
        <a-form-model-item prop="name" label="名称">
          <a-input v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="remark" label="备注">
          <a-input v-model="form.remark" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { clientCategoriesList, clientCategoriesCreate, clientCategoriesUpdate, clientCategoriesDestroy } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'ClientCategories',
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
    methods: {
      initailize() {
        this.resetForm();
        this.list();
      },
      list() {
        this.tableLoading = true;
        clientCategoriesList(this.searchForm).then(resp => {
          this.totalRows = resp.data.count;
          this.items = resp.data.results;
        }).finally(() => {
          this.tableLoading = false;
        });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            clientCategoriesCreate(this.form).then(resp => {
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
            clientCategoriesUpdate(this.form)
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
        clientCategoriesDestroy(form)
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