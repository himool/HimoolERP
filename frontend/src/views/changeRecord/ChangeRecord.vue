<template>
  <div>
    <a-card>
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading">
        <div slot="create_datetime" slot-scope="value">{{moment(value).format('YYYY-MM-DD HH:mm:ss')}}</div>
        <div slot="before_change" slot-scope="value">{{NP.round(value, 2)}}</div>
        <div slot="after_change" slot-scope="value">{{NP.round(value, 2)}}</div>
        <div slot="relation_order" slot-scope="value">
          <a-button v-if="value" type="link" @click="openInvoice(value)">查看</a-button>
        </div>
      </a-table>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { changeRecordList } from '@/api/purchase'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'ChangeRecord',
    data() {
      return {
        NP,
        moment,
        items: [],
        columns: [
          {
            title: '时间',
            dataIndex: 'create_datetime',
            key: 'create_datetime',
            scopedSlots: { customRender: 'create_datetime' },
          },
          {
            title: '编号',
            dataIndex: 'goods_code',
            key: 'goods_code',
          },
          {
            title: '名称',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '规格',
            dataIndex: 'spec',
            key: 'spec',
          },
          {
            title: '单位',
            dataIndex: 'goods_unit',
            key: 'goods_unit',
          },
          {
            title: '修改方式',
            dataIndex: 'change_method',
            key: 'change_method',
          },
          {
            title: '修改前',
            dataIndex: 'before_change',
            key: 'before_change',
            scopedSlots: { customRender: 'before_change' },
          },
          {
            title: '修改后',
            dataIndex: 'after_change',
            key: 'after_change',
            scopedSlots: { customRender: 'after_change' },
          },
          {
            title: '操作人',
            dataIndex: 'operator',
            key: 'operator',
          },
          {
            title: '关联采购单',
            dataIndex: 'relation_order',
            key: 'relation_order',
            scopedSlots: { customRender: 'relation_order' },
          },
        ],
        totalRows: 0,
        perPage: 20,
        currentPage: 1,
        loading: false,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        changeRecordList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
        
          .finally(() => {
            this.loading = false;
          });
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      openInvoice(id) {
        window.open(`/invoice/purchase?id=${id}`);
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>