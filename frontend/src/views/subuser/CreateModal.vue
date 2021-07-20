<template>
  <div>
    <a-modal v-model="visible" title="创建子账号" okText="创建" :maskClosable="false" @ok="create" @cancel="cancel">
      <a-form-model ref="createForm" :model="createForm" :rules="rules" :label-col="{ span: 4 }"
        :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="phone" label="电话">
          <a-input size="large" v-model="createForm.phone" />
        </a-form-model-item>
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="createForm.username" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="createForm.password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="确认密码">
          <a-input-password size="large" v-model="createForm.confirm" />
        </a-form-model-item>
        <a-form-model-item prop="roles" label="角色">
          <a-checkbox-group v-model="createForm.roles">
            <a-checkbox v-for="item of roleItems" :key="item.id" :value="item.id">{{item.name}}</a-checkbox>
          </a-checkbox-group>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { subuserCreate } from '@/api/account'

  export default {
    name: 'CreateModal',
    props: ['visible', 'roleItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        createForm: { name: '', phone: '', username: '', password: '', confirm: '', roles: [] },
        rules: {
          phone: [
            { required: true, message: '请输入电话', trigger: 'change' },
            { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur' },
          ],
          username: [{ required: true, message: '请输入用户名', trigger: 'change' }],
          password: [{ required: true, message: '请输入密码', trigger: 'change' }],
          confirm: [
            { required: true, message: '请再次输入密码', trigger: 'change' },
            { validator: this.validateConfirm, trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      create() {
        this.$refs.createForm.validate(valid => {
          if (valid) {
            subuserCreate(this.createForm)
              .then(resp => {
                this.$message.success('新增成功');
                this.$emit('create', resp.data);
                this.cancel();
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
              })
          }
        });
      },
      validateConfirm(rule, value, callback) {
        return value === this.createForm.password ? callback() : callback(new Error('两次输入密码不一致'))
      },
      cancel() {
        this.$emit('cancel', false);
        this.resetForm();
        this.$refs.createForm.resetFields();
      },
      resetForm() {
        this.createForm = { name: '', phone: '', username: '', password: '', confirm: '', roles: [] };
      }
    },
  }
</script>