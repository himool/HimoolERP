<template>
  <a-select   v-model.number="value" :disabled="disabled">
    <a-select-option
      v-for="user in userList"
      :key="user.id"
      :value="user.id"
    >
      {{ user.name }}
    </a-select-option>
  </a-select>
</template>

<script>
import { userList,getSubuserById } from '@/api/account'
export default {
  props: ["value", "disabled"],
  watch: {
    value(newV, oldV) {
      var that = this;
      this.$emit("change", newV, oldV);
      getSubuserById({
          id:newV
      }).then((res)=>{
      that.$emit("detailInfo",res.data);
      });
    },
  },
  data() {
    var that = this;
    userList().then((resp) => {
        that.value = resp.data[0].id;
      that.userList = resp.data    ;
    });
    return {
      userList: [],
    };
  },
};
</script>

<style>
</style>