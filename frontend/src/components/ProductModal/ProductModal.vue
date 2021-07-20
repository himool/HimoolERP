<template>
  <div>
    <a-modal v-model="visible" title="选择商品" :footer="null" :maskClosable="false" @cancel="$emit('cancel', false)">
      <div>
        <a-input-search v-model="searchText" placeholder="输入查询..." @search="search" />
      </div>
      <div style="margin-top: 12px;">
        <a-table :columns="goodsColumns" :data-source="items" :loading="loading" size="small" :pagination="false">
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

    <!-- <a-modal v-model="productModalVisible" :maskClosable="false" okText="确定" cancelText="取消"
      :title="selectedGoods.id ? `${selectedGoods.name} - ${selectedGoods.code}` : ''" @ok="confirm">
      <a-table :columns="productColumns" :data-source="selectedGoods.products" size="small" :pagination="false">
        <div slot="spec1" slot-scope="value, item">{{item.spec1_name}}</div>
        <div slot="spec2" slot-scope="value, item">{{item.spec2_name}}</div>
        <div slot="quantity" slot-scope="value, item">
          <a-input-number v-model="item.quantity" />
        </div>
      </a-table>
    </a-modal> -->
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
        goodsColumns: [
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
        // productColumns: [
        //   {
        //     title: '规格A',
        //     dataIndex: 'spec1',
        //     key: 'spec1',
        //     scopedSlots: { customRender: 'spec1' },
        //   },
        //   {
        //     title: '规格B',
        //     dataIndex: 'spec2',
        //     key: 'spec2',
        //     scopedSlots: { customRender: 'spec2' },
        //   },
        //   {
        //     title: '数量',
        //     dataIndex: 'quantity',
        //     key: 'quantity',
        //     scopedSlots: { customRender: 'quantity' },
        //   },
        // ],
        loading: false,
        items: [],
        // productModalVisible: false,
        selectedGoods: {},
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
        console.log(item);
        // this.selectedGoods = { ...item };
        // this.productModalVisible = true;
      },
      confirm() {
        // this.productModalVisible = false;
        // this.$emit('confirm', { ...this.selectedGoods });
        // this.$emit('cancel', false);
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      cancel() {
        this.$emit('cancel', false);
        this.items = [];
        this.searchText = '';
        this.currentPage = 1;
      }
    },
  }
</script>