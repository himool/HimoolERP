<template>
  <div>
    <a-card title="配置管理">
      <a-spin :spinning="loading">
        <a-descriptions bordered>
          <a-descriptions-item label="激活入库" :span="3">
            <a-switch v-model="form.auto_stock_in" @change="update" />
          </a-descriptions-item>
          <a-descriptions-item label="激活出库" :span="3">
            <a-switch v-model="form.auto_stock_out" @change="update" />
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </a-card>
  </div>
</template>

<script>
  import { configRetrieve, configUpdate } from '@/api/user';

  export default {
    data() {
      return {
        loading: false,
        form: {},
      };
    },
    methods: {
      initData() {
        this.retrieve();
      },
      retrieve() {
        this.loading = true;
        configRetrieve().then(resp => {
          this.form = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        }).finally(() => {
          this.loading = false;
        });
      },
      update() {
        this.loading = true;
        configUpdate(this.form).then(resp => {
          this.form = resp.data;
          console.log(this.form);
          this.$message.success('保存成功');
        }).catch(err => {
          this.$message.error(err.response.data.message);
        }).finally(() => {
          this.loading = false;
        });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>

<style scoped>
</style>