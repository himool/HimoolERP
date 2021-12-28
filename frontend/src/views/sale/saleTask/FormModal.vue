<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑销售任务' : '新增销售任务' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="任务商品">
            {{ form.name }}
            <a-button type="primary" icon="plus" @click="materialsSelectModalVisible = true" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="商品编号">
            {{ form.number }}
          </a-form-model-item>
          <a-form-model-item prop="warehouse" label="仓库">
            <a-select v-model="form.warehouse" style="width: 100%">
              <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="salesperson" label="销售员">
            <a-select v-model="form.salesperson" style="width: 100%">
              <a-select-option v-for="item in clientsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="total_quantity" label="任务总量">
            <a-input-number v-model="form.total_quantity" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="start_time" label="开始时间">
            <a-date-picker v-model="form.start_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="end_time" label="结算时间">
            <a-date-picker v-model="form.end_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
          </a-form-model-item>
        </a-form-model>
      </div>
      <goods-select-modal v-model="materialsSelectModalVisible" :warehouse="form.warehouse" @select="onSelectMaterial"></goods-select-modal>
    </a-modal>
  </div>
</template>

<script>
  import { saleTaskCreate } from '@/api/sale'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'warehouseItems', 'clientsItems'],
    model: { prop: 'visible', event: 'cancel' },
    components: {
      GoodsSelectModal: () => import('@/components/GoodsSelectModal/index'),
    },
    data() {
      return {
        goods: null,
        materialsSelectModalVisible: false,
        rules: {
          name: [{ required: true, message: '请选择任务商品', trigger: 'change' }],
          warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
          salesperson: [{ required: true, message: '请选择销售员', trigger: 'change' }],
          total_quantity: [{ required: true, message: '请输入任务总量', trigger: 'change' }],
          start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
          end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? saleTaskCreate : saleTaskCreate;
            func({...this.form, goods: this.goods }).then(data => {
              this.$message.success(this.form.id ? '修改成功' : '新增成功');
              this.$emit(this.form.id ? 'update' : 'create', data);
              this.cancel();
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.$refs.form.resetFields();
      },
      onSelectMaterial(item) {
        this.goods = item.id;
        this.$set(this.form,'name',item.name);
        this.$set(this.form,'number',item.number);
      },
    },
  }
</script>

<style scoped>
</style>