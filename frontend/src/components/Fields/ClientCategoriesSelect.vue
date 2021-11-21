<template>
  <a-select v-model.number="value" :disabled="disabled">
    <a-select-option
      v-for="(client) in clientCategoriesOptions"
      :key="client.id"
      :value="client.id"
    >
      {{ client.name }}
    </a-select-option>
  </a-select>
</template>

<script>
import { clientCategoriesOptions } from "@/api/sales";
export default {
  props: ["value","disabled"],
  watch:{
      value(newV,oldV){
          this.$emit('change',newV,oldV);
      },
  },
  data() {
    var that = this;
    clientCategoriesOptions().then((resp) => {
      that.clientCategoriesOptions = resp.data.results;
    });
    return {
      clientCategoriesOptions: [],
    };
  },
};
</script>

<style>
</style>