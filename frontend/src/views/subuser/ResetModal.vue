<template>
  <div>
    <a-modal v-model="visible" okText="重置" :maskClosable="false" @ok="reset" @cancel="cancel">
      <div slot="title">重置密码: {{form.username}}</div>

      <a-form-model ref="resetForm" :model="resetForm" :rules="rules" :label-col="{ span: 4 }"
        :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="resetForm.password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="确认密码">
          <a-input-password size="large" v-model="resetForm.confirm" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { subuserReset } from '@/api/account'

  export default {
    name: 'ResetModal',
    props: ['visible', 'form'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        resetForm: {
          password: '',
          confirm: '',
        },
        rules: {
          password: [{ required: true, message: '请输入密码', trigger: 'change' }],
          confirm: [
            { required: true, message: '请再次输入密码', trigger: 'change' },
            { validator: this.validateConfirm, trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      reset() {
        this.$refs.resetForm.validate(valid => {
          if (valid) {
            subuserReset({ username: this.form.username, password: this.resetForm.password })
              .then(() => {
                this.$message.success('重置成功');
                this.cancel();
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.resetForm = {
          password: '',
          confirm: '',
        };
        this.$refs.resetForm.resetFields();

      },
      validateConfirm(rule, value, callback) {
        return value === this.resetForm.password ? callback() : callback(new Error('两次输入密码不一致'))
      },
    },
  }
</script>