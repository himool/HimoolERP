<template>
  <div>
    <a-row gutter="12">
      <a-col :span="16">
        <sales-trend />
        <sales-goods style="margin-top: 12px;"/>

      </a-col>
      <a-col :span="8">
        <sales-task />
        <warehouse-task style="margin-top: 12px;"/>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    components: {
      SalesTask: () => import('./SalesTask.vue'),
      SalesTrend: () => import('./SalesTrend.vue'),
      WarehouseTask: () => import('./WarehouseTask.vue'),
      SalesGoods: () => import('./SalesGoods.vue'),
    },
  }
</script>
