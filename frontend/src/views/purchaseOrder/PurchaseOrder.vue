<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :lg="6">
        <a-card>
          <a-table :columns="purchaseColumns" :data-source="purchaseItems" :loading="tableLoading" :pagination="false"
            :customRow="customRow" :rowClassName="rowClassName" size="small">
            <div slot="status" slot-scope="value, item">{{item.is_done ? '已完成' : '等待入库'}}</div>
            <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
          </a-table>
          <div style="text-align: center; margin-top: 16px;">
            <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
              @change="changePage" />
          </div>
        </a-card>
      </a-col>
      <a-col :span="24" :lg="18">
        <a-card :title="purchaseForm.id ? `采购单 - ${purchaseForm.id}` : '采购单'">
          <div>
            <a-form-model ref="purchaseForm" :model="purchaseForm" :rules="rules" :label-col="{ span: 8 }"
              :wrapper-col="{ span: 16 }">
              <a-row>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="supplier" label="供应商">
                    <a-select v-model="purchaseForm.supplier" :disabled="purchaseForm.id">
                      <a-select-option v-for="item in supplierItems" :key="item.id" :value="item.id">{{item.name}}
                      </a-select-option>
                    </a-select>
                  </a-form-model-item>
                </a-col>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="warehouse" label="仓库">
                    <a-select v-model="purchaseForm.warehouse" :disabled="purchaseForm.id">
                      <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                      </a-select-option>
                    </a-select>
                  </a-form-model-item>
                </a-col>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="account" label="结算账户">
                    <a-select v-model="purchaseForm.account" :disabled="purchaseForm.id">
                      <a-select-option v-for="item in accountItems" :key="item.id" :value="item.id">{{item.name}}
                      </a-select-option>
                    </a-select>
                  </a-form-model-item>
                </a-col>

                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="contacts" label="联系人">
                    <a-select v-model="purchaseForm.contacts" :disabled="purchaseForm.id">
                      <a-select-option v-for="item in userItems" :key="item.id" :value="item.id">{{item.username}}
                      </a-select-option>
                    </a-select>
                  </a-form-model-item>
                </a-col>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="date" label="日期">
                    <a-date-picker v-model="purchaseForm.date" :showToday="false" :allowClear="false"
                      :disabled="purchaseForm.id" style="width: 100%;" />
                  </a-form-model-item>
                </a-col>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item prop="amount" label="实付金额">
                    <a-input-number v-model="purchaseForm.amount" :precision="2" :disabled="purchaseForm.id"
                      style="width: 100%;" />
                  </a-form-model-item>
                </a-col>

                <a-col :sm="12" :xl="16" :xs="24">
                  <a-form-model-item prop="remark" label="备注" :label-col="{ span: 8, xl: 4 }"
                    :wrapper-col="{ span: 16, xl: 20 }">
                    <a-input v-model="purchaseForm.remark" allowClear :disabled="purchaseForm.id" />
                  </a-form-model-item>
                </a-col>
                <a-col :sm="12" :xl="8" :xs="24">
                  <a-form-model-item style="float: right;">
                    <a-button type="primary" @click="addGoodsModalVisible = true" :disabled="purchaseForm.id">
                      <a-icon type="plus" />添加条目
                    </a-button>
                  </a-form-model-item>
                </a-col>
              </a-row>

            </a-form-model>
          </div>
          <div style="margin: 16px 0;">
            <a-table :columns="goodsColumns" :data-source="dataSource" :loading="loading" :pagination="false"
              size="small">
              <div slot="index" slot-scope="value, item, index">{{item.isTotal ? '' : index + 1}}</div>
              <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
              <div slot="discount_amount" slot-scope="value">{{NP.round(value, 2)}}</div>

              <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!purchaseForm.id && !item.isTotal">
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
                        <!-- <a-form-model-item style="text-align: center;">
                          <a-checkbox @change="item.is_calculate_avg = !item.is_calculate_avg">自动计算平均采购价</a-checkbox>
                        </a-form-model-item> -->
                      </a-form-model>
                    </div>
                    <a-button size="small">
                      <a-icon type="edit" />
                    </a-button>
                  </a-popover>
                  <a-button type="danger" size="small" @click="purchaseForm.goods_set.splice(index, 1)">
                    <a-icon type="close" />
                  </a-button>
                </a-button-group>
              </div>
            </a-table>
          </div>
          <div>
            <a-popconfirm v-if="purchaseForm.id && !purchaseForm.is_done" title="确定删除吗?" @confirm="destroy">
              <a-button type="danger" style="margin-right: 16px;">删除</a-button>
            </a-popconfirm>
            <a-popconfirm v-if="!purchaseForm.id" title="确定采购吗?" @confirm="create">
              <a-button type="primary" :loading="buttonLoading">采购</a-button>
            </a-popconfirm>
            <a-button v-else @click="printInvoice">生成打印单据</a-button>
            <a-button style="float: right;" @click="resetForm">清空表单</a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
  </div>
