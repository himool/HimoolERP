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

        <div style="margin-bottom: 12px; float: right">
          <a-button type="primary" icon="plus" style="margin: 0 8px" @click="openCreateModal">新增生产计划</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px">
        <a-table
          rowKey="id"
          :columns="columns"
          :data-source="items"
          :pagination="pagination"
          :loading="loading"
          :scroll="{ x: 1600 }"
        >
          <div slot="action" slot-scope="value, item, index">
            <a-button-group size="small">
              <a-button>编辑</a-button>
              <a-button>详情</a-button>
              <a-popconfirm title="确定发布吗?">
                <a-button type="primary">发布工单</a-button>
              </a-popconfirm>
              <a-popconfirm title="确定删除吗?">
                <a-button type="danger">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>

    <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
  </div>
</template>

<script>
export default {
  components: {
    FormModal: () => import("./FormModal.vue"),
  },
  data() {
    return {
      searchForm: { search: "", page: 1, ordering: undefined },
      pagination: { current: 1, total: 0, pageSize: 16 },
      loading: false,
      items: [
        {
          id: 1,
          number: "p3423412312312",
          sales_order_number: "SO2322343242342",
          status: "进行中",
          goods_number: "G10000000001",
          goods_name: "手机",
          planned_quantity: 12,
          completed_quantity: 6,
          start_time: "2020-02-02 00:00:00",
          end_time: "2022-02-02 00:00:00",
        },
      ],
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          width: 60,
          fixed: "left",
          customRender: (value, item, index) => {
            return index + 1;
          },
        },
        {
          title: "生产计划单号",
          dataIndex: "number",
          fixed: "left",
        },
        {
          title: "销售单号",
          dataIndex: "sales_order_number",
        },
        {
          title: "状态",
          dataIndex: "status",
          width: 100,
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
          width: 100,
        },
        {
          title: "完成数量",
          dataIndex: "completed_quantity",
          width: 100,
        },
        {
          title: "计划开始时间",
          dataIndex: "start_time",
          width: 180,
        },
        {
          title: "计划结束时间",
          dataIndex: "end_time",
          width: 180,
        },
        {
          title: "操作",
          dataIndex: "action",
          fixed: "right",
          width: 256,
          scopedSlots: { customRender: "action" },
        },
      ],
      visible: false,
      targetItem: {},
      sss: false,
    };
  },
  methods: {
    search() {},
    openCreateModal() {
      this.targetItem = {};
      this.visible = true;
    },
    create() {},
    update() {},
    onChangePicker() {},
  },
};
</script>

<style scoped></style>
