<template>
  <div>
    <a-layout>
      <a-layout-sider class="sidebar" width="256" v-model="collapsed" :trigger="null" collapsible>
        <sidebar :collapsed="collapsed" />
      </a-layout-sider>

      <a-layout>
        <a-layout-header class="headbar">
          <headbar :collapsed="collapsed" :username="username" @toggleCollapsed="toggleCollapsed" />
        </a-layout-header>

        <a-layout-content>
          <router-view style="padding: 8px;" />
        </a-layout-content>

        <!-- <a-layout-footer style=" padding: 8px;">
          <div style="color: #777; text-align: center;">
            版权所有 © 2020 盒木科技 <a href="http://beian.miit.gov.cn" target="_blank">苏ICP备20014894号</a>
          </div>
        </a-layout-footer> -->

      </a-layout>
    </a-layout>
  </div>
</template>

<script>
  import { getInfo } from '@/api/user'
  // import moment from 'moment'

  export default {
    name: 'ConsoleLayout',
    components: {
      Headbar: () => import('@/components/Headbar/Headbar'),
      Sidebar: () => import('@/components/Sidebar/Sidebar'),
    },
    data() {
      return {
        collapsed: false,
        username: '',
      };
    },
    methods: {
      initialize() {
        getInfo()
          .then(resp => {
            this.username = resp.data.username;
            if (resp.data.end_datetime) {
              // let remainDays = moment(resp.data.end_datetime).diff(moment(), 'days');
              // if (remainDays <= 7) {
              //   this.accountWarning(remainDays);
              // }
              if (resp.data.inventory_warning_count > 0) {
                this.inventoryWarning(resp.data.inventory_warning_count);
              }
            }
          })
          .catch(err => {
            if (err.response.status === 403) {
              
                this.$message.error('请先登录');
              this.$router.push('/user/login');
            } else {
              
                this.$message.error(err.response.data.message);
            }
          });
      },
      toggleCollapsed() {
        this.collapsed = !this.collapsed;
      },
      accountWarning(value) {
        this.$notification.warning({
          message: '账号到期提醒',
          description: `您的账号还有 ${value} 天过期, 如需继续使用请立即购买`,
          btn: h => {
            return h(
              'a-button',
              {
                props: { type: 'primary', size: 'small', },
                // on: {
                //   click: () => this.$notification.close(key),
                // },
              },
              '立即购买',
            );
          },
        });
      },
      inventoryWarning(value) {
        this.$notification.warning({
          message: '库存警告',
          description: `您有 ${value} 个商品库存低于库存下限, 请及时补货`,
          btn: h => {
            return h(
              'a-button',
              {
                props: { type: 'primary', size: 'small', },
                on: { click: () => this.$router.push({ path: '/inventory', query: { is_show_warning: true } }) },
              },
              '查看详情',
            );
          },
        });
      },
    },
    mounted() {
      this.initialize();
    },
  }
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