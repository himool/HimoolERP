<template>
  <a-modal v-model="visible" :title="form.id ? '编辑分类' : '新增分类'" :maskClosable="false" :okText="form.id ? '保存' : '新增'"
    cancelText="取消" @ok="form.id ? update() : create()" @cancel="cancel">
    <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
      <a-form-model-item prop="name" label="分类名称">
        <a-input size="large" v-model="form.name" />
      </a-form-model-item>
      <a-form-model-item prop="description" label="分类描述">
        <a-input size="large" v-model="form.description" />
      </a-form-model-item>
      <a-form-model-item prop="order" label="排序">
        <a-input size="large" v-model="form.order" />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
  import { categoryCreate, categoryUpdate } from '@/api/goods'

  export default {
    name: 'CategoryModal',
    props: ['form', 'visible'],
    data() {
      return {
        rules: {
          name: [{ required: true, message: '请输入分类名称', trigger: 'change' }],
        },
      };
    },
    methods: {
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            categoryCreate(this.form)
              .then(resp => {
                this.$emit('create', resp.data)
                this.$message.success('新增成功');
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      update() {
        this.$refs.form.validate(valid => {
          if (valid) {
            categoryUpdate(this.form)
              .then(resp => {
                this.$emit('update', resp.data)
                this.$message.success('修改成功');
              })
              .catch(err => {
                
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      cancel() {
        this.$emit('cancel');
        this.$refs.form.clearValidate();
      },
    },
  }
</script>