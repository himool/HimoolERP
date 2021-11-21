<template>
  <div style="height: 100vh;">
    <div class="logo" @click="$router.push('/')" style="width: 256px">
      <img :src="logo" width="36" style="margin-top: -6px; margin-left: 8px;" />
      <span v-if="!collapsed" style="color: #1890ff; margin-left: 6px;">海鸥云</span>
      <span v-if="!collapsed" style="color: #1890ff; margin-left: 6px; font-size: 14px;">进销存</span>
    </div>
    <a-menu theme="light" mode="inline" :selectedKeys="selectedKeys" :openKeys="openKeys" :inline-collapsed="collapsed"
      :style="{width: collapsed ? '80px' : '256px'}" @click="switchView" @openChange="openChange">
      <a-menu-item key="/home">
        <a-icon type="home" /><span>首页</span>
      </a-menu-item>

      <a-sub-menu v-for="menu in menus" :key="menu.key">
        <span slot="title">
          <a-icon :type="menu.icon" /><span>{{menu.name}}</span></span>
        <a-menu-item v-for="submenu of menu.submenus" :key="submenu.key">{{submenu.name}}</a-menu-item>
      </a-sub-menu>
    </a-menu>
  </div>
</template>

<script>
  import menus from './menus.js'

  export default {
    name: 'Sidebar',
    props: ['collapsed'],
    data() {
      return {
        menus,
        openKeys: [],
        selectedKeys: [],
        logo: require('@/assets/logo.png'),
      };
    },
    methods: {
      initialize() {
        this.changeRoute(this.$route.path);
      },
      switchView(item) {
        if (this.$route.path !== item.key) {
          this.$router.push(item.key);
        }
      },
      openChange(openKeys) {
        this.openKeys = [openKeys[openKeys.length - 1]];
      },
      changeRoute(path) {
        this.selectedKeys = [path];
        for (let m of menus) {
          if (m.submenus.findIndex(item => item.key == path) != -1) {
            this.openKeys = [m.key];
            return
          }
        }
      },
    },
    watch: {
      $route(to) {
        this.changeRoute(to.path);
      },
    },
    created() {
      this.initialize();
    },
  }
</script>

<style scoped>
  .logo {
    font-weight: bold;
    font-size: 20px;
    height: 64px;
    padding: 16px;
    border-bottom: 1px solid #6662;
    cursor: pointer;
  }
</style>