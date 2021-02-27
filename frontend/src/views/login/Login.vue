<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" placeholder="用户名或手机号" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="7" offset="5">
        <a-button type="link" style="float: left; padding: 0;" @click="$router.push('/user/set_password')">忘记密码
        </a-button>
      </a-col>
      <a-col :span="7">
        <a-button type="link" style="float: right; padding: 0;" @click="$router.push('/user/register')">注册账号</a-button>
      </a-col>
    </a-row>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;"
          @click="login">登录</a-button>
      </a-col>
    </a-row>

    <div style="text-align: center; font-size: 16px; color: #40a9ff; margin-bottom: 24px; margin-top: 28px;">此版本为试用版, 如需定制或购买请联系我们</div>

  </div>
</template>

<script>
  import { login } from '@/api/user'

  export default {
    name: 'Login',
    data() {
      return {
        isLoading: false,
        form: {
          username: '',
          password: '',
        },
        rules: {
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
    created() {
      this.initialize();
    },
  } 
</script>