<template>
  <a-select v-model.number="value" :disabled="disabled">
    <a-select-option
      v-for="(client) in clientList"
      :key="client.id"
      :value="client.id"
    >
      {{ client.name }}
    </a-select-option>
  </a-select>
</template>

<script>
import { clientList } from "@/api/sales";
export default {
  props: ["value","disabled"],
  watch:{
      value(newV,oldV){
          this.$emit('change',newV,oldV);
      },
  },
  data() {
    var that = this;
    clientList().then((resp) => {
      that.clientList = resp.data.results;
    });
    return {
      clientList: [],
    };
  },
};
</script>

<style>
</style>