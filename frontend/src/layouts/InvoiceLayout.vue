<template>
  <div>
    <router-view />
    <div style="text-align: center;">
      <a-button type="primary" @click="htmlToPDF('invoice', 'Order')">下载单据</a-button>
    </div>
  </div>
</template>

<script>
  import { htmlToPDF } from '@/utils/htmlToPDF'

  export default {
    name: 'InvoiceLayout',
    data() {
      return {
        htmlToPDF,
      };
    },
    methods: {
    },
  }
</script>

<style scoped>
</style>