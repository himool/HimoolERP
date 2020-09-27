<template>
  <div>
    <a-modal v-model="visible" title="选择销售关联单" width="640px" :footer="null" :maskClosable="false" @cancel="cancel">
      <div>
        <a-input-search v-model="searchForm.search" placeholder="单号/公司/销售员" @search="search" />
      </div>
      <div style="margin-top: 12px;">
        <a-table :columns="columns" :data-source="items" :loading="loading" size="small" :pagination="false">
          <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          <div slot="action" slot-scope="value, item">
            <a-button size="small" @click="select(item)">选择</a-button>
          </div>
        </a-table>
      </div>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination :value="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { salesOrderList } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'RelationModal',
    props: ['visible'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        moment,
        perPage: 10,
        totalRows: 0,
        searchForm: { search: '', page: 1, is_done: true, is_return: false, page_size: 10 },
        items: [],
        loading: false,
        columns: [
          {
            title: '单号',
            dataIndex: 'id',
            key: 'id',
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '公司',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '销售员',
            dataIndex: 'seller',
            key: 'seller',
          },
          {
            title: '选择',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
      };
    },
    methods: {
      list() {
        this.loading = true;
        salesOrderList(this.searchForm)
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
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      select(item) {
        this.$emit('select', { ...item });
        this.cancel();
      },
      cancel() {
        this.$emit('cancel', false);
        this.items = [];
        this.searchForm.page = 1;
        this.searchForm.search = '';
      },
    },
    watch: {
      visible(value) {
        if (value) {
          this.list();
        }
      }
    },
  }
</script>