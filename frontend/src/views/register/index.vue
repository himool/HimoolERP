<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="phone" label="手机号">
          <a-input size="large" v-model="form.phone" />
        </a-form-model-item>
        <a-form-model-item prop="code" label="验证码">
          <a-space>
            <a-input size="large" v-model="form.code" />
            <a-button type="primary" size="large" @click="sendCode">{{ countDown > 0 ? `${countDown} s` : "发送" }}</a-button>
          </a-space>
        </a-form-model-item>
        <a-form-model-item prop="register_city" label="所在城市">
          <a-cascader size="large" v-model="form.cityCode" placeholder="" :options="provinceAndCityData" @change="changeCity" />
        </a-form-model-item>
        <a-form-model-item prop="number" label="公司编号">
          <a-input size="large" v-model="form.number" placeholder="公司英文名或拼音缩写" @pressEnter="register" />
        </a-form-model-item>
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" @pressEnter="register" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password" @pressEnter="register" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row :gutter="[4, 4]">
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%" @click="register"> 注册 </a-button>
      </a-col>
      <a-col :span="14" offset="5" style="text-align: right">
        <a @click="$router.push('/user/login')">返回登录</a>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { makeCode, registerAccount } from "@/api/user";
import { provinceAndCityData } from "element-china-area-data";

export default {
  data() {
    return {
      register_city_code: [],
      isLoading: false,
      form: {
        cityCode: undefined,
        register_city: "",
        phone: "",
        code: "",
        number: "",
        username: "",
        password: "",
      },
      rules: {
        register_city: [{ required: true, message: "请选择城市", trigger: "change" }],
        phone: [{ required: true, message: "请输入手机号", trigger: "change" }],
        code: [{ required: true, message: "请输入验证码", trigger: "change" }],
        number: [
          { required: true, message: "请输入公司", trigger: "change" },
          { max: 32, message: "超出最大长度 (32)", trigger: "change" },
        ],
        username: [
          { required: true, message: "请输入用户名", trigger: "change" },
          { max: 32, message: "超出最大长度 (32)", trigger: "change" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "change" }],
      },
      countDown: -1,
      provinceAndCityData,
    };
  },
  methods: {
    changeCity(code, selectedOptions) {
      this.register_city_code = code;
      this.form.register_city = selectedOptions.map((item) => item.label).join(" ");
    },
    register() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.isLoading = true;
          registerAccount({ ...this.form, register_city_code: this.register_city_code })
            .then((data) => {
              this.$message.success("注册成功");
              this.$router.push("/user/login");
            })
            .finally(() => {
              this.isLoading = false;
            });
        }
      });
    },
    sendCode() {
      if (/^1[3-9]\d{9}$/.test(this.form.phone)) {
        makeCode({ phone: this.form.phone }).then(() => {
          this.$message.success("验证码发送成功");
          this.startCountDown();
        });
      } else {
        this.$message.warning("手机号错误");
      }
    },
    startCountDown() {
      if (this.countDown < 0) {
        this.countDown = 60;
      } else if (this.countDown == 0) {
        this.countDown = -1;
        return;
      } else {
        this.countDown--;
      }

      setTimeout(() => {
        this.startCountDown();
      }, 1000);
    },
  },
};
</script>
