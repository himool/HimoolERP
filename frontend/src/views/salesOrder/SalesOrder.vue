<template>
  <div>
    <a-card>
      <div slot="title">
        <a-button type="primary" @click="addGoodsModalVisible = true">
          <a-icon type="plus" />添加条目
        </a-button>
        <a-button style="margin-left: 12px;" @click="resetForm">空白零售单</a-button>
        <a-popconfirm title="确定结账吗?" @confirm="create">
          <a-button type="primary" style="float: right;" :loading="loading">结账</a-button>
        </a-popconfirm>
      </div>
      <a-row gutter="12">
        <a-col :span="18">
          <a-table :columns="columns" :data-source="dataSource" :pagination="false" size="small">
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
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
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
            <a-form-model-item prop="warehouse" label="公司">
              <a-select v-model="form.warehouse">
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
            <a-form-model-item prop="amount" label="实收金额">
              <a-input-number v-model="form.amount" :precision="2" style="width: 100%;" />
            </a-form-model-item>

            <a-form-model-item :wrapperCol="{ offset: 8 }">
              <a-button type="primary" style="width: 100%;" @click="clientModalVisible = true">选择已有客户</a-button>
            </a-form-model-item>

            <a-form-model-item prop="client_contacts" label="联系人">
              <a-input v-model="form.client_contacts" allowClear />
            </a-form-model-item>
            <a-form-model-item prop="client_phone" label="客户手机">
              <a-input v-model="form.client_phone" allowClear />
            </a-form-model-item>
            <a-form-model-item prop="client_name" label="客户名称">
              <a-input v-model="form.client_name" allowClear />
            </a-form-model-item>
            <a-form-model-item prop="client_address" label="客户地址">
              <a-input v-model="form.client_address" allowClear />
            </a-form-model-item>
            <a-form-model-item prop="remark" label="客户备注">
              <a-input v-model="form.remark" allowClear />
            </a-form-model-item>
          </a-form-model>
        </a-col>
      </a-row>
    </a-card>

    <add-goods-modal v-model="addGoodsModalVisible" @confirm="addGoods" />
    <client-modal v-model="clientModalVisible" @confirm="selectClient" />
  </div>
</template>

<script>
  import { warehouseList } from '@/api/warehouse'
  import { accountList, sellertList } from '@/api/account'
  import { salesOrderCreate } from '@/api/sales'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesOrder',
    components: {
      AddGoodsModal: () => import('@/components/AddGoodsModal/AddGoodsModal.vue'),
      ClientModal: () => import('@/components/ClientModal/ClientModal.vue'),
    },
    data() {
      return {
        NP,
        form: {},
        warehouseItems: [],
        accountItems: [],
        sellerItems: [],
        columns: [
          {
            title: '#',
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
        loading: false,
        addGoodsModalVisible: false,
        clientModalVisible: false,

        rules: {
          discount: [{ required: true, message: '请输入整单折扣', trigger: 'change' }],
          date: [{ required: true, message: '请选择日期', trigger: 'change' }],
          seller: [{ required: true, message: '请选择供应商', trigger: 'change' }],
          warehouse: [{ required: true, message: '请选择公司', trigger: 'change' }],
          account: [{ required: true, message: '请选择账户', trigger: 'change' }],
          amount: [{ required: true, message: '请输入实收金额', trigger: 'change' }],
          client_phone: [{ pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' }]
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
                this.$message.success('结账成功');
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
      selectClient(item) {
        this.form.client_phone = item.phone;
        this.form.client_contacts = item.contacts;
        this.form.client_name = item.name;
        this.form.client_address = item.address;
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
        };
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>