<template>
  <a-select   v-model.number="value" :disabled="disabled">
    <a-select-option
      v-for="warehouse in warehouseList"
      :key="warehouse.id"
      :value="warehouse.id"
    >
      {{ warehouse.name }}
    </a-select-option>
  </a-select>
</template>

<script>
import { warehouseList } from "@/api/warehouse";
export default {
  props: ["value", "disabled"],
  watch: {
    value(newV, oldV) {
      this.$emit("change", newV, oldV);
    },
  },
  data() {
    var that = this;
    warehouseList().then((resp) => {
        that.value = resp.data[0].id;
      that.warehouseList = resp.data    ;
    });
    return {
      warehouseList: [],
    };
  },
};
</script>

<style>
</style>