</template>

<script>
  import { supplierList, purchaseOrderList, purchaseOrderCreate, purchaseOrderDestroy } from '@/api/purchase'
  import { accountList, userList } from '@/api/account'
  import { warehouseList } from '@/api/warehouse'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'PurchaseOrder',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
    },
    data() {
      return {
        NP,
        moment,
        purchaseForm: {},
        purchaseItems: [],
        supplierItems: [],
        warehouseItems: [],
        accountItems: [],
        userItems: [],
        tableLoading: false,
        buttonLoading: false,
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
        purchaseColumns: [
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
        currentPage: 1,
        totalRows: 0,
        perPage: 15,

        addGoodsModalVisible: false,

        rules: {
          supplier: [{ required: true, message: '请选择供应商', trigger: 'change' }],
          warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
          account: [{ required: true, message: '请选择账户', trigger: 'change' }],
          contacts: [{ required: true, message: '请选择联系人', trigger: 'change' }],
          amount: [{ required: true, message: '请输入金额', trigger: 'change' }],
          date: [{ required: true, message: '请选择日期', trigger: 'change' }],
        },
      };
    },
    computed: {
      total() {
        let quantity = 0, amount = 0, discount_amount = 0;
        if (this.purchaseForm.goods_set) {
          for (let item of this.purchaseForm.goods_set) {
            quantity = NP.plus(quantity, item.quantity);
            amount = NP.plus(amount, item.amount);
            discount_amount = NP.plus(discount_amount, item.discount_amount);
          }
        }
        return { quantity, amount, discount_amount }
      },
      dataSource() {
        let totalItem = { name: '合计:', isTotal: true, ...this.total };
        return this.purchaseForm.goods_set ? [...this.purchaseForm.goods_set, totalItem] : [totalItem];
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
            console.log(resp.data)
            this.userItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      list() {
        this.tableLoading = true;
        purchaseOrderList({ page: this.currentPage, is_return: false })
          .then(resp => {
            this.totalRows = resp.data.count;
            this.purchaseItems = resp.data.results;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.tableLoading = false;
          });
      },
      create() {
        this.$refs.purchaseForm.validate(valid => {
          if (valid) {
            console.log(this.purchaseForm);
            if (this.purchaseForm.goods_set.length == 0) {
              this.$message.error('请选择条目');
              return
            }
            this.buttonLoading = true;
            let form = { ...this.purchaseForm };

            purchaseOrderCreate(form)
              .then(resp => {
                this.$message.success('新增成功');
                this.purchaseItems.splice(0, 0, resp.data)
                this.purchaseForm = resp.data;
              })
              .catch(err => {
                console.log(err.response.data);
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.buttonLoading = false;
              });
          }
        });
      },
      destroy() {
        let form = { ...this.purchaseForm };
        purchaseOrderDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.purchaseItems.splice(this.purchaseItems.findIndex(item => item.id === form.id), 1);
            this.resetForm();
          })
          .catch(err => {

            this.$message.error(err.response.data.message);
          });
      },
      addGoods(goodsItem) {
        // goodsItem.is_calculate_avg = false;
        goodsItem.discount = 100;
        this.computeGoods(goodsItem);
        this.purchaseForm.goods_set.push(goodsItem);
      },
      computeGoods(goodsItem) {
        goodsItem.discount_price = NP.times(goodsItem.purchase_price, goodsItem.discount, 0.01);
        goodsItem.amount = NP.times(goodsItem.purchase_price, goodsItem.quantity);
        goodsItem.discount_amount = NP.times(goodsItem.purchase_price, goodsItem.quantity, goodsItem.discount, 0.01);
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      printInvoice() {
        window.open(`/invoice/purchase?id=${this.purchaseForm.id}`);
      },
      customRow(item) {
        return {
          on: {
            click: () => {
              this.$refs.purchaseForm.clearValidate();
              this.purchaseForm = { ...item };
            },
          },
        }
      },
      rowClassName(item) {
        if (item.id == this.purchaseForm.id) {
          return 'table-selected'
        }
      },
      resetForm() {
        this.purchaseForm = {
          supplier: null,
          warehouse: null,
          account: null,
          contacts: null,
          amount: 0.0,
          date: moment().startOf('day').format(),
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