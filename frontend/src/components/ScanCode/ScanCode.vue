<template>
  <div>
    <a-form layout="inline" :form="form" @keyup.enter.native="list">
      <a-form-item>
        <a-input v-model="form.code_or_number" placeholder="请扫码添加商品" allowClear> </a-input>
      </a-form-item>
      <a-form-item>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { goodsList } from "@/api/goods";
export default {
  data() {
    return {
      loading: false,
      visible: false,
      form: {
        code_or_number: "",
      },
    };
  },
  mounted() {},
  methods: {
    list() {
      this.loading = true;
      var that = this;
      goodsList(this.form)
        .then((resp) => {
          if (Array.isArray(resp.data.results)) {
            if (resp.data.results.length==0) {
              that.$message.warn('无此商品，请先录入商品信息再扫码。');
            }
            that.$emit("list", resp.data.results);
          }
        })
        .finally(() => {
          that.loading = false;
          that.$set(that.form,'code_or_number','');
        });
    },
  },
};
</script>

<style>
</style>