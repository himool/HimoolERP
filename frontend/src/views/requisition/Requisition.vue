<template>
  <div>
    <a-row gutter="8">
      <a-col :span="8">
        <a-card>
            <a-row gutter="8" style="margin-bottom: 8px;">
              <a-col :span="12" style="margin-bottom: 8px;">
                <a-select v-model="searchForm.out_warehouse" placeholder="调出仓库" style="width: 100%;" allowClear @change="search">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                  </a-select-option>
                </a-select>
              </a-col>
              <a-col :span="12" style="margin-bottom: 8px;">
                <a-select v-model="searchForm.into_warehouse" placeholder="调入仓库" style="width: 100%;" allowClear @change="search">
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
        <a-card :title="form.id ? `调拨单 - ${form.id}` : '调拨单'">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-row>
              <a-col :span="12" :xl="8">
                <a-form-model-item prop="out_warehouse" label="调出仓库">
                  <a-select v-model="form.out_warehouse" :disabled="form.id">
                    <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :span="12" :xl="8">
                <a-form-model-item prop="into_warehouse" label="调入仓库">
                  <a-select v-model="form.into_warehouse" :disabled="form.id">
                    <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :span="12" :xl="8">
                <a-form-model-item prop="date" label="日期">
                  <a-date-picker v-model="form.date" :showToday="false" :allowClear="false" :disabled="form.id"
                    style="width: 100%;" />
                </a-form-model-item>
              </a-col>

              <a-col :span="12" :xl="16">
                <a-form-model-item prop="remark" label="备注" :label-col="{ span: 8, xl: 4 }"
                  :wrapper-col="{ span: 16, xl: 20 }">
                  <a-input v-model="form.remark" allowClear :disabled="form.id" />
                </a-form-model-item>
              </a-col>
              <a-col :span="24" :xl="8">
                <a-form-model-item style="float: right;">
                  <a-button type="primary" :disabled="form.id" @click="addGoodsModalVisible = true">
                    <a-icon type="plus" />添加条目</a-button>
                </a-form-model-item>
              </a-col>
            </a-row>
          </a-form-model>

          <a-table :columns="goodsColumns" :data-source="dataSource" :pagination="false" size="small">
            <div slot="index" slot-scope="value, item, index">{{item.id ? index + 1 : ''}}</div>
            <div slot="action" slot-scope="value, item, index">
              <a-button-group v-if="!form.id && item.id">
                <a-popover title="修改条目" trigger="click">
                  <div slot="content">
                    <a-form-model :label-col="{ span: 6 }" :wrapper-col="{ span: 12 }">
                      <a-form-model-item label="调拨数量">
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
            <a-popconfirm title="确定调拨吗?" @confirm="create">
              <a-button v-if="!form.id" type="primary" style="margin-left: 16px;" :loading="buttonLoading">调拨</a-button>
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
  import { warehouseList, requisitionList, requisitionCreate } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'Requisition',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
    },
    data() {
      return {
        moment,
        form: {},
        items: [],
        columns: [
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '调出',
            dataIndex: 'out_warehouse_name',
            key: 'out_warehouse_name',
          },
          {
            title: '调入',
            dataIndex: 'into_warehouse_name',
            key: 'into_warehouse_name',
          },
        ],
        rules: {
          out_warehouse: [
            { required: true, message: '请选择调出仓库', trigger: 'change' },
          ],
          into_warehouse: [
            { required: true, message: '请选择调入仓库', trigger: 'change' },
          ],
          date: [
            { required: true, message: '请选择日期', trigger: 'change' },
          ],
        },
        searchForm: {
          page: 1,
          out_warehouse: undefined,
          into_warehouse: undefined,
          search: '',
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
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '商品',
            dataIndex: 'name',
            key: 'name',
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
            title: '调拨数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
        ],

        tableLoading: false,
        buttonLoading: false,
        totalRows: 0,
        perPage: 15,
      };
    },
    computed: {
      dataSource() {
        let quantity = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
          }
        }
        let totalItem = { name: '合计:', quantity };
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
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.tableLoading = true;

        if (this.searchForm.out_warehouse && this.searchForm.into_warehouse && this.searchForm.out_warehouse === this.searchForm.into_warehouse) {
          
                this.$message.error('调入仓库与调出仓库冲突');
          return
        }
        requisitionList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
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
            if (this.form.out_warehouse === this.form.into_warehouse) {
              
                this.$message.error('调入仓库与调出仓库冲突');
              return
            }

            requisitionCreate(this.form)
              .then(resp => {
                this.$message.success('调拨成功');
                this.items.splice(0, 0, resp.data)
                this.resetForm();
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
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
      search() {
        this.searchForm.page = 1;
        this.list();
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      printInvoice() {
        window.open(`/invoice/requisition?id=${this.form.id}`);
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
          out_warehouse: null,
          into_warehouse: null,
          remark: '',
          date: moment().startOf('day').format(),
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