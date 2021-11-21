<template>
  <div>
    <a-row gutter="8">
      <a-col :span="8">
        <a-card>
          <a-row style="margin-bottom: 8px;">
            <a-col :span="24" style="margin-bottom: 8px;">
              <a-select v-model="searchForm.warehouse" placeholder="仓库" style="width: 100%;" allowClear
                @change="search">
                <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                </a-select-option>
              </a-select>
            </a-col>
            <a-col :span="24" style="margin-bottom: 8px;">
              <a-input-search v-model="searchForm.search" placeholder="单号" enter-button @search="search" />
            </a-col>
          </a-row>

          <a-table :columns="columns" :data-source="items" :loading="tableLoading" :pagination="false"
            :customRow="customRow" :rowClassName="rowClassName" size="small">
            <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          </a-table>
          <div style="text-align: center; margin-top: 16px;">
            <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
              @change="changePage" />
          </div>
        </a-card>
      </a-col>
      <a-col :span="16">
        <a-card :title="form.id ? `盘点单 - ${form.id}` : '盘点单'">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-row gutter="8">
              <a-col :span="12" :xl="6">
                <a-form-model-item prop="warehouse" label="仓库">
                  <a-select v-model="form.warehouse" :disabled="form.id">
                    <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :span="12" :xl="12">
                <a-form-model-item prop="remark" label="备注" :label-col="{ span: 8, xl: 3 }"
                  :wrapper-col="{ span: 16, xl: 21 }">
                  <a-input v-model="form.remark" allowClear :disabled="form.id" />
                </a-form-model-item>
              </a-col>
              <a-col :span="12" :xl="6">
                <a-form-model-item style="text-align: right;">
                  <a-button type="primary" :disabled="form.id" @click="addGoodsModalVisible = true">
                    <a-icon type="plus" />添加商品</a-button>
                </a-form-model-item>
              </a-col>
            </a-row>
          </a-form-model>
          <a-table :columns="goodsColumns" :data-source="dataSource" :pagination="false" size="small">
            <div slot="index" slot-scope="value, item, index">{{item.id ? index + 1 : ''}}</div>
            <div slot="before_counting" slot-scope="value,">{{form.id ? value : '-'}}</div>
            <div slot="profit_quantity" slot-scope="value, item">
              {{form.id ? item.id ? NP.minus(item.quantity, item.before_counting): value : '-'}}
            </div>
            <div slot="profit_amount" slot-scope="value, item">
              {{form.id ? item.id ? NP.round(NP.times(NP.minus(item.quantity, item.before_counting), item.purchase_price), 2): value : '-'}}
            </div>
            <div slot="action" slot-scope="value, item, index">
              <a-button-group v-if="!form.id && item.id">
                <a-popover title="修改条目" trigger="click">
                  <div slot="content">
                    <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 12 }">
                      <a-form-model-item label="盘点数量">
                        <a-input-number v-model="item.quantity" style="width: 100%;" />
                      </a-form-model-item>
                    </a-form-model>
                  </div>
                  <a-button size="small">
                    <a-icon type="edit" />
                  </a-button>
                </a-popover>
                <a-button type="danger" size="small" @click="form.goods_set.splice(index, 1)">
                  <a-icon type="close" />
                </a-button>
              </a-button-group>
            </div>
          </a-table>
          <div style="margin-top: 16px;">
            <a-popconfirm title="确定盘点吗?" @confirm="create">
              <a-button v-if="!form.id" type="primary" style="margin-left: 16px;" :loading="buttonLoading">盘点</a-button>
            </a-popconfirm>
            <a-button v-if="form.id" style="margin-left: 16px;" @click="printInvoice">生成打印单据
            </a-button>
            <a-button style="float: right;" @click="resetForm">清空表单</a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
  </div>
</template>

<script>
  import { warehouseList, countingListList, countingListCreate } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'CountingList',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
    },
    data() {
      return {
        NP,
        moment,
        form: {},
        searchForm: { search: '', warehouse: undefined, page: 1 },
        items: [],
        columns: [
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
        ],
        rules: {
          warehouse: [
            { required: true, message: '请选择仓库', trigger: 'change' },
          ],
        },

        warehouseItems: [],
        addGoodsModalVisible: false,
        goodsColumns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '商品',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '编号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '规格',
            dataIndex: 'spec',
            key: 'spec',
          },
          {
            title: '单位',
            dataIndex: 'unit',
            key: 'unit',
          },
          {
            title: '盘点数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '盘点前数量',
            dataIndex: 'before_counting',
            key: 'before_counting',
            scopedSlots: { customRender: 'before_counting' },
          },
          {
            title: '盈亏数量',
            dataIndex: 'profit_quantity',
            key: 'profit_quantity',
            scopedSlots: { customRender: 'profit_quantity' },
          },
          {
            title: '盈亏金额(元)',
            dataIndex: 'profit_amount',
            key: 'profit_amount',
            scopedSlots: { customRender: 'profit_amount' },
          },
            {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],

        tableLoading: false,
        buttonLoading: false,
        currentPage: 1,
        totalRows: 0,
        perPage: 16,
      };
    },
    computed: {
      dataSource() {
        let quantity = 0, before_counting = 0, profit_quantity = 0, profit_amount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
            if (this.form.id) {
              before_counting = NP.plus(before_counting, item.before_counting);
              let quantity = NP.minus(item.quantity, item.before_counting)
              profit_quantity = NP.plus(profit_quantity, quantity);
              profit_amount = NP.plus(profit_amount, NP.times(item.purchase_price, quantity));
            }
          }
        }
        let totalItem = { name: '合计:', quantity, before_counting, profit_quantity, profit_amount };
        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      },
    },
    methods: {
      initialize() {
        this.resetForm();
        this.list();

        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
          })
        
      },
      list() {
        this.tableLoading = true;
        countingListList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
         
          .finally(() => {
            this.tableLoading = false;
          });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            if (this.form.goods_set.length == 0) {
              
                this.$message.error('请选择条目');
              return
            }
            this.buttonLoading = true;
            countingListCreate(this.form)
              .then(resp => {
                this.$message.success('盘点成功');
                this.items.splice(0, 0, resp.data)
                this.resetForm();
              })
              
              .finally(() => {
                this.buttonLoading = false;
              });
          }
        });
      },
      addGoods(goodsItem) {
        this.form.goods_set.push(goodsItem);
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      printInvoice() {
        window.open(`/invoice/counting_list?id=${this.form.id}`);
      },
      customRow(item) {
        return {
          on: {
            click: () => {
              this.$refs.form.clearValidate();
              this.form = { ...item };
            },
          },
        }
      },
      rowClassName(item) {
        if (item.id == this.form.id) {
          return 'table-selected'
        }
      },
      resetForm() {
        this.form = {
          warehouse: null,
          remark: '',
          goods_set: [],
        };
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scope>
  .table-selected {
    background: #e6f7ff;
  }
</style>