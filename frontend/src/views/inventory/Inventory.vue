<template>
  <div>
    <a-card>
      <div>
        <a-form-model :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }" layout="inline">
          <a-form-model-item>
            <a-popover title="列表设置" trigger="click">
              <template slot="content">
                <a-checkbox-group v-model="checkedColumns" @change="changeColumns">
                  <a-checkbox value="code">货号</a-checkbox>
                  <a-checkbox value="barnd">品牌</a-checkbox>
                  <a-checkbox value="category">分类</a-checkbox>
                  <a-checkbox value="purchase_price">采购价</a-checkbox>
                </a-checkbox-group>
              </template>
              <a-button>
                <a-icon type="setting" />
              </a-button>
            </a-popover>
          </a-form-model-item>
          <a-form-model-item class="form" label="仓库" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-select v-model="searchForm.warehouse" allowClear>
              <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item class="form" label="分类">
            <a-select v-model="searchForm.category" allowClear>
              <a-select-option v-for="item in categoryItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>

          <a-form-model-item class="form" label="搜索">
            <a-input v-model="searchForm.search" placeholder="名称/货号" allowClear />
          </a-form-model-item>
          <a-form-model-item class="form" label="排序">
            <a-select v-model="searchForm.ordering" allowClear>
              <a-select-option key="name" value="goods_name">按名称</a-select-option>
              <a-select-option key="brand" value="brand_name">按品牌</a-select-option>
              <a-select-option key="brand" value="quantity">按数量(从小到大)</a-select-option>
              <a-select-option key="brand" value="-quantity">按数量(从大到小)</a-select-option>
            </a-select>
          </a-form-model-item>

          <a-form-model-item class="form" label="数量">
            <a-input-number v-model="searchForm.min_quantity" step="100" style="width: 40%;" />
            <span style="margin: 0 5px;">至</span>
            <a-input-number v-model="searchForm.max_quantity" step="100" style="width: 40%;" />
          </a-form-model-item>

          <a-form-model-item prop="name" :wrapper-col="{ span: 24 }">
            <a-checkbox v-model="searchForm.is_filter_zero">过滤无库存</a-checkbox>
            <a-checkbox v-model="searchForm.is_filter_negative">过滤负库存</a-checkbox>
            <a-checkbox v-model="searchForm.is_show_warning">显示库存警告</a-checkbox>
          </a-form-model-item>

          <a-form-model-item>
            <a-button type="primary" @click="search">查询</a-button>
          </a-form-model-item>

          <a-form-model-item>
            <a-button @click="exportData">导出</a-button>
          </a-form-model-item>
          <a-form-model-item style="float: right; font-size: 15px;" :wrapper-col="{ span: 24 }">
            <span style="margin-right: 16px;">总价值: {{totalAmount ? NP.round(totalAmount, 2) : 0}}</span>
            <span>总数量: {{totalQuantity ? totalQuantity : 0}}</span>
          </a-form-model-item>

        </a-form-model>
      </div>

      <div style="margin-top: 8px;">
        <a-table :columns="columns" :data-source="items" :loading="loading" :pagination="false">
          <div slot="code" slot-scope="value, item">{{ item.goods.code }}</div>
          <div slot="name" slot-scope="value, item">{{ item.goods.name }}</div>
          <div slot="brand" slot-scope="value, item">{{ item.goods.brand }}</div>
          <div slot="specification" slot-scope="value, item">{{ item.goods.specification }}</div>
          <div slot="unit" slot-scope="value, item">{{ item.goods.unit }}</div>
          <div slot="category_name" slot-scope="value, item">{{ item.goods.category_name }}</div>

          <div slot="purchase_price_title">采购价
            <a-icon :type="isShowPurchasePrice ? 'eye-invisible' : 'eye'" style="margin: 4px; cursor: pointer;"
              @click="isShowPurchasePrice = !isShowPurchasePrice" />
          </div>
          <div slot="purchase_price" slot-scope="value, item">
            {{ isShowPurchasePrice ? NP.round(item.goods.purchase_price, 2) : '*****' }}
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
  import { warehouseList, inventoryList, exportInventory } from '@/api/warehouse'
  import { categoryList } from '@/api/goods'
  import NP from 'number-precision'

  export default {
    name: 'Inventory',
    data() {
      return {
        NP,
        searchForm: {
          search: '',
          ordering: '',
          warehouse: null,
          category: null,
          min_quantity: '',
          max_quantity: '',
          is_filter_zero: false,
          is_filter_negative: false,
          is_show_warning: false,
          page: 1,
        },
        warehouseItems: [],
        categoryItems: [],
        items: [],
        columnsTemplate: [
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
            scopedSlots: { customRender: 'code' },
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
            scopedSlots: { customRender: 'name' },
          },
          {
            title: '品牌',
            dataIndex: 'brand',
            key: 'brand',
            scopedSlots: { customRender: 'brand' },
          },
          {
            title: '规格型号',
            dataIndex: 'specification',
            key: 'specification',
            scopedSlots: { customRender: 'specification' },
          },
          {
            title: '单位',
            dataIndex: 'unit',
            key: 'unit',
            scopedSlots: { customRender: 'unit' },
          },
          {
            title: '分类',
            dataIndex: 'category_name',
            key: 'category_name',
            scopedSlots: { customRender: 'category_name' },
          },
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            slots: { title: 'purchase_price_title' },
            scopedSlots: { customRender: 'purchase_price' },
          },
        ],
        columns: [],
        checkedColumns: ['code', 'barnd', 'category', 'purchase_price'],
        loading: false,
        noMoreData: false,
        totalAmount: 0,
        totalQuantity: 0,
        isShowPurchasePrice: true,
        perPage: 15,
      };
    },
    methods: {
      initialize() {
        this.list();
        this.changeColumns();

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
        inventoryList(this.searchForm)
          .then(resp => {
            if (this.searchForm.page === 1) {
              this.items = resp.data.results;
            } else {
              this.items.push(...resp.data.results);
            }
            this.totalAmount = resp.data.total_amount;
            this.totalQuantity = resp.data.total_quantity;
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
      changeColumns() {
        let columns = ['code', 'barnd', 'category', 'purchase_price'].filter(value => this.checkedColumns.indexOf(value) === -1);
        this.columns = this.columnsTemplate.filter(item => columns.indexOf(item.key) === -1);
      },
      exportData() {
        exportInventory(this.searchForm)
          .then(resp => {
            this.convertRes2Blob(resp);
          })
          .catch((err) => {
            
                this.$message.error(err.response.data.message);
          });
      },
      convertRes2Blob(response) {
        const filename = response.headers['content-disposition'].match(/filename=(.*)/)[1];
        const blob = new Blob([response.data], { type: 'application/octet-stream' });

        if (typeof window.navigator.msSaveBlob !== 'undefined') {
          window.navigator.msSaveBlob(blob, decodeURI(filename));
        } else {
          const blobURL = window.URL.createObjectURL(blob);
          const tempLink = document.createElement('a');
          tempLink.style.display = 'none';
          tempLink.href = blobURL;
          tempLink.setAttribute('download', decodeURI(filename));

          if (typeof tempLink.download === 'undefined') {
            tempLink.setAttribute('target', '_blank');
          }

          document.body.appendChild(tempLink);
          tempLink.click();
          document.body.removeChild(tempLink);
          window.URL.revokeObjectURL(blobURL);
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