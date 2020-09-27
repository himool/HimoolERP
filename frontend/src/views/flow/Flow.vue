<template>
  <div>
    <a-card>
      <div>
        <a-form-model :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }" layout="inline">
          <a-form-model-item class="form" label="公司">
            <a-select v-model="searchForm.warehouse" allowClear>
              <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item class="form" label="业务类型" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-select v-model="searchForm.type" allowClear>
              <a-select-option value="采购单">采购单</a-select-option>
              <a-select-option value="采购退货单">采购退货单</a-select-option>
              <a-select-option value="销售单">销售单</a-select-option>
              <a-select-option value="销售退货单">销售退货单</a-select-option>
              <a-select-option value="调拨单">调拨单</a-select-option>
              <a-select-option value="盘点单">盘点单</a-select-option>
              <a-select-option value="初始化库存">初始化库存</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item class="form" label="分类">
            <a-select v-model="searchForm.category" allowClear>
              <a-select-option v-for="item in categoryItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item class="form" label="商品/货号" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-input v-model="searchForm.search" allowClear />
          </a-form-model-item>
          <a-form-model-item>
            <a-button type="primary" @click="search">查询</a-button>
          </a-form-model-item>
        </a-form-model>
      </div>
      <div style="margin-top: 16px;">
        <a-table :columns="columns" :data-source="items" :loading="loading" :pagination="false">
          <div slot="create_datetime" slot-scope="value">{{moment(value).format('YYYY-MM-DD HH:mm')}}</div>
          <div slot="change_quantity" slot-scope="value">{{value > 0 ? `+${value}` : value}}</div>
          <div slot="relation_order" slot-scope="value, item">
            <a-button
              v-if="!item.is_undo && (item.requisition || item.counting_list || item.purchase_order || item.sales_order)"
              type="link" @click="openInvoice(item)">查看</a-button>
          </div>
        </a-table>
        <div style="margin-top: 16px; text-align: center;">
          <a-button :loading="loading" :disabled="noMoreData" type="dashed" @click="loadMore">
            {{noMoreData ?  '没有更多数据': '加载更多' }}</a-button>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { categoryList } from '@/api/goods'
  import { warehouseList, flowList } from '@/api/warehouse'
  import moment from 'moment'

  export default {
    name: 'Flow',
    data() {
      return {
        moment,
        searchForm: {
          search: '',
          warehouse: '',
          type: '',
          category: '',
          page: 1,
        },
        loading: false,
        noMoreData: false,
        columns: [
          {
            title: '时间',
            dataIndex: 'create_datetime',
            key: 'create_datetime',
            scopedSlots: { customRender: 'create_datetime' },
          },
          {
            title: '货号',
            dataIndex: 'goods_code',
            key: 'goods_code',
          },
          {
            title: '名称',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '规格型号',
            dataIndex: 'specification',
            key: 'specification',
          },
          {
            title: '单位',
            dataIndex: 'unit',
            key: 'unit',
          },
          {
            title: '公司',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '类别',
            dataIndex: 'type',
            key: 'type',
          },
          {
            title: '发生数量',
            dataIndex: 'change_quantity',
            key: 'change_quantity',
            scopedSlots: { customRender: 'change_quantity' },
          },
          {
            title: '剩余数量',
            dataIndex: 'remain_quantity',
            key: 'remain_quantity',
          },
          {
            title: '操作人',
            dataIndex: 'operator',
            key: 'operator',
          },
          {
            title: '关联单',
            dataIndex: 'relation_order',
            key: 'relation_order',
            scopedSlots: { customRender: 'relation_order' },
          },
        ],
        warehouseItems: [],
        categoryItems: [],
        items: [],
        perPage: 15,
      };
    },
    methods: {
      initialize() {
        if (this.$route.query.search) {
          this.searchForm.search = this.$route.query.search;
        }
        this.list();

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });

        categoryList()
          .then(resp => {
            this.categoryItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.loading = true;
        flowList(this.searchForm)
          .then(resp => {
            if (this.searchForm.page === 1) {
              this.items = resp.data.results;
            } else {
              this.items.push(...resp.data.results);
            }
            this.noMoreData = resp.data.results.length < this.perPage ? true : false;
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
      loadMore() {
        this.searchForm.page += 1;
        this.list();
      },
      openInvoice(item) {
        if (item.is_undo) {
          return
        }

        if (item.requisition) {
          window.open(`/invoice/requisition?id=${item.requisition}`);
        } else if (item.counting_list) {
          window.open(`/invoice/counting_list?id=${item.counting_list}`);
        } else if (item.purchase_order) {
          window.open(`/invoice/purchase?id=${item.purchase_order}`);
        } else if (item.sales_order) {
          window.open(`/invoice/sales?id=${item.sales_order}`);
        }
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
  .form {
    width: 220px;
  }
</style>