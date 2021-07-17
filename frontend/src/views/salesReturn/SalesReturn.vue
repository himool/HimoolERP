<template>
  <div>
    <a-card>
      <div slot="title">
        <a-button type="primary" @click="addGoodsModalVisible = true">
          <a-icon type="plus" />添加条目
        </a-button>
        <a-button style="margin-left: 12px;" @click="resetForm">空白退货单</a-button>
        <a-popconfirm title="确定退货吗?" @confirm="create">
          <a-button type="primary" style="float: right;" :loading="loading">退货</a-button>
        </a-popconfirm>
      </div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 10 }" :wrapper-col="{ span: 14 }">

        <a-row gutter="12">
          <a-col :span="18">
            <a-col :span="9">
              <a-form-model-item prop="sales_order" label="关联销售单" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
                <a-button style="width: 100%;" @click="relationModalVisible = true">
                  {{form.sales_order ? form.sales_order : '设置'}}</a-button>
              </a-form-model-item>
            </a-col>
            <a-col :span="5">
              <a-form-model-item v-if="form.sales_order" label="日期">
                <div>{{moment(salesForm.date).format('YYYY-MM-DD')}}</div>
              </a-form-model-item>
            </a-col>
            <a-col :span="5">
              <a-form-model-item v-if="form.sales_order" label="整单折扣">
                <div>{{salesForm.discount}} %</div>
              </a-form-model-item>
            </a-col>
            <a-col :span="5">
              <a-form-model-item v-if="form.sales_order" label="实收金额">
                <div>{{salesForm.amount}}</div>
              </a-form-model-item>
            </a-col>
            <div v-if="form.sales_order">
              <a-table :columns="goodsColumns1" :data-source="salesForm.goods_set ? salesForm.goods_set : []"
                :loading="formLoading" :pagination="false" size="small">
                <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
                <div slot="amount" slot-scope="value">{{NP.round(value, 2)}}</div>
              </a-table>
            </div>
            <a-divider></a-divider>

            <a-table :columns="goodsColumns2" :data-source="dataSource" :pagination="false" size="small">
              <div slot="index" slot-scope="value, item, index">{{item.isTotal ?  '' : index + 1}}</div>
              <div slot="amount" slot-scope="value, item">
                {{NP.round(item.isTotal ? value : NP.times(item.quantity, item.retail_price), 2)}}
              </div>
              <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal">
                  <a-popover title="修改条目" trigger="click">
                    <div slot="content">
                      <a-form-model :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
                        <a-form-model-item label="单价">
                          <a-input-number v-model="item.retail_price" :precision="2" style="width: 100%;" />
                        </a-form-model-item>
                        <a-form-model-item label="备注">
                          <a-input v-model="item.remark" allowClear />
                        </a-form-model-item>
                      </a-form-model>
                    </div>
                    <a-button type="primary" size="small">
                      <a-icon type="edit" />
                    </a-button>
                  </a-popover>
                  <a-button size="small" @click="item.quantity += 1">
                    <a-icon type="plus" />
                  </a-button>
                  <a-button size="small" @click="item.quantity -= 1">
                    <a-icon type="minus" />
                  </a-button>
                  <a-button type="danger" size="small" @click="form.goods_set.splice(index, 1)">
                    <a-icon type="close" />
                  </a-button>
                </a-button-group>
              </div>
            </a-table>
          </a-col>
          <a-col :span="6">
            <a-form-model-item prop="discount" label="整单折扣">
              <a-input-number v-model="form.discount" :precision="0" :min="0" :max="100" :step="5"
                :formatter="value => `${value}%`" :parser="value => value.replace('%', '')" style="width: 100%;" />
            </a-form-model-item>
            <a-form-model-item prop="date" label="日期">
              <a-date-picker v-model="form.date" :showToday="false" :allowClear="false" style="width: 100%;" />
            </a-form-model-item>
            <a-form-model-item prop="seller" label="销售员">
              <a-select v-model="form.seller">
                <a-select-option v-for="value in sellerItems" :key="value" :value="value">{{value}}
                </a-select-option>
              </a-select>
            </a-form-model-item>
            <a-form-model-item prop="warehouse" label="仓库">
              <a-select v-model="form.warehouse" disabled>
                <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
                </a-select-option>
              </a-select>
            </a-form-model-item>
            <a-form-model-item prop="account" label="结算账户">
              <a-select v-model="form.account">
                <a-select-option v-for="item in accountItems" :key="item.id" :value="item.id">{{item.name}}
                </a-select-option>
              </a-select>
            </a-form-model-item>
            <a-form-model-item prop="amount" label="退款金额">
              <a-input-number v-model="form.amount" :precision="2" style="width: 100%;" />
            </a-form-model-item>
            <a-form-model-item prop="client_contacts" label="联系人">
              <a-input v-model="form.client_contacts" disabled />
            </a-form-model-item>
            <a-form-model-item prop="client_phone" label="客户手机">
              <a-input v-model="form.client_phone" disabled />
            </a-form-model-item>
            <a-form-model-item prop="client_name" label="客户名称">
              <a-input v-model="form.client_name" disabled />
            </a-form-model-item>
            <a-form-model-item prop="client_address" label="客户地址">
              <a-input v-model="form.client_address" disabled />
            </a-form-model-item>
            <a-form-model-item prop="remark" label="客户备注">
              <a-input v-model="form.remark" />
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
    </a-card>

    <relation-modal v-model="relationModalVisible" @select="selectSales" />
    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
  </div>
