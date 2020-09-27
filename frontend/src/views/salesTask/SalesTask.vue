<template>
  <div>
    <a-card>
      <div slot="title">
        <span>销售任务</span>
        <a-button type="primary" style="float: right;" @click="visible = true">
          <a-icon type="plus" />添加任务
        </a-button>
      </div>
      <div>
        <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
          :rowClassName="rowClassName">
          <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
          <div slot="status" slot-scope="value, item">{{rowStatus(item)}}</div>
          <div slot="complete_schedule" slot-scope="value, item">{{completeSchedule(item)}}</div>
          <div slot="start_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          <div slot="end_date" slot-scope="value">{{moment(value).subtract(1, 'days').format('YYYY-MM-DD')}}</div>
          <div slot="create_date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
        </a-table>
      </div>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>

    <add-task-modal v-model="visible" @create="create" />
  </div>
</template>

<script>
  import { salesTaskList } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesTask',
    components: {
      AddTaskModal: () => import('./AddTaskModal'),
    },
    data() {
      return {
        moment,
        totalRows: 0,
        perPage: 20,
        currentPage: 1,
        columns: [
          {
            title: '#',
            dataIndex: 'index',
            key: 'index',
            width: '64px',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            scopedSlots: { customRender: 'status' },
          },
          {
            title: '任务指派',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '任务商品',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '任务数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '完成数量',
            dataIndex: 'completed_quantity',
            key: 'completed_quantity',
          },
          {
            title: '完成进度',
            dataIndex: 'complete_schedule',
            key: 'complete_schedule',
            scopedSlots: { customRender: 'complete_schedule' },
          },
          {
            title: '起始日期',
            dataIndex: 'start_date',
            key: 'start_date',
            scopedSlots: { customRender: 'start_date' },
          },
          {
            title: '截至日期',
            dataIndex: 'end_date',
            key: 'end_date',
            scopedSlots: { customRender: 'end_date' },
          },
          {
            title: '创建日期',
            dataIndex: 'create_date',
            key: 'create_date',
            scopedSlots: { customRender: 'create_date' },
          },
        ],
        items: [],
        visible: false,
        loading: false,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        salesTaskList({ page: this.currentPage })
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      create(item) {
        this.items.splice(0, 0, item);
      },
      completeSchedule(item) {
        if (item.quantity == 0) {
          return '0 %'
        }

        return NP.times(NP.round(NP.divide(item.completed_quantity, item.quantity), 2), 100) + ' %'
      },
      rowClassName(item) {
        let today = moment()
        if (item.completed_quantity >= item.quantity) {  // 已完成
          return 'table-success'
        }

        if (today.isBefore(item.end_date)) {  // 进行中
          return 'table-warning'
        }

        if (!today.isBefore(item.end_date) && item.completed_quantity < item.quantity) {  // 已到期未完成
          return 'table-error'
        }
      },
      rowStatus(item) {
        let today = moment()
        if (item.completed_quantity >= item.quantity) {  // 已完成
          return '已完成'
        }

        if (today.isBefore(item.end_date)) {  // 进行中
          return '进行中'
        }

        if (!today.isBefore(item.end_date) && item.completed_quantity < item.quantity) {  // 已到期未完成
          return '未完成'
        }
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scope>
  .table-error {
    background: #fff1f0;
  }

  .table-warning {
    background: #fffbe6
  }

  .table-success {
    background: #f6ffed;
  }
</style>