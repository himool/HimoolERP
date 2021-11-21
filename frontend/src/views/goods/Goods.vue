<template>
  <div>
    <div style="margin-top: 8px">
      <a-card title="商品信息">
        <a-row gutter="16">
          <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px">
            <a-input
              v-model="searchForm.search"
              placeholder="名称, 编号"
              allowClear
              @pressEnter="handleSearch"
            />
          </a-col>
          <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px">
            <a-select
              v-model="searchForm.category"
              placeholder="商品分类"
              style="width: 100%"
              allowClear
              @change="handleSearch"
            >
              <a-select-option
                v-for="item of categoryItems"
                :key="item.id"
                :value="item.id"
                >{{ item.name }}
              </a-select-option>
            </a-select>
          </a-col>
          <a-col
            :span="24"
            :md="8"
            :xl="12"
            style="
              margin-bottom: 12px;
              display: flex;
              justify-content: space-between;
            "
          >
            <a-button type="primary" icon="search" @click="handleSearch"
              >查询</a-button
            >
            <a-button
              type="primary"
              @click="
                resetForm();
                goodsVisible = true;
              "
            >
              <a-icon type="plus" />新增商品
            </a-button>
          </a-col>
        </a-row>

        <a-table
          :columns="columns"
          :data-source="goodsItems"
          size="small"
          :loading="loading"
          :pagination="false"
          @change="handleTableChange"
        >
          <div slot="status" slot-scope="value">
            <template v-if="value">
              <a-badge status="success" />
              <span>启用</span>
            </template>
            <template v-else>
              <a-badge status="error" />
              <span>禁用</span>
            </template>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button
                size="small"
                @click="
                  $router.push({
                    path: '/inventory',
                    query: { search: item.code },
                  })
                "
              >
                <a-icon type="appstore" />库存
              </a-button>
              <a-button
                size="small"
                @click="
                  $router.push({
                    path: '/flow',
                    query: { search: item.number },
                  })
                "
              >
                <a-icon type="profile" />流水
              </a-button>
              <a-button
                size="small"
                @click="
                  setGoodForm(item);
                  goodsVisible = true;
                "
              >
                <a-icon type="edit" />编辑
              </a-button>
              <a-popconfirm
                :title="`删除商品: ${item.name}`"
                ok-text="确认"
                cancel-text="取消"
                @confirm="destroy(item)"
              >
                <a-button type="danger" size="small">
                  <a-icon type="delete" />删除
                </a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
        <div style="text-align: center; margin-top: 24px">
          <a-pagination
            v-model="searchForm.page"
            :total="totalRows"
            :pageSize="perPage"
            show-less-items
            @change="list"
          />
        </div>
      </a-card>
    </div>

    <goods-modal
      v-model="goodsVisible"
      :form.sync="goodsForm"
      :categoryItems="categoryItems"
      @create="create"
      @update="update"
      @cancel="goodsVisible = false"
    />
  </div>
</template>

<script>
import {
  goodsList,
  goodsDestroy,
  categoryList,
  goodsRead,
  goodsReadByNumber,
} from "@/api/goods";
import NP from "number-precision";

export default {
  name: "Goods",
  components: {
    GoodsModal: () => import("@/components/GoodsModal/GoodsModal"),
  },
  data() {
    return {
      NP,
      searchForm: { page: 1 },
      goodsForm: {},
      goodsItems: [],
      categoryItems: [],
      loading: false,
      goodsVisible: false,
      setGoodsItem: {},
      totalRows: 0,
      perPage: 16,
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          scopedSlots: { customRender: "index" },
          customRender: (text, record, index) => `${index + 1}`,
        },
        {
          title: "名称",
          dataIndex: "name",
          key: "name",
          sorter: true,
        },
        {
          title: "编号",
          dataIndex: "number",
          key: "number",
          sorter: true,
        },
        {
          title: "分类",
          dataIndex: "category_name",
          key: "category_name",
        },
        {
          title: "规格",
          dataIndex: "spec",
          key: "spec",
        },
        {
          title: "单位(元)",
          dataIndex: "unit",
          key: "unit",
        },
        {
          title: "采购价(元)",
          dataIndex: "purchase_price",
          key: "purchase_price",
          sorter: true,
        },
        {
          title: "零售价(元)",
          dataIndex: "retail_price",
          key: "retail_price",
          sorter: true,
        },
        {
          title: "状态",
          dataIndex: "status",
          key: "status",
          scopedSlots: { customRender: "status" },
        },
        {
          title: "排序",
          dataIndex: "order",
          key: "order",
          sorter: true,
        },
        {
          title: "操作",
          dataIndex: "action",
          key: "action",
          scopedSlots: { customRender: "action" },
          width: "296px",
        },
      ],
    };
  },
  methods: {
    initalize() {
      this.resetForm();
      this.list();
      categoryList().then((resp) => {
        this.categoryItems = resp.data;
      });
    },
    setGoodForm(item) {
      goodsRead(item).then((resp) => {
        if (resp.data.image_items) {
          resp.data.image_items = resp.data.image_items.map((image_item) => {
            return {
              uid: image_item.id,
              name: image_item.name,
              status: "done",
              url: image_item.file,
            };
          });
        }
        this.goodsForm = resp.data;
      });
    },
    list() {
      this.loading = true;
      goodsList(this.searchForm)
        .then((resp) => {
          this.totalRows = resp.data.count;
          this.goodsItems = resp.data.results;
        })

        .finally(() => {
          this.loading = false;
        });
    },
    create(goodsItem, isKeepAdd) {
      this.goodsItems.push(goodsItem);
      if (isKeepAdd) {
        this.resetForm();
      } else {
        this.goodsVisible = false;
      }
    },
    update(goodsItem) {
      this.goodsItems.splice(
        this.goodsItems.findIndex((item) => item.id === goodsItem.id),
        1,
        goodsItem
      );
      this.goodsVisible = false;
    },
    destroy(goodsItem) {
      let form = { ...goodsItem };
      goodsDestroy(form).then(() => {
        this.$message.success("删除成功");
        this.goodsItems.splice(
          this.goodsItems.findIndex((item) => item.id === form.id),
          1
        );
      });
    },
    search() {
      this.searchForm.page = 1;
      this.list();
    },
    resetForm() {
      var that = this;
      goodsReadByNumber()
        .then((resp) => {
          that.goodsForm = {
            status: true,
            order: 100,
            image_items: [],
            number: resp.data.number,
            inventory_items: [],
          };
          that.$set(that.goodsForm, "image_items", []);
          that.$set(that.goodsForm, "inventory_items", []);
        })
        .finally(() => {});
    },
    handleSearch() {
      this.list();
    },
    handleTableChange(pagination, filters, sorter) {
      this.searchForm.ordering = `${sorter.order == "descend" ? "-" : ""}${
        sorter.field
      }`;
      this.list();
    },
  },
  mounted() {
    this.initalize();
  },
};
</script>
<style>
.ant-divider-horizontal.ant-divider-with-text-left:before {
  top: 50%;
  width: 0%;
}
.ant-divider-horizontal.ant-divider-with-text-left:after,
.ant-divider-horizontal.ant-divider-with-text-right:before {
  top: 0%;
  width: 95%;
}
</style>