</template>

<script>
  import { warehouseList } from '@/api/warehouse'
  import { accountList, sellertList } from '@/api/account'
  import { salesOrderCreate } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesReturn',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
      RelationModal: () => import('./RelationModal.vue'),
    },
    data() {
      return {
        NP,
        moment,
        form: {},
        salesForm: {},
        warehouseItems: [],
        accountItems: [],
        addGoodsModalVisible: false,
        relationModalVisible: false,
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
            dataIndex: 'retail_price',
            key: 'retail_price',
          },
          {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
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
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '名称',
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
            dataIndex: 'retail_price',
            key: 'retail_price',
          },
          {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
            scopedSlots: { customRender: 'amount' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px'
          },
        ],
        formLoading: false,
        buttonLoading: false,
        rules: {
          discount: [{ required: true, message: '请输入整单折扣', trigger: 'change' }],
          date: [{ required: true, message: '请选择日期', trigger: 'change' }],
          seller: [{ required: true, message: '请选择供应商', trigger: 'change' }],
          warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
          account: [{ required: true, message: '请选择账户', trigger: 'change' }],
          amount: [{ required: true, message: '请输入实收金额', trigger: 'change' }],
          sales_order: [{ required: true, message: '请选择关联单', trigger: 'change' }],
        },
      };
    },
    computed: {
      dataSource() {
        let totalQuantity = 0, totalAmount = 0;
        if (this.form.goods_set) {
          for (let item of this.form.goods_set) {
            totalQuantity += item.quantity;
            totalAmount = NP.times(item.quantity, item.retail_price);
          }
        }

        let totalItem = {
          name: '合计:',
          quantity: totalQuantity,
          amount: NP.times(totalAmount, this.form.discount ? this.form.discount : 100, 0.01),
          isTotal: true,
        };

        return this.form.goods_set ? [...this.form.goods_set, totalItem] : [totalItem];
      }
    },
    methods: {
      initialize() {
        this.resetForm();
        warehouseList()
          .then(resp => {
            this.warehouseItems = resp.data;
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

        sellertList()
          .then(resp => {
            this.sellerItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            if (this.form.goods_set.length == 0) {
              this.$message.error('请选择条目');
              return
            }
            this.loading = true;
            salesOrderCreate(this.form)
              .then(() => {
                this.$message.success('退货成功');
                this.resetForm();
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.loading = false;
              });
          }
        });
      },
      addGoods(goodsItem) {
        goodsItem.remark = '';
        this.form.goods_set.push(goodsItem);
      },
      selectSales(item) {
        this.form.sales_order = item.id;
        this.salesForm = item;
        this.form.client_phone = item.client_phone;
        this.form.client_name = item.client_name;
        this.form.client_contacts = item.client_contacts;
        this.form.client_address = item.client_address;
        this.form.warehouse = item.warehouse;
      },
      resetForm() {
        this.form = {
          date: moment().startOf('day').format(),
          warehouse: null,
          account: null,
          seller: null,
          amount: 0.0,
          client_phone: '',
          client_contacts: '',
          client_name: '',
          client_address: '',
          remark: '',
          discount: 100,
          goods_set: [],
          sales_order: null,
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
</style>