<template>
  <div>
    <a-modal v-model="visible" title="选择商品" :footer="null" :maskClosable="false" @cancel="$emit('cancel', false)">
      <div>
        <a-input-search v-model="searchText" placeholder="输入查询..." @search="search" />
      </div>
      <div style="margin-top: 12px;">
        <a-table :columns="goodsColumns" :data-source="goodsItems" :loading="loading" size="small" :pagination="false">
          <div slot="action" slot-scope="value, item">
            <a-button size="small" @click="select(item)">选择</a-button>
          </div>
        </a-table>
      </div>
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="currentPage" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-modal>

    <a-modal v-model="formModalVisible" title="新增任务" okText="新增" cancelText="取消" :maskClosable="false" @ok="create">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item label="任务商品">
          <div>{{selectedGoods.name}}</div>
        </a-form-model-item>
        <a-form-model-item label="商品货号">
          <div>{{selectedGoods.code}}</div>
        </a-form-model-item>
        <a-form-model-item prop="warehouse" label="公司">
          <a-select v-model="form.warehouse">
            <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="quantity" label="任务数量">
          <a-input-number v-model="form.quantity" style="width: 100%;" />
        </a-form-model-item>
        <a-form-model-item prop="start_date" label="开始日期">
          <a-date-picker v-model="form.start_date" :showToday="false" :allowClear="false" style="width: 100%;" />
        </a-form-model-item>
        <a-form-model-item prop="end_date" label="截至日期">
          <a-date-picker v-model="form.end_date" :showToday="false" :allowClear="false" style="width: 100%;" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { goodsList } from '@/api/goods'
  import { warehouseList } from '@/api/warehouse'
  import { salesTaskCreate } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'AddTaskModal',
    props: ['visible'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        form: {},
        searchText: '',
        currentPage: 1,
        totalRows: 0,
        perPage: 10,
        loading: false,
        goodsItems: [],
        warehouseItems: [],
        selectedGoods: {},
        goodsColumns: [
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '货号',
            dataIndex: 'code',
            key: 'code',
          },
          {
            title: '选择',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
          },
        ],
        formModalVisible: false,
        rules: {
          warehouse: [
            { required: true, message: '请选择公司', trigger: 'change' },
          ],
          quantity: [
            { required: true, message: '请输入任务数量', trigger: 'change' },
            { validator: this.quantityValidator, trigger: 'change' }
          ],
          start_date: [
            { required: true, message: '请选择开始日期', trigger: 'change' },
          ],
          end_date: [
            { required: true, message: '请选择截至日期', trigger: 'change' },
            { validator: this.endDateValidator, trigger: 'change' },
          ],
        },
      };
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
        this.loading = true;
        goodsList({ search: this.searchText, page: this.currentPage, page_size: this.perPage })
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
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            salesTaskCreate(this.form)
              .then((resp) => {
                this.$message.success('新增成功');
                this.formModalVisible = false;
                this.$emit('create', resp.data);
                this.$emit('cancel', false);
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      search() {
        this.currentPage = 1;
        this.list();
      },
      select(item) {
        this.selectedGoods = item;
        this.form.goods = item.id;
        this.formModalVisible = true;
      },
      confirm() {
        this.productModalVisible = false;
        this.$emit('confirm', { ...this.selectedGoods });
        this.$emit('cancel', false);
      },
      changePage(value) {
        this.currentPage = value;
        this.list();
      },
      quantityValidator(rule, value, callback) {
        return value > 0 ? callback() : callback(new Error('请输入有效任务数量'))
      },
      endDateValidator(rule, value, callback) {
        return moment(value).isBefore(moment().startOf('day')) ? callback(new Error('请选择有效截止日期')) : callback()
      },
      resetForm() {
        this.form = {
          goods: null,
          warehouse: null,
          quantity: 1,
          start_date: moment().startOf('day').format(),
          end_date: moment().startOf('day').format(),
        };
      },
    },
    watch: {
      visible(value) {
        if (value) {
          this.goodsItems = [];
          this.searchText = '';
          this.currentPage = 1;
          this.selectedGoods = {};
          this.formModalVisible = false;
          this.resetForm();
          this.list();
        }
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>