<template>
  <div>
    <a-modal
      v-model="visible"
      :title="form.id ? '编辑商品' : '新增商品'"
      :maskClosable="false"
      :footer="null"
      width="756px"
      @cancel="
        $refs.form.clearValidate();
        $emit('cancel', false);
      "
    >
      <a-form-model
        ref="form"
        :model="form"
        :rules="rules"
        :label-col="{ span: 4, md: 8 }"
        :wrapper-col="{ span: 20, md: 16 }"
      >
        <a-row gutter="12">
          <a-divider orientation="left" id="basic-information">
            基本信息
          </a-divider>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="code" label="条形码">
              <a-input-search v-model="form.code">
                <a-button
                  slot="enterButton"
                  type="primary"
                  @click.native="getCode"
                >
                  生成条形码
                </a-button>
              </a-input-search>
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="number" label="商品编号">
              <a-input v-model="form.number" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="name" label="商品名称">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="category" label="分类">
              <a-select
                v-model.number="form.category"
                style="width: 75%"
                :allowClear="true"
              >
                <a-select-option
                  v-for="item of categoryItems"
                  :key="item.id"
                  :value="item.id"
                  >{{ item.name }}
                </a-select-option>
              </a-select>
              <a-button
                type="primary"
                style="width: 20%; margin-left: 5%"
                @click="
                  resetForm();
                  categoryVisible = true;
                "
              >
                <a-icon type="plus" />
              </a-button>
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="unit" label="单位">
              <a-input v-model="form.unit" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="spec" label="规格">
              <a-input v-model="form.spec" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="enable_shelf_life" label="启用保质期">
              <a-switch
                checked-children="开"
                un-checked-children="关"
                v-model="form.enable_shelf_life"
              />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12" v-if="!!form.enable_shelf_life">
            <a-form-model-item prop="shelf_life_days" label="保质期天数">
              <a-input v-model="form.shelf_life_days" suffix="天" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12" v-if="!!form.enable_shelf_life">
            <a-form-model-item
              prop="shelf_life_warning_days"
              label="保质期预警天数"
            >
              <a-input v-model="form.shelf_life_warning_days" suffix="天" />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="status" label="状态">
              <a-switch
                checked-children="启用"
                un-checked-children="禁用"
                v-model="form.status"
              />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="order" label="排序">
              <a-input-number
                v-model.number="form.order"
                :precision="0"
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="remark" label="备注">
              <a-input
                v-model.number="form.remark"
                :precision="0"
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-divider orientation="left" id="price-management">
            价格管理
          </a-divider>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="purchase_price" label="采购价（元）">
              <a-input-number
                v-model="form.purchase_price"
                
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item prop="retail_price" label="零售价（元）">
              <a-input-number
                v-model="form.retail_price"
                
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-divider orientation="left" id="graphic-information">
            图文信息
          </a-divider>
          <a-col :span="24" :md="24">
            <a-upload
              :action="uploadUrl"
              list-type="picture-card"
              :headers="{ 'X-CSRFToken': Cookies.get('csrftoken') }"
              :file-list="form.image_items"
              @preview="handlePreview"
              @change="handleChange"
              :before-upload="beforeUpload"
              name="file"
            >
              <div v-if="form.image_items && form.image_items.length < 8">
                <a-icon type="plus" />
                <div class="ant-upload-text"></div>
              </div>
            </a-upload>
            <a-modal
              :visible="previewVisible"
              :footer="null"
              @cancel="handleCancel"
            >
              <img alt="example" style="width: 100%" :src="previewImage" />
            </a-modal>
          </a-col>
          <a-col :span="24" :md="24">
            <a-textarea
              placeholder="商品详细介绍"
              :rows="4"
              v-model="form.description"
            />
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-divider orientation="left" id="beginning-inventory">
            期初库存
          </a-divider>
          <a-col :span="24" :md="24">
            <a-table
              :columns="columns"
              :data-source="inventory_items"
              :loading="loading"
              :pagination="false"
              style="width: 100%"
            >
              <div slot="quantity" slot-scope="value, item">
                <a-input-number
                  :disabled="!!form.id"
                  :readonly="!!form.id"
                  :value="item.quantity"
                  min="0"
                  @change="(value) => changeQuantity(value, item)"
                />
              </div>
            </a-table>
          </a-col>
        </a-row>
        <a-row gutter="12">
          <a-divider orientation="left" id="inventory-warning">
            库存预警
          </a-divider>
          <a-col :span="24" :md="12">
            <a-form-model-item
              prop="inventory_warning_upper_limit"
              label="库存预警上限"
            >
              <a-input-number
                v-model="form.inventory_warning_upper_limit"
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
          <a-col :span="24" :md="12">
            <a-form-model-item
              prop="inventory_warning_lower_limit"
              label="库存预警下限"
            >
              <a-input-number
                v-model="form.inventory_warning_lower_limit"
                style="width: 100%"
              />
            </a-form-model-item>
          </a-col>
        </a-row>
      </a-form-model>
      <div style="text-align: center; margin: 8px 0">
        <a-button
          type="primary"
          @click="form.id ? update() : create()"
          style="width: 30%"
          >{{ form.id ? "保存" : "新增" }}
        </a-button>
      </div>
      <div v-if="!form.id" style="text-align: center; margin: 8px 0">
        <a-checkbox v-model="isKeepAdd">持续添加</a-checkbox>
      </div>
    </a-modal>

    <category-modal
      :form="categoryForm"
      :visible="categoryVisible"
      @create="createCategory"
      @cancel="categoryVisible = false"
    />
  </div>
