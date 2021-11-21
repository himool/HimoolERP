<template>
  <div>
    <a-modal
      v-model="visible"
      title="初始化库存"
      :maskClosable="false"
      @cancel="cancel"
      @ok="confirm"
    >
      <div style="margin-top: 12px">
        <a-table
          :columns="columns"
          :data-source="items"
          :loading="loading"
          size="small"
          :pagination="false"
        >
          <div slot="quantity" slot-scope="value, item">
            <a-input-number
              :value="item.quantity"
              min="0"
              @change="(value) => changeQuantity(value, item)"
            />
          </div>
        </a-table>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { warehouseList } from "@/api/warehouse";

export default {
  name: "InventoryModal",
  props: ["visible", "inventory"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      items: [],
      warehouseItems: [],
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
    };
  },
  methods: {
    list() {
      this.loading = true;
      warehouseList({ status: true })
        .then((resp) => {
          this.items = resp.data;
          for (let item of this.items) {
            item.quantity = this.inventory[item.id]
              ? this.inventory[item.id]
              : 0;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    changeQuantity(value, item) {
      item.quantity = value;
      this.items = [...this.items];
    },
    confirm() {
      this.$emit("confirm", this.items);
      this.cancel();
    },
    cancel() {
      this.$emit("cancel", false);
    },
  },
  watch: {
    visible(value) {
      if (value) {
        this.list();
      }
    },
  },
};
</script>

<style scoped>
</style>