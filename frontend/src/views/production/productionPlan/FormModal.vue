<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "编辑生产计划" : "新增生产计划" }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="类型">
            <a-select style="width: 100%">
              <a-select-option value="jack">
                按库存生产
              </a-select-option>
              <a-select-option value="lucy">
                按订单生产
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
// import { clientCreate, clientUpdate } from "@/api/basicData";

export default {
  name: "FormModal",
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules: {
        name: [{ required: true, message: "请输入名称", trigger: "change" }],
        number: [{ required: true, message: "请输入编号", trigger: "change" }],
        initial_arrears_amount: [
          { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: "初期欠款金额格式不正确", trigger: "change" },
        ],
      },
      loading: false,
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          let func = this.form.id ? clientUpdate : clientCreate;
          func(this.form)
            .then((data) => {
              this.$message.success(this.form.id ? "修改成功" : "新增成功");
              this.$emit(this.form.id ? "update" : "create", data);
              this.cancel();
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    cancel() {
      this.$emit("cancel", false);
      this.$refs.form.resetFields();
    },
  },
};
</script>

<style scoped></style>
