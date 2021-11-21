<template>
  <a-select v-model.number="value" :disabled="disabled">
    <a-select-option
      v-for="(supplier) in supplierList"
      :key="supplier.id"
      :value="supplier.id"
    >
      {{ supplier.name }}
    </a-select-option>
  </a-select>
</template>

<script>
import { supplierList } from "@/api/purchase";
export default {
  props: ["value","disabled"],
  watch:{
      value(newV,oldV){
          this.$emit('change',newV,oldV);
      },
  },
  data() {
    var that = this;
    supplierList().then((resp) => {
      that.supplierList = resp.data;
    });
    return {
      supplierList: [],
    };
  },
};
</script>

<style>
</style>