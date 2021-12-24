<template>
  <div>
    <div style="float: right;">
      <a-dropdown :trigger="['click']">
        <span class="trigger">
          {{warehouse || '全部仓库'}}
          <a-icon type="down" />
        </span>
        <a-menu slot="overlay">
          <template v-for="(item,index) in items" >
            <a-menu-item :key="index" @click="itemClick(item)">
            <span>{{item.name}}</span>
          </a-menu-item>
          </template>
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import { warehouseOption } from '@/api/option';

  export default {
    name: 'WarehouseHeadbar',
    data() {
      return {
        items:[],
        warehouse:'',
      };
    },
    created(){
        warehouseOption(this.searchForm).then(data => {
          this.items = data.results;
        }).finally(() => {
        });
    },
    methods:{
      itemClick(item){
        this.setWarehouse(item);
      },
      setWarehouse(item){
        this.warehouse = item.name;
        window.localStorage.setItem('warehouse',item.id);
        this.$router.go(0);
      },
    }
  
  }
</script>

<style scoped>
  .trigger {
    font-size: 18px;
    line-height: 64px;
    padding: 0 24px;
    cursor: pointer;
    transition: color 0.3s;
  }

  .trigger:hover {
    color: #1890ff;
  }
</style>