<template>
  <div>
    <div style="margin-top: 8px;">
      <a-card title="商品信息">
        <div slot="extra" style="margin: -6px 0;">
          <a-button type="primary" @click="resetForm(); goodsVisible = true;">
            <a-icon type="plus" />新增商品
          </a-button>
        </div>

        <a-row gutter="16">
          <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
            <a-input v-model="searchForm.search" placeholder="名称, 货号" allowClear @pressEnter="handleSearch" />
          </a-col>
          <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
            <a-select v-model="searchForm.category" placeholder="商品分类" style="width: 100%;" allowClear
              @change="handleSearch">
              <a-select-option v-for="item of categoryItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
            <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
          </a-col>
        </a-row>

        <a-table :columns="columns" :data-source="goodsItems" size="small" :loading="loading" :pagination="false"
          @change="handleTableChange">
          <div slot="status" slot-scope="value, item">{{item.status ? '启用' : '停用'}}</div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button size="small" @click="$router.push({path: '/inventory', query: {search: item.code}})">
                <a-icon type="appstore" />库存
              </a-button>
              <a-button size="small" @click="$router.push({path: '/flow', query: {search: item.code}})">
                <a-icon type="profile" />流水
              </a-button>
              <a-button size="small" @click="goodsForm = {...item}; goodsVisible = true;">
                <a-icon type="edit" />编辑
              </a-button>
              <a-popconfirm :title="`删除商品: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
                <a-button type="danger" size="small">
                  <a-icon type="delete" />删除
                </a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
        <div style="text-align: center; margin-top: 24px;">
          <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
            @change="list" />
        </div>
      </a-card>
    </div>

    <goods-modal v-model="goodsVisible" :form="goodsForm" :categoryItems="categoryItems" @create="create"
      @update="update" @cancel="goodsVisible = false" />
  </div>
</template>

<script>
  import { goodsList, goodsDestroy, categoryList } from '@/api/goods'
  import NP from 'number-precision'

  export default {
    name: 'Goods',
    components: {
      GoodsModal: () => import('@/components/GoodsModal/GoodsModal'),
    },
    data() {
      return {
        NP,
        searchForm: { page: 1 },
        goodsForm: {},
        goodsItems: [],
        categoryItems: [],
        loading: false,
        goodsVisible: false,

        setGoodsItem: {},

        totalRows: 0,
        perPage: 20,
        columns: [
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
            sorter: true,
          },
          {
            title: '品牌',
            dataIndex: 'brand',
            key: 'brand',
          },
          {
            title: '分类',
            dataIndex: 'category_name',
            key: 'category_name',
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
            title: '采购价',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            sorter: true,
          },
          {
            title: '零售价',
            dataIndex: 'retail_price',
            key: 'retail_price',
            sorter: true,
          },
          {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            scopedSlots: { customRender: 'status' },
          },
          {
            title: '排序',
            dataIndex: 'order',
            key: 'order',
            sorter: true,
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '296px',
          },
        ],
      };
    },
    methods: {
      initalize() {
        this.resetForm();
        this.list();

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
        goodsList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.goodsItems = resp.data.results;
          })
          .catch(err => {

            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      create(goodsItem, isKeepAdd) {
        this.goodsItems.push(goodsItem);
        if (isKeepAdd) {
          this.resetForm();
        } else {
          this.goodsVisible = false;
        }
      },
      update(goodsItem) {
        this.goodsItems.splice(this.goodsItems.findIndex(item => item.id === goodsItem.id), 1, goodsItem);
        this.goodsVisible = false;
      },
      destroy(goodsItem) {
        let form = { ...goodsItem };
        goodsDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.goodsItems.splice(this.goodsItems.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {

            this.$message.error(err.response.data.message);
          });
      },
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      resetForm() {
        this.goodsForm = {
          name: '',
          code: '',
          purchase_price: 0,
          suggested_retail_price: 0,
          retail_price: 0,
          order: 100,
          status: true,
          inventory_warning_lower_limit: 0,
          inventory_warning_upper_limit: 5000,
          brand: '',
          category: null,
          specification: '',
          unit: '',
          inventory: {},
          initial_quantity: 0,
        };
      },
      handleSearch() {
        this.list();
      },
      handleTableChange(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initalize();
    },
  }
</script>