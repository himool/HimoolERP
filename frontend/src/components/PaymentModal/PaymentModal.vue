<template>
  <div>
    <a-modal v-model="visible" :title="`付款 - ${order.id}`" :maskClosable="false" @cancel="cancel" @ok="create">
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item label="总金额">
            <div>{{order.total_amount}}</div>
          </a-form-model-item>
          <a-form-model-item label="已付金额">
            <div>{{order.amount}}</div>
          </a-form-model-item>
          <a-form-model-item prop="account" label="结算账户">
            <a-select v-model="form.account">
              <a-select-option v-for="item in accountItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="amount" label="付款金额">
            <a-input-number v-model="form.amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="备注">
            <a-input v-model="form.remark" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { accountList } from '@/api/account'
  import NP from 'number-precision'

  export default {
    name: 'PaymentModal',
    props: ['visible', 'order'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        form: { account: undefined, amount: 0, remark: '' },
        rules: {
          amount: [
            { required: true, message: '请输入金额', trigger: 'change' },
            { validator: this.validateAmount, trigger: 'blur' },
          ],
          account: [{ required: true, message: '请选择账户', trigger: 'change' }]
        },
      };
    },
    methods: {
      initialize() {
        accountList()
          .then(resp => {
            this.accountItems = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.$emit('payment', { id: this.order.id, ...this.form });
          }
        })
      },
      cancel() {
        this.$emit('cancel', false);
        this.resetForm();
      },
      validateAmount(rule, value, callback) {
        let remainAmount = NP.minus(this.order.total_amount, this.order.amount);
        return value > 0 && value <= remainAmount ? callback() : callback(new Error('金额错误'))
      },
      resetForm() {
        this.form = { account: undefined, amount: 0, remark: '' };
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>