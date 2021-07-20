<template>
  <div>
    <a-modal v-model="visible" :okText="保存" :maskClosable="false" @ok="update" @cancel="cancel">
      <div slot="title">编辑子账号: {{form.username}}</div>
      <a-form-model ref="updateForm" :model="updateForm" :rules="rules" :label-col="{ span: 4 }"
        :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="phone" label="电话">
          <a-input size="large" v-model="updateForm.phone" />
        </a-form-model-item>
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="updateForm.username" />
        </a-form-model-item>
        <a-form-model-item prop="roles" label="角色">
          <a-checkbox-group v-model="updateForm.roles">
            <a-checkbox v-for="item of roleItems" :key="item.id" :value="item.id">{{item.name}}</a-checkbox>
          </a-checkbox-group>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { subuserUpdate } from '@/api/account'

  export default {
    name: 'UpdateModal',
    props: ['visible', 'roleItems', 'form'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        updateForm: {},
        rules: {
          phone: [
            { required: true, message: '请输入电话', trigger: 'change' },
            { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' },
          ],
          username: [{ required: true, message: '请输入用户名', trigger: 'change' }],
        },
      };
    },
    methods: {
      update() {
        this.$refs.updateForm.validate(valid => {
          if (valid) {
            subuserUpdate(this.updateForm)
              .then(resp => {
                this.$message.success('修改成功');
                this.$emit('update', resp.data);
                this.cancel();
              })
              .catch(err => {
                console.log(err.toString());
                
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.$refs.updateForm.resetFields();
      }
    },
    watch: {
      visible(value) {
        if (value) {
          console.log(this.form)
          this.updateForm = {
            id: this.form.id,
            name: this.form.name,
            phone: this.form.phone,
            username: this.form.username,
            roles: this.form.roles,
          }
        }
      }
    },
  }
</script>