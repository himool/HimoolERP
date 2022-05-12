<template>
  <div id="app">
    <a-config-provider v-if="!loading" :locale="locales.zh_CN">
      <router-view />
    </a-config-provider>
  </div>
</template>

<script>
import { getCSRFToken } from "@/api/manage";
import Cookies from "js-cookie";

export default {
  name: "App",
  data() {
    return {
      locales: window.antd.locales,
      loading: true,
    };
  },
  methods: {
    initData() {
      getCSRFToken().then((data) => {
        this.loading = false;
        Cookies.set()
      });
    },
  },
  mounted() {
    this.initData();
  },
};
</script>

<style>
html {
  height: 100%;
}

body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
}
.panel .ant-table {
  min-height: 220px !important;
}
</style>
