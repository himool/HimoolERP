<template>
  <div>
    <a-modal v-model="visible" title="选择客户" :footer="null" :maskClosable="false" @cancel="$emit('cancel', false)">
      <div>
        <a-input-search v-model="searchText" placeholder="输入查询..." @search="search" />
      </div>
      <div style="margin-top: 12px;">
        <a-table :columns="columns" :data-source="items" :loading="loading" size="small" :pagination="false">
          <div slot="action" slot-scope="value, item">
            <a-button size="small" @click="select(item)">选择</a-button>
          </div>
        </a-table>
      </div>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { clientList } from '@/api/sales'

  export default {
    name: 'ClientModal',
    props: ['visible'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        searchText: '',
        currentPage: 1,
        totalRows: 0,
        perPage: 10,
        loading: false,
        items: [],
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
            title: '名称',
            dataIndex: 'name',
            key: 'name',
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
        clientList({ search: this.searchText, page: this.currentPage, page_size: this.perPage })
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
        this.currentPage = 1;
        this.list();
      },
      select(item) {
        this.$emit('confirm', { ...item });
        this.$emit('cancel', false);
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
    },
    watch: {
      visible(value) {
        if (value) {
          this.items = [];
          this.searchText = '';
          this.currentPage = 1;
          this.list();
        }
      }
    },
    mounted() {
      this.list();
    },
  }
</script>

<style scoped>
</style>