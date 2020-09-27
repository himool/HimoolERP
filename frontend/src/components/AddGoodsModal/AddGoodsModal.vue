<template>
  <div>
    <a-modal v-model="visible" title="选择商品" :footer="null" :maskClosable="false" @cancel="cancel">
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

    <a-modal v-model="formModalVisible" :maskClosable="false" okText="确定" cancelText="取消"
      :title="selectedGoods.id ? `${selectedGoods.name} - ${selectedGoods.code}` : ''" @ok="confirm">
      <div style="text-align: center;">
        <span style="margin-right: 4px;">数量:</span>
        <a-input-number v-model="selectedGoods.quantity" :min="0" style="width: 40%;" />
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { goodsList } from '@/api/goods'

  export default {
    name: 'AddGoodsModal',
    props: ['visible'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        searchText: '',
        currentPage: 1,
        totalRows: 0,
        perPage: 10,
        columns: [
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '选择',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        loading: false,
        items: [],
        form: { quantity: 1 },

        selectedGoods: { quantity: 1 },
        formModalVisible: false,
      };
    },
    methods: {
      list() {
        this.loading = true;
        goodsList({ search: this.searchText, page: this.currentPage, page_size: this.perPage })
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
        item.quantity = 1;
        this.selectedGoods = { ...item };
        this.formModalVisible = true;
      },
      confirm() {
        if (this.selectedGoods.quantity <= 0) {
          this.$message.error('商品数量不能小于等于0');
          return
        }
        this.$emit('confirm', { ...this.selectedGoods });
        this.cancel();
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      cancel() {
        this.formModalVisible = false;
        this.$emit('cancel', false);
        this.items = [];
        this.searchText = '';
        this.currentPage = 1;
      }
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