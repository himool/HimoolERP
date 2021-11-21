<template>
  <div>
    <a-modal v-model="visible" title="选择客户" :footer="null" @cancel="cancel">
      <div>
        <a-input-search v-model="searchForm.search" placeholder="输入查询..." @search="searchData" />
      </div>
      <div style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :data-source="items" :loading="loading" :pagination="pagination">
          <div slot="action" slot-scope="value, item">
            <a-button size="small" @click="selectItem(item)">选择</a-button>
          </div>
        </a-table>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { clientList } from '@/api/sales'
  import { columns } from './columns';

  export default {
    props: ['visible'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        searchForm: { search: '', page: 1 },
        pagination: { current: 1, total: 0, pageSize: 16, showTotal: total => `共 ${total} 条` },
        loading: false,
        items: [],
        columns,
      };
    },
    methods: {
      initData() {
        this.list();
      },
      list() {
        this.loading = true;
        clientList(this.searchForm).then(resp => {
          this.pagination.total = resp.data.count;
          this.items = resp.data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      selectItem(item) {
        this.$emit('select', item);
        this.cancel();
      },
      searchData() {
        this.pagination.current = 1;
        this.searchForm.page = 1;
        this.list();
      },
      changeQuery(pagination, filters, sorter) {
        this.pagination = pagination;
        this.searchForm.page = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      cancel() {
        this.$emit('cancel', false);
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>