<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="company_name" label="公司名称">
          <a-input size="large" v-model="form.company_name" />
        </a-form-model-item>
        <a-form-model-item prop="name" label="姓名">
          <a-input size="large" v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item prop="phone" label="手机号">
          <a-input size="large" v-model="form.phone" />
        </a-form-model-item>
        <a-form-model-item prop="code" label="验证码">
          <a-input-search v-model="form.code" size="large" @search="getCaptcha">
            <a-button slot="enterButton" type="primary" :loading="captchaLoading" style="font-size: 14px;">
              {{captchaLoading ? countdown : '获取验证码'}}</a-button>
          </a-input-search>
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
    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="link" style="float: left; padding: 0;" @click="$router.push('/user/login')">返回登录</a-button>
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
  import { register, getCaptcha } from '@/api/user'

  export default {
    name: 'Register',
    data() {
      return {
        isLoading: false,
        captchaLoading: false,
        countdown: 60,
        form: {
          company_name: '',
          name: '',
          phone: '',
          code: '',
          username: '',
          password: '',
          confirm: '',
        },
        rules: {
          company_name: [
            { required: true, message: '请输入公司名称', trigger: 'change' },
          ],
          name: [
            { required: true, message: '请输入姓名', trigger: 'change' },
          ],
          phone: [
            { required: true, message: '请输入手机号', trigger: 'change' },
            { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' },
          ],
          code: [
            { required: true, message: '请输入验证码', trigger: 'change' },
            { len: 6, message: '请检查验证码 (6位)', trigger: 'blur' },
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
      countSecond() {
        this.countdown -= 1;
        if (this.countdown >= 0) {
          window.setTimeout(this.countSecond, 1000);
        } else {
          this.countdown = 60;
          this.captchaLoading = false;
        }
      },
      getCaptcha() {  // 验证码
        this.$refs.form.validateField(['phone'], (err) => {
          if (!err) {
            this.captchaLoading = true;
            this.countSecond();

            getCaptcha({ phone: this.form.phone })
              .then(() => {
                this.$message.success('验证码发送成功');
              })
              .catch(() => {
                this.captchaLoading = false;
                this.countdown = -1;
                this.$message.error('验证码发送失败');
              })
          }
        });
      },
    },
  }
</script>