<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :xl="16">
        <a-card title="客户">
          <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="tableLoading">
            <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
            <div slot="action" slot-scope="value, item">
              <a-button-group>
                <a-tooltip>
                  <div slot="title">查看购买记录</div>
                  <a-button size="small" @click="$router.push({path: '/sales_record', query: {search: item.phone}})">
                    <a-icon type="unordered-list" />
                  </a-button>
                </a-tooltip>

                <a-popconfirm title="删除客户" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
                  <a-button type="danger" size="small">
                    <a-icon type="delete" />
                  </a-button>
                </a-popconfirm>
              </a-button-group>
            </div>
          </a-table>

          <div style="text-align: center; margin-top: 24px;">
            <a-pagination :value="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
              @change="changePage" />
          </div>
        </a-card>
      </a-col>
      <a-col :span="24" :xl="8">
        <a-card title="添加客户">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
            <a-form-model-item prop="phone" label="手机号">
              <a-input size="large" v-model="form.phone" />
            </a-form-model-item>
            <a-form-model-item prop="contacts" label="联系人">
              <a-input size="large" v-model="form.contacts" />
            </a-form-model-item>
            <a-form-model-item prop="name" label="名称">
              <a-input size="large" v-model="form.name" />
            </a-form-model-item>
            <a-form-model-item prop="mailbox" label="邮箱">
              <a-input size="large" v-model="form.mailbox" />
            </a-form-model-item>
            <a-form-model-item prop="address" label="地址">
              <a-input size="large" v-model="form.address" />
            </a-form-model-item>
          </a-form-model>
          <div style="text-align: center;">
            <a-button type="primary" :loading="buttonLoading" style="width: 96px;"
              @click="create">添加客户
            </a-button>
          </div>
        </a-card>

        <a-card title="查找客户" style="margin-top: 12px;">
          <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
            <a-form-model-item label="名称/手机号">
              <a-input size="large" v-model="searchText" allowClear />
            </a-form-model-item>
          </a-form-model>
          <div style="text-align: center;">
            <a-button type="primary" :loading="tableLoading" style="width: 96px;"
              @click="search">查询
            </a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { clientList, clientCreate, clientDestroy } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'Client',
    data() {
      return {
        moment,
        form: {},
        searchText: '',
        columns: [
          {
            title: '手机号',
            dataIndex: 'phone',
            key: 'phone',
          },
          {
            title: '联系人',
            dataIndex: 'contacts',
            key: 'contacts',
          },
          {
            title: '客户名称',
            dataIndex: 'name',
            key: 'name',
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
            title: '创建时间',
            dataIndex: 'create_date',
            key: 'create_date',
            scopedSlots: { customRender: 'create_date' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '100px',
          },
        ],
        items: [],
        tableLoading: false,
        buttonLoading: false,
        totalRows: 0,
        perPage: 10,
        currentPage: 1,
        rules: {
          phone: [
            { required: true, message: '请输入手机号', trigger: 'change' },
            { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      initailize() {
        this.resetForm();
        this.tableLoading = true;
        clientList({ search: this.searchText, page: this.currentPage })
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.tableLoading = false;
          });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.buttonLoading = true;
            clientCreate(this.form)
              .then(resp => {
                this.$message.success('新增成功');
                this.items.push(resp.data);
                this.resetForm();
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.buttonLoading = false;
              });
          }
        });
      },
      destroy(item) {
        let form = { ...item };
        clientDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
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
        this.form = { name: '', phone: '', address: '', mailbox: '', contacts: '' };
      },
    },
    mounted() {
      this.initailize();
    },
  }
</script>

<style scoped>
</style>