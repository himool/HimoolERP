<template>
  <div>
    <a-layout>
      <a-layout-sider class="sidebar" width="256" v-model="collapsed" :trigger="null" collapsible>
        <sidebar :collapsed="collapsed" />
      </a-layout-sider>

      <a-layout v-if="isLogin">
        <a-layout-header class="headbar">
          <headbar :collapsed="collapsed" :username="username" @toggleCollapsed="toggleCollapsed" />
        </a-layout-header>

        <a-layout-content>
          <router-view v-if="isRouterAlive" style="padding: 8px;" />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import { superUserInfo } from "@/api/manage";

export default {
  name: "BaseLayout",
  components: {
    Headbar: () => import("@/components/Headbar/Headbar"),
    Sidebar: () => import("@/components/Sidebar/Sidebar"),
  },
  provide() {
    return {
      reloadPage: () => {
        return this.reloadPage();
      },
    };
  },
  data() {
    return {
      isLogin: false,
      collapsed: false,
      isRouterAlive: true,
      username: "222",
    };
  },
  methods: {
    initialize() {
      superUserInfo().then((response) => {
        this.isLogin = true;
        this.username = response.data.username;
      });
    },
    toggleCollapsed() {
      this.collapsed = !this.collapsed;
    },
    reloadPage() {
      this.isRouterAlive = false;
      this.$nextTick(() => (this.isRouterAlive = true));
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped>
.headbar {
  background: #fff;
  padding: 0;
  box-shadow: 0px 1px 10px #7774;
}

.sidebar {
  background: #fff;
  overflow: auto;
  box-shadow: 1px 0px 10px #7774;
}
</style>
