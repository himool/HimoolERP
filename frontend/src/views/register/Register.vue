<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="phone" label="手机号">
          <a-input size="large" v-model="form.phone" />
        </a-form-model-item>
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="确认密码">
          <a-input-password size="large" v-model="form.confirm" />
        </a-form-model-item>
      </a-form-model>
    </div>
    <a-row style="margin-bottom: 12px;">
      <a-col offset="12" :span="8">
        <span>已有帐号?</span>
        <a @click="$router.push('/user/login')">返回登录</a>
      </a-col>
    </a-row>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="register">注册</a-button>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { register } from '@/api/user'

  export default {
    name: 'Register',
    data() {
      return {
        isLoading: false,
        captchaLoading: false,
        countdown: 60,
        form: {
          phone: '',
          username: '',
          password: '',
          confirm: '',
        },
        rules: {
          phone: [
            { required: true, message: '请输入手机号', trigger: 'change' },
            { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' },
          ],
          username: [
            { required: true, message: '请输入用户名', trigger: 'change' },
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'change' },
          ],
          confirm: [
            { required: true, message: '请再次输入密码', trigger: 'change' },
            { validator: this.validateConfirm, trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      validateConfirm(rule, value, callback) {
        return value === this.form.password ? callback() : callback(new Error('两次输入密码不一致'))
      },
      register() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.isLoading = true;
            register(this.form)
              .then(() => {
                this.$message.success('注册成功');
                this.$router.push('/user/login');
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.isLoading = false;
              });
          }
        });
      },
    },
  }
</script>