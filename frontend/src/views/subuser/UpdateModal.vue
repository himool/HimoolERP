<template>
  <div>
    <a-modal
      v-model="visible"
      :okText="保存"
      :maskClosable="false"
      @ok="update"
      @cancel="cancel"
    >
      <div slot="title">编辑账号: {{ form.username }}</div>
      <a-form-model
        ref="updateForm"
        :model="updateForm"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="updateForm.username" />
        </a-form-model-item>
        <a-form-model-item prop="name" label="员工姓名">
          <a-input size="large" v-model="updateForm.name" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="updateForm.password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="确认密码">
          <a-input-password size="large" v-model="updateForm.confirm" />
        </a-form-model-item>
        <a-form-model-item prop="phone" label="手机号">
          <a-input size="large" v-model="updateForm.phone" />
        </a-form-model-item>
        <a-form-model-item prop="email" label="邮箱">
          <a-input size="large" v-model="updateForm.email" />
        </a-form-model-item>
        <a-form-model-item prop="sex" label="性别">
          <a-select style="width: 100%" v-model="updateForm.sex">
            <a-select-option value="man"> 男 </a-select-option>
            <a-select-option value="woman"> 女 </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item prop="roles" label="权限">
          <a-checkbox-group v-model="updateForm.roles">
            <a-checkbox
              v-for="item of roleItems"
              :key="item.id"
              :value="item.id"
              >{{ item.name }}</a-checkbox
            >
          </a-checkbox-group>
        </a-form-model-item>
        <a-form-model-item prop="status" label="状态">
          <a-switch
            checked-children="启用"
            un-checked-children="禁用"
            v-model="updateForm.status"
          />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
import { subuserUpdate, getSubuserById } from "@/api/account";

export default {
  name: "UpdateModal",
  props: ["visible", "roleItems", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      updateForm: {},
      rules: {
        phone: [
          { required: true, message: "请输入电话", trigger: "change" },
          {
            pattern: /^1[3456789]\d{9}$/,
            message: "手机号格式错误",
            trigger: "blur",
          },
        ],
        username: [
          { required: true, message: "请输入用户名", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    update() {
      this.$refs.updateForm.validate((valid) => {
        if (valid) {
          subuserUpdate(this.updateForm).then((resp) => {
            this.$message.success("修改成功");
            this.$emit("update", resp.data);
            this.cancel();
          });
        }
      });
    },
    cancel() {
      this.$emit("cancel", false);
      this.$refs.updateForm.resetFields();
    },
  },
  watch: {
    visible(value) {
      if (value) {
        var that = this;
        getSubuserById({
          id: this.form.id,
        }).then((resp) => {
          this.updateForm = resp.data;
        });
      }
    },
  },
};
</script>