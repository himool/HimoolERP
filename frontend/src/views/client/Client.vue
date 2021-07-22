<template>
  <div>
    <a-card title="客户">
      <div slot="extra" style="margin: -6px 0;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增客户
        </a-button>
      </div>

      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="手机号, 名称" allowClear @pressEnter="handleSearch" />
        </a-col>
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="tableLoading"
        @change="handleTableChange">
        <div slot="phone" slot-scope="value">
          <a-button type="link" @click="$router.push({path: '/sales_record', query: {search: value}})">{{value}}
          </a-button>
        </div>

        <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
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
            title: '手机号',
            dataIndex: 'phone',
            key: 'phone',
            sorter: true,
            scopedSlots: { customRender: 'phone' },
          },
          {
            title: '联系人',
            dataIndex: 'contacts',
            key: 'contacts',
            sorter: true,
          },
          {
            title: '客户名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
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
            sorter: true,
            scopedSlots: { customRender: 'create_date' },
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
        perPage: 10,
        currentPage: 1,
        rules: {
          phone: [
            { required: true, message: '请输入手机号', trigger: 'change' },
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
        clientList(this.searchForm).then(resp => {
          this.totalRows = resp.data.count;
          this.items = resp.data.results;
          console.log(resp.data)
        }).catch(err => {
          this.$message.error(err.response.data.message);
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
            }).catch(err => {
              this.$message.error(err.response.data.message);
            });
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
              .catch(err => {
                this.$message.error(err.response.data.message);
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
            this.visible = false;
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