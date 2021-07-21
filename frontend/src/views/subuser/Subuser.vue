<template>
  <div>
    <a-card>
      <div slot="title">子账号
        <a-button type="primary" @click="createVisible = true" style="float: right;">创建子账号</a-button>
      </div>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
        <div slot="username" slot-scope="value">
          <a-button type="link" @click="$router.push({path: '/sales_record', query: {search: value}})">{{value}}</a-button>
        </div>

        <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        <div slot="roles" slot-scope="value, item">{{item.role_names.join(', ')}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="selectedItem = item; updateVisible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-button size="small" @click="selectedItem = item; resetVisible = true;">
              <a-icon type="reload" />重置密码
            </a-button>
            <a-popconfirm :title="`删除账号: ${item.username}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </a-table>
    </a-card>

    <create-modal v-model="createVisible" :roleItems="roleItems" @create="create" />
    <update-modal v-model="updateVisible" :roleItems="roleItems" :form="selectedItem" @update="update" />
    <reset-modal v-model="resetVisible" :form="selectedItem" />

  </div>
</template>

<script>
  import { roleList, subuserList, subuserDestroy } from '@/api/account'
  import moment from 'moment'

  export default {
    name: 'Subuser',
    components: {
      CreateModal: () => import('./CreateModal.vue'),
      UpdateModal: () => import('./UpdateModal.vue'),
      ResetModal: () => import('./ResetModal.vue'),
    },
    data() {
      return {
        moment,
        columns: [
          {
            title: '用户名',
            dataIndex: 'username',
            key: 'username',
            scopedSlots: { customRender: 'username' },
          },
          {
            title: '创建时间',
            dataIndex: 'create_date',
            key: 'create_date',
            scopedSlots: { customRender: 'create_date' },
          },
          {
            title: '手机号',
            dataIndex: 'phone',
            key: 'phone',
          },
          {
            title: '角色',
            dataIndex: 'roles',
            key: 'roles',
            scopedSlots: { customRender: 'roles' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '256px',
          },
        ],
        items: [],
        loading: false,
        roleItems: [],

        createVisible: false,
        updateVisible: false,
        resetVisible: false,

        selectedItem: {},
      };
    },
    methods: {
      initailize() {
        this.loading = true;
        subuserList()
          .then(resp => {
            this.items = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });

        roleList()
          .then(resp => {
            this.roleItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      create(subuser) {
        this.items.push(subuser);
      },
      update(subuser) {
        this.items.splice(this.items.findIndex(item => item.id === this.selectedItem.id), 1, subuser);
      },
      destroy(item) {
        let form = { ...item };
        subuserDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
    },
    mounted() {
      this.initailize();
    },
  }
</script>