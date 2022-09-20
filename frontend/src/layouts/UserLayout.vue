<template>
  <div class="background" ref="card">
    <a-card class="card">
      <div>
        <div style="text-align: center; padding-top: 16px">
          <img :src="logo" width="100" style="cursor: pointer; margin-top: 16px" @click="backIndex" />
        </div>
        <div class="title" style="margin-top: 16px">
          <span style="cursor: pointer; font-size: 24px" @click="backIndex">Himool ERP</span>
        </div>
        <div style="text-align: center; font-size: 16px; color: #1890ff; margin-top: 8px; margin-bottom: 24px">
          <span>盒木企业管理系统</span>
        </div>
      </div>
      <router-view />
    </a-card>
  </div>
</template>

<script>
export default {
  name: "UserLayout",
  data() {
    return {
      logo: require("@/assets/logo.png"),
    };
  },
  methods: {
    backIndex() {
      window.open("http://www.haioucloud.com", "_self");
    },
  },
};
</script>

<style scoped>
.card {
  width: 480px;
  border-radius: 8px;
  padding-bottom: 64px;
  margin: auto;
}

.background {
  min-height: 100%;
  padding: 10vh 0;
  background: #f0f2f5 url("~@/assets/background.svg") no-repeat 50%;
}

.title {
  text-align: center;
  font-size: 32px;
  color: #1890ff;
  margin-top: 8px;
  font-weight: bold;
}
</style>
