<template>
  <div>
    <a-modal v-model="visible" :title="form.id ? '编辑商品' : '新增商品'" :maskClosable="false" :footer="null" width="756px"
      @cancel="$refs.form.clearValidate(); $emit('cancel', false);">
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4, md: 8 }"
        :wrapper-col="{ span: 20, md: 16 }">
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="name" label="商品名称">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="code" label="商品货号">
              <a-input v-model="form.code" :disabled="form.id" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="purchase_price" label="采购价">
              <a-input-number v-model="form.purchase_price" :precision="2" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="retail_price" label="零售价">
              <a-input-number v-model="form.retail_price" :precision="2" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="inventory_warning_upper_limit" label="库存预警上限">
              <a-input-number v-model="form.inventory_warning_upper_limit" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="suggested_retail_price" label="建议零售价">
              <a-input-number v-model="form.suggested_retail_price" :precision="2" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="inventory_warning_lower_limit" label="库存预警下限">
              <a-input-number v-model="form.inventory_warning_lower_limit" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="brand" label="品牌">
              <a-input v-model="form.brand" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="specification" label="规格型号">
              <a-input v-model="form.specification" />
            </a-form-model-item>
          </a-col>

          <a-col :span="24" :md="12">
            <a-form-model-item prop="category" label="分类">
              <a-select v-model="form.category" style="width: 75%;" :allowClear="true">
                <a-select-option v-for="item of categoryItems" :key="item.id" :value="item.id">{{item.name}}
                </a-select-option>
              </a-select>
              <a-button type="primary" style="width: 20%; margin-left: 5%;"
                @click="resetForm(); categoryVisible = true;">
                <a-icon type="plus" />
              </a-button>
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item prop="spec2" label="单位">
              <a-input v-model="form.unit" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="order" label="排序">
              <a-input-number v-model="form.order" :precision="0" style="width: 100%;" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-col :span="24" :md="12">
            <a-form-model-item label="初始库存数量">
              <a-button style="width: 100%;" :disabled="form.id" @click="inventoryVisible = true">
                {{form.initial_quantity > 0 ? form.initial_quantity : '设置'}}</a-button>
              <!-- <a-input-number v-model="form.initial_quantity" style="width: 100%;" :disabled="form.id" /> -->
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="status" label="状态">
              <a-select v-model="form.status">
                <a-select-option :value="true">启用</a-select-option>
                <a-select-option :value="false">停用</a-select-option>
              </a-select>
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
      <div style="text-align: center; margin: 8px 0;">
        <a-button type="primary" @click="form.id ? update() : create()" style="width: 30%;">{{form.id ? '保存' : '新增'}}
        </a-button>
      </div>
      <div v-if="!form.id" style="text-align: center; margin: 8px 0;">
        <a-checkbox v-model="isKeepAdd">持续添加</a-checkbox>
      </div>
    </a-modal>

    <category-modal :form="categoryForm" :visible="categoryVisible" @create="createCategory"
      @cancel="categoryVisible = false" />
    <inventory-modal v-model="inventoryVisible" :inventory="form.inventory" @confirm="createInventory" />
  </div>
</template>

<script>
  import { goodsCreate, goodsUpdate } from '@/api/goods'
  import NP from 'number-precision'

  export default {
    name: 'GoodsModal',
    components: {
      CategoryModal: () => import('@/components/CategoryModal/CategoryModal'),
      InventoryModal: () => import('./InventoryModal.vue')
    },
    props: ['form', 'visible', 'categoryItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        isKeepAdd: false,
        categoryForm: {},
        categoryVisible: false,
        inventoryVisible: false,
        rules: {
          name: [{ required: true, message: '请输入商品名称', trigger: 'change' }],
          code: [{ required: true, message: '请输入商品货号', trigger: 'change' }],
          purchase_price: [{ required: true, message: '请输入采购价', trigger: 'change' }],
          retail_price: [{ required: true, message: '请输入零售价', trigger: 'change' }],
        },
      };
    },
    methods: {
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            goodsCreate(this.form)
              .then(resp => {
                this.$emit('create', resp.data, this.isKeepAdd);
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
            goodsUpdate(this.form)
              .then(resp => {
                this.$emit('update', resp.data);
                this.$message.success('修改成功');
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              });
          }
        });
      },
      createInventory(items) {
        let initial_quantity = 0;
        for (let item of items) {
          initial_quantity  = NP.plus(initial_quantity, item.quantity);
          this.form.inventory[item.id] = item.quantity;
        }
        this.form.initial_quantity = initial_quantity;
      },
      createCategory(categoryItem) {
        this.categoryItems.push(categoryItem);
        this.form.category = categoryItem.id;
        this.categoryVisible = false;
      },
      resetForm() {
        this.categoryForm = { name: '', description: '', order: 100 };
      },
      cancel() {
        this.$emit('cancel');
        this.$refs.form.clearValidate();
      },
    },
  }
</script>