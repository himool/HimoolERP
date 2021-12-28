<template>
  <div>
    <a-card title="销售任务">
      <a-row gutter="16">
        <a-col :span="24" :md="6" :xl="4" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="名称, 备注" allowClear @search="search" />
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">新增任务</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{value ? '激活' : '冻结'}}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-popconfirm title="确定删除吗" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
    <form-modal v-model="visible" :form="targetItem" :warehouseItems="warehouseItems" :clientsItems="clientsItems" @create="create" @update="update" />

  </div>
</template>

<script>
  import { clientsOption, warehousesOption } from '@/api/option'
  import { saleTaskList, saleTaskDestroy } from '@/api/sale'

  export default {
    name: 'Warehouse',
    components: {
      FormModal: () => import('./FormModal.vue'),
    },
    data() {
      return {
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
          },
          {
            title: '任务商品',
            dataIndex: 'goods_name',
            sorter: true,
          },
          {
            title: '商品编号',
            dataIndex: 'goods_number'
          },
          {
            title: '仓库',
            dataIndex: 'warehouse_name'
          },
          {
            title: '销售员',
            dataIndex: 'salesperson_name'
          },
          {
            title: '任务总量',
            dataIndex: 'total_quantity'
          },
          {
            title: '开始时间',
            dataIndex: 'start_time'
          },
          {
            title: '结束',
            dataIndex: 'end_time'
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px'
          },
        ],
        searchForm: { search: '', page: 1 },
        pagination: { current: 1, total: 0, pageSize: 15 },
        loading: false,
        items: [],
        warehouseItems: [],
        clientsItems: [],
        visible: false,
        targetItem: {},
        form: {},
        importLoading: false,
      };
    },
    computed: {
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        saleTaskList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      create(item) {
        this.items.splice(0, 0, item);
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      openFormModal(item) {
        this.targetItem = { ...item };
        warehousesOption({ page_size: 999999, is_active: true }).then(data => {
          this.warehouseItems = data.results;
        });
        clientsOption({ page_size: 999999, is_active: true }).then(data => {
          this.clientsItems = data.results;
        });
        this.visible = true;
      },
      destroy(id) {
        saleTaskDestroy({ id }).then(() => {
          this.items.splice(this.items.findIndex(item => item.id == id), 1);
          this.$message.success('删除成功');
        });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>