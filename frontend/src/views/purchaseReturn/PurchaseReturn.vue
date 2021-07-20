<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="6">
        <a-card>
          <a-table :columns="columns" :data-source="items" :loading="tableLoading" :pagination="false"
            :customRow="customRow" :rowClassName="rowClassName" size="small">
            <div slot="status" slot-scope="value, item">{{item.is_done ? '已完成' : '等待出库'}}</div>
            <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          </a-table>
          <div style="text-align: center; margin-top: 16px;">
            <a-pagination :value="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
              @change="changePage" />
          </div>
        </a-card>
      </a-col>
      <a-col :span="24" :lg="18">
        <a-card :title="form.id ? `采购退货单 - ${form.id}` : '采购退货单'">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
            <a-row>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="purchase_order" label="关联采购单">
                  <a-button style="width: 100%;" @click="relationModalVisible = true" :disabled="form.id">
                    {{form.purchase_order ? form.purchase_order : '设置'}}</a-button>
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item v-if="form.purchase_order" label="日期">
                  <a-spin v-if="formLoading" size="small"></a-spin>
                  <div v-else>{{moment(purchaseForm.date).format('YYYY-MM-DD')}}</div>
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item v-if="form.purchase_order" label="实付金额">
                  <a-spin v-if="formLoading" size="small"></a-spin>
                  <div v-else>{{purchaseForm.amount}}</div>
                </a-form-model-item>
              </a-col>
            </a-row>
            <div v-if="form.purchase_order">
              <a-table :columns="goodsColumns1" :data-source="purchaseForm.goods_set ? purchaseForm.goods_set : []"
                :loading="formLoading" :pagination="false" size="small">
                <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
                <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
                <div slot="discount_amount" slot-scope="value">{{NP.round(value, 2)}}</div>
              </a-table>
            </div>
            <a-divider />

            <a-row>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="supplier" label="供应商">
                  <a-select v-model="form.supplier" disabled>
                    <a-select-option v-for="item in supplierItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="warehouse" label="仓库">
                  <a-select v-model="form.warehouse" disabled>
                    <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="account" label="结算账户">
                  <a-select v-model="form.account" :disabled="form.id">
                    <a-select-option v-for="item in accountItems" :key="item.id" :value="item.id">{{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>

              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="contacts" label="联系人">
                  <a-select v-model="form.contacts" :disabled="form.id">
                    <a-select-option v-for="item in userItems" :key="item.id" :value="item.id">{{item.username}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="date" label="日期">
                  <a-date-picker v-model="form.date" :showToday="false" :allowClear="false" :disabled="form.id"
                    style="width: 100%;" />
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item prop="amount" label="退款金额">
                  <a-input-number v-model="form.amount" :precision="2" :disabled="form.id" style="width: 100%;" />
                </a-form-model-item>
              </a-col>

              <a-col :sm="12" :xl="16" :xs="24">
                <a-form-model-item prop="remark" label="备注" :label-col="{ span: 8, xl: 4 }"
                  :wrapper-col="{ span: 16, xl: 20 }">
                  <a-input v-model="form.remark" allowClear :disabled="form.id" />
                </a-form-model-item>
              </a-col>
              <a-col :sm="12" :xl="8" :xs="24">
                <a-form-model-item style="float: right;">
                  <a-button type="primary" @click="addGoodsModalVisible = true" :disabled="form.id">
                    <a-icon type="plus" />添加条目</a-button>
                </a-form-model-item>
              </a-col>
            </a-row>
            <div>
              <a-table :columns="goodsColumns2" :data-source="dataSource" :loading="loading" :pagination="false"
                size="small">
                <div slot="index" slot-scope="value, item, index">{{item.isTotal ?  '' : index + 1}}</div>
                <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
                <div slot="discount_amount" slot-scope="value">{{NP.round(value, 2)}}</div>

                <div slot="action" slot-scope="value, item, index">
                  <a-button-group v-if="!form.id && !item.isTotal">
                    <a-popover title="修改条目" trigger="click">
                      <div slot="content">
                        <a-form-model :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
                          <a-form-model-item label="数量">
                            <a-input-number v-model="item.quantity" style="width: 100%;" @change="computeGoods(item)" />
                          </a-form-model-item>
                          <a-form-model-item label="单价">
                            <a-input-number v-model="item.purchase_price" :precision="2" style="width: 100%;"
                              @change="computeGoods(item)" />
                          </a-form-model-item>
                          <a-form-model-item label="折扣">
                            <a-input-number v-model="item.discount" :precision="0" :min="0" :max="100" :step="5"
                              :formatter="value => `${value}%`" :parser="value => value.replace('%', '')"
                              style="width: 100%;" @change="computeGoods(item)" />
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
            </div>
          </a-form-model>
          <div style="margin-top: 16px;">
            <a-popconfirm v-if="form.id && !form.is_done" title="确定删除吗?" @confirm="destroy">
              <a-button type="danger" style="margin-right: 16px;">删除</a-button>
            </a-popconfirm>
            <a-popconfirm v-if="!form.id" title="确定退货吗?" @confirm="create">
              <a-button type="primary" :loading="buttonLoading" @click="create">退货</a-button>
            </a-popconfirm>
            <a-button v-else @click="printInvoice">生成打印单据</a-button>
            <a-button style="float: right;" @click="resetForm">清空表单</a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <relation-modal v-model="relationModalVisible" @select="selectPurchase" />
    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
  </div>
</template>

<script>
  import { supplierList, purchaseOrderList, purchaseOrderCreate, purchaseOrderRetrieve, purchaseOrderDestroy } from '@/api/purchase'
  import { accountList, userList } from '@/api/account'
  import { warehouseList } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseReturn',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
      RelationModal: () => import('./RelationModal.vue'),
    },
    data() {
      return {
        NP,
        moment,
        form: {},
        purchaseForm: {},
        searchForm: { page: 1, is_return: true },
        items: [],
        supplierItems: [],
        warehouseItems: [],
        accountItems: [],
        userItems: [],

        tableLoading: false,
        buttonLoading: false,
        formLoading: false,
        totalRows: 0,
        perPage: 15,

        addGoodsModalVisible: false,
        relationModalVisible: false,
        rules: {
          purchase_order: [{ required: true, message: '请选择关联单', trigger: 'change' }],
          supplier: [{ required: true, message: '请选择供应商', trigger: 'change' }],
          warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
          account: [{ required: true, message: '请选择账户', trigger: 'change' }],
          contacts: [{ required: true, message: '请选择联系人', trigger: 'change' }],
          amount: [{ required: true, message: '请输入金额', trigger: 'change' }],
          date: [{ required: true, message: '请选择日期', trigger: 'change' }],
        },
        columns: [
          {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            scopedSlots: { customRender: 'status' },
          },
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
            scopedSlots: { customRender: 'date' },
          },
          {
            title: '供应商',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
        ],
        goodsColumns1: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            scopedSlots: { customRender: 'index' },
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
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '单价',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
          },
          {
            title: '折扣',
            dataIndex: 'discount',
            key: 'discount',
          },
          {
            title: '折后价',
            dataIndex: 'discount_price',
            key: 'discount_price',
          },
          {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
            scopedSlots: { customRender: 'amount' },
          },
          {
            title: '折后金额',
            dataIndex: 'discount_amount',
            key: 'discount_amount',
            scopedSlots: { customRender: 'discount_amount' },
          },
        ],
        goodsColumns2: [
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
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
          },
          {
            title: '单价',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            customRender: (value, item) => {
              return item.isTotal ? '' : NP.round(value, 2)
            },
          },
          {
            title: '折扣',
            dataIndex: 'discount',
            key: 'discount',
            customRender: (value, item) => {
              return item.isTotal ? '' : `${value} %`
            },
          },
          {
            title: '折后价',
            dataIndex: 'discount_price',
            key: 'discount_price',
            customRender: (value, item) => {
              return item.isTotal ? '' : NP.round(value, 2)
            },
          },
          {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
            scopedSlots: { customRender: 'amount' },
          },
          {
            title: '折后金额',
            dataIndex: 'discount_amount',
            key: 'discount_amount',
            scopedSlots: { customRender: 'discount_amount' },
          },
        ],
      };
    },
    computed: {
      total() {
        let quantity = 0, amount = 0, discount_amount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
            amount = NP.plus(amount, item.amount);
            discount_amount = NP.plus(discount_amount, item.discount_amount);
          }
        }
        return { quantity, amount, discount_amount }
      },
      dataSource() {
        let totalItem = { name: '合计:', isTotal: true, ...this.total };
        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      }
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

        supplierList()
          .then(resp => {
            this.supplierItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });

        accountList()
          .then(resp => {
            this.accountItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });

        userList()
          .then(resp => {
            this.userItems = resp.data;
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.tableLoading = true;
        purchaseOrderList(this.searchForm)
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
            this.buttonLoading = true;
            purchaseOrderCreate(this.form)
              .then(resp => {
                this.$message.success('退货成功');
                this.items.splice(0, 0, resp.data)
                this.form = resp.data;
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
      retrieve() {
        this.purchaseForm = {};
        this.formLoading = true;
        purchaseOrderRetrieve({ id: this.form.purchase_order })
          .then(resp => {
            if (resp.data.id == this.form.purchase_order) {
              this.purchaseForm = resp.data;
              this.formLoading = false;
            }
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      destroy() {
        let form = { ...this.form };
        purchaseOrderDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
            this.resetForm();
          })
          .catch(err => {
            
                this.$message.error(err.response.data.message);
          });
      },
      addGoods(goodsItem) {
        goodsItem.discount = 100;
        this.computeGoods(goodsItem);
        this.form.goods_set.push(goodsItem);
      },
      computeGoods(goodsItem) {
        goodsItem.discount_price = NP.times(goodsItem.purchase_price, goodsItem.discount, 0.01);
        goodsItem.amount = NP.times(goodsItem.purchase_price, goodsItem.quantity);
        goodsItem.discount_amount = NP.times(goodsItem.purchase_price, goodsItem.quantity, goodsItem.discount, 0.01);
      },
      selectPurchase(item) {
        this.form.purchase_order = item.id;
        this.purchaseForm = item;
        this.form.supplier = item.supplier;
        this.form.warehouse = item.warehouse;
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      printInvoice() {
        window.open(`/invoice/purchase?id=${this.form.id}`);
      },
      customRow(item) {
        return {
          on: {
            click: () => {
              this.$refs.form.clearValidate();
              this.form = { ...item };
              this.retrieve();
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
          supplier: null,
          warehouse: null,
          account: null,
          contacts: null,
          amount: 0.0,
          date: moment().startOf('day').format(),
          remark: '',
          goods_set: [],
          purchase_order: null,
          is_return: true,
        };
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
  .table-selected {
    background: #e6f7ff;
  }
</style>