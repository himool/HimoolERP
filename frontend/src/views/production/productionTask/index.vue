<template>
  <div>
    <a-card title="生产计划">
      <a-row :gutter="[12, 8]">
        <a-col :span="24" style="width: 256px;">
          <a-range-picker @change="onChangePicker" />
        </a-col>
        <a-col :span="24" style="width: 200px;">
          <a-input v-model="searchForm.search" placeholder="生产单号, 销售单号" allowClear @pressEnter="search" />
        </a-col>
        <a-col :span="24" style="width: 84px;">
          <a-button type="primary" icon="search" @click="search">查询</a-button>
        </a-col>
      </a-row>

      <a-row style="margin-top: 12px">
        <a-table rowKey="id" :columns="columns" :data-source="items" :pagination="pagination" :loading="loading">
          <div slot="action" slot-scope="value, item, index">
            <a-button-group size="small">
              <a-button>详情</a-button>
              <a-button>生产</a-button>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchForm: { search: "", page: 1, ordering: undefined },
      pagination: { current: 1, total: 0, pageSize: 16 },
      loading: false,
      items: [],
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          width: 60,
          customRender: (value, item, index) => {
            return index + 1;
          },
        },
        {
          title: "生产计划单号",
          dataIndex: "number",
        },
        {
          title: "销售单号",
          dataIndex: "sales_order_number",
        },
        {
          title: "产品编号",
          dataIndex: "goods_number",
        },
        {
          title: "产品名称",
          dataIndex: "goods_name",
        },
        {
          title: "计划数量",
          dataIndex: "planned_quantity",
        },
        {
          title: "完成数量",
          dataIndex: "completed_quantity",
        },
        {
          title: "计划开始时间",
          dataIndex: "start_time",
        },
        {
          title: "计划结束时间",
          dataIndex: "end_time",
        },
        {
          title: "操作",
          dataIndex: "action",
          scopedSlots: { customRender: "action" },
        },
      ],
      visible: false,
      targetItem: {},
    };
  },
  methods: {},
};
</script>

<style scoped></style>