</template>

<script>
// api
import {
  goodsCreate,
  goodsUpdate,
  goodsReadByCode,
  goodsReadByNumber,
} from "@/api/goods";
import { warehouseList } from "@/api/warehouse";
import Cookies from 'js-cookie'
// import NP from "number-precision";
import config from "@/config/api";
var uploadUrl = config.baseUrl + config.uploadUrl;
uploadUrl = decodeURI(uploadUrl);
console.log("文件上传地址", uploadUrl);
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}
export default {
  name: "GoodsModal",
  components: {
    CategoryModal: () => import("@/components/CategoryModal/CategoryModal"),
  },
  props: ["form", "visible", "categoryItems"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      Cookies,
      uploadUrl,
      inventory_items: [],
      loading: false,
      columns: [
        {
          title: "仓库",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "数量",
          dataIndex: "quantity",
          key: "quantity",
          scopedSlots: { customRender: "quantity" },
        },
      ],
      isKeepAdd: false,
      categoryForm: {},
      categoryVisible: false,
      rules: {
        name: [
          { required: true, message: "请输入商品名称", trigger: "change" },
        ],
        number: [
          { required: true, message: "请输入商品编号", trigger: "change" },
        ],
        purchase_price: [
          { required: true, message: "请输入采购价", trigger: "change" },
        ],
        retail_price: [
          { required: true, message: "请输入零售价", trigger: "change" },
        ],
      },
      previewVisible: false,
      previewImage: "",
    };
  },
  methods: {
    beforeUpload(){
      
    },
    reset() {
      this.form = {};
      this.previewImage = "";
      this.previewVisible = false;
      this.isKeepAdd = false;
      this.inventory_items = this.inventory_items.map((inventory_item) => {
        if (inventory_item.quantity) {
          inventory_item.quantity = 0;
        }
        return inventory_item;
      });
    },
    getCode() {
      var that = this;
      goodsReadByCode({}).then((resp) => {
        that.$set(this.form, "code", resp.data.code);
      });
    },
    list() {
      this.loading = true;
      var that = this;
      warehouseList({ status: true })
        .then((resp) => {
          that.inventory_items = resp.data;
        })
        .finally(() => {
          that.loading = false;
        });
    },
    changeQuantity(value, item) {
      item.quantity = value || 0;
      this.inventory_items = [...this.inventory_items];
    },
    handleCancel() {
      this.previewVisible = false;
    },
    async handlePreview(file) {
      if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
      }
      this.previewImage = file.url || file.preview;
      this.previewVisible = true;
    },
    handleChange({ fileList }) {
      this.$set(this.form,'image_items',fileList);
    },
    create() {
      this.createInventory();
      var that = this;
      this.$refs.form.validate((valid) => {
        if (valid) {
          
          goodsCreate(that.form).then((resp) => {
            that.$emit("create", resp.data, that.isKeepAdd);
            that.$message.success("新增成功");
          });
        }
      });
    },
    update() {
      var that = this;
      this.createInventory();
      this.$refs.form.validate((valid) => {
        if (valid) {
          goodsUpdate(that.form).then((resp) => {
            that.$emit("update", resp.data);
            that.$message.success("修改成功");
          });
        }
      });
    },
    createInventory() {
      var inventory_items = this.inventory_items.map((item) => {
        return {
          warehouse: parseInt(item.id),
          quantity: parseInt(item.quantity || 0),
        };
      });
          
      this.$set(this.form, "inventory_items", inventory_items);
    },
    createCategory(categoryItem) {
      this.categoryItems.push(categoryItem);
      this.form.category = categoryItem.id;
      this.categoryVisible = false;
    },
    resetForm() {
      this.categoryForm = { name: "", description: "", order: 100 };
    },
    cancel() {
      this.$emit("cancel");
      this.$refs.form.clearValidate();
    },
  },
  watch: {
    'form.image_items': {
    handler(newVal) {
      if (Array.isArray(newVal)) {
        var images = newVal.map((file)=>{
          if (file.status) {
            if (file.status == 'done') {
              if (file.response && file.response.id) {
                return file.response.id;
              }
               if (file.uid) {
              return file.uid;
            }
            } 
          } 
        });
        this.$set(this.form,'images',images);
      }
    },
    deep: true
  },
    visible(oldV, newV) {
      if (!!oldV == true) {
        var that = this;
        goodsReadByNumber()
          .then((resp) => {
            that.$set(that.form, "number", resp.data.number);
          })
          .finally(() => {});
      } else {
        this.reset();
      }
    },
  },
  mounted() {
    this.list();
  },
};
</script>
<style scoped>
/* you can make up upload button and sample style by using stylesheets */
.ant-upload-select-picture-card i {
  font-size: 32px;
  color: #999;
}

.ant-upload-select-picture-card .ant-upload-text {
  margin-top: 8px;
  color: #666;
}
.ant-divider-horizontal.ant-divider-with-text-center,
.ant-divider-horizontal.ant-divider-with-text-left,
.ant-divider-horizontal.ant-divider-with-text-right {
  margin-top: 0px;
}
</style>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>