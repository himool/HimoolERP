<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="number" label="序号">
          <a-input size="large" v-model="form.number" placeholder="序号" />
        </a-form-model-item>
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" placeholder="用户名或手机号" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="login">登录</a-button>
      </a-col>
    </a-row>

    <div style="text-align: center; width: 100%; margin-top: 24px;">
      <div>
        试用或购买请扫描下方客服经理微信二维码咨询
      </div>
      <div>
        <img :src="wechatCustomerService" width="100" style="margin-top: 8px;" />
      </div>
    </div>

  </div>
</template>

<script>
  import { login } from '@/api/user'

  export default {
    name: 'Login',
    data() {
      return {
        wechatCustomerService: require('@/assets/wechat_customer_service.png'),
        isLoading: false,
        form: {
          number : '',
          username: '',
          password: '',
        },
        rules: {
          number:[
             { required: true, message: '请输入序号', trigger: 'change' },
          ],
          username: [
            { required: true, message: '请输入用户名', trigger: 'change' },
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'change' },
          ],
        },
      };
    },
    methods: {
      initialize() {
        document.onkeypress = (e) => {
          let code = document.all ? event.keyCode : e.which;
          if (code == 13) {
            this.login();
            return false;
          }
        }
      },
      login() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.isLoading = true;
            login(this.form)
              .then(() => {
                this.$router.push('/home');
              })
            
              .finally(() => {
                this.isLoading = false;
              });
          }
        });
      },
    },
    created() {
      this.initialize();
    },
  }
</script>