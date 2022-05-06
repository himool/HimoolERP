<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "编辑角色" : "新增角色" }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="名称">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="备注">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>

          <a-checkbox-group v-model="form.permissions">
            <a-descriptions size="small" title="权限" bordered>
              <a-descriptions-item
                v-for="permissionTypeItem in $parent.permissionItems"
                :key="permissionTypeItem.id"
                :span="3"
              >
                <div slot="label" style="width: 90px">
                  <a-checkbox :value="permissionTypeItem.name" @change="checkAll">{{
                    permissionTypeItem.name
                  }}</a-checkbox>
                </div>
                <a-row>
                  <a-col v-for="item in permissionTypeItem.permission_items" :key="item.id" :span="8">
                    <a-checkbox :value="item.id">{{ item.name }}</a-checkbox>
                  </a-col>
                </a-row>
              </a-descriptions-item>
            </a-descriptions>
          </a-checkbox-group>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { roleCreate, roleUpdate } from "@/api/system";
import rules from "./rules.js";

export default {
  name: "FormModal",
  props: ["visible", "form", "roleName"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules,
      loading: false,
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          let func = this.form.id ? roleUpdate : roleCreate;

          let permissions = [];
          for (let value of this.form.permissions) {
            if (typeof value == "number") {
              permissions.push(value);
            }
          }

          func({ ...this.form, permissions })
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
    checkAll(event) {
      for (let item of this.$parent.permissionItems) {
        if (item.name == event.target.value) {
          for (let permissionItem of item.permission_items) {
            let index = this.form.permissions.indexOf(permissionItem.id);

            if (event.target.checked && index == -1) {
              this.form.permissions.push(permissionItem.id);
            } else if (!event.target.checked && index != -1) {
              this.form.permissions.splice(index, 1);
            }
          }
          break;
        }
      }
    },
    onCheck(event) {
      if (event.target.checked) {
        this.form.permissions.push(event.target.value);
      }
    },
    cancel() {
      this.$emit("cancel", false);
      this.$refs.form.resetFields();
    },
  },
};
</script>

<style scoped></style>
