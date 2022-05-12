<template>
  <div>
    <a-card title="账户管理">
      <a-row gutter="16">
        <a-col :span="24" style="max-width: 200px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="公司编号" allowClear @pressEnter="search" />
        </a-col>
        <a-col :span="24" style="width: 100px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="search">查询</a-button>
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">新增账户</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table
          size="small"
          :columns="columns"
          :dataSource="items"
          rowKey="id"
          :loading="loading"
          :pagination="pagination"
          @change="tableChange"
        >
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{ value ? "激活" : "冻结" }}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="openFormModal(item)">编辑</a-button>
              <a-popconfirm title="确定删除吗" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
    <form-modal
      v-model="visible"
      :form="targetItem"
      :clientsClassificationOptions="clientsClassificationItems"
      @create="create"
      @update="update"
    />
    <a-modal v-model="importLoading" :footer="null" :maskClosable="false" :closable="false">
      <div><a-spin style="margin-right: 12px;" />正在导入中, 请等待...</div>
    </a-modal>
  </div>
</template>

<script>
import { teamList, teamDestroy } from "@/api/manage";

export default {
  name: "Warehouse",
  components: {
    FormModal: () => import("./FormModal.vue"),
  },
  data() {
    return {
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          width: 60,
          customRender: (value, item, index) => {
            return index + 1;
          },
        },
        {
          title: "公司编号",
          dataIndex: "number",
        },
        {
          title: "到期时间",
          dataIndex: "expiry_time",
        },
        {
          title: "用户数量",
          dataIndex: "user_quantity",
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
        },
        {
          title: "操作",
          dataIndex: "action",
          scopedSlots: { customRender: "action" },
          width: "156px",
        },
      ],
      searchForm: { search: "", page: 1, page_size: 15 },
      pagination: { current: 1, total: 0, pageSize: 15 },
      loading: false,
      items: [],
      visible: false,
      targetItem: {},
    };
  },
  computed: {},
  methods: {
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      teamList(this.searchForm)
        .then((data) => {
          this.pagination.total = data.count;
          this.items = data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    create(item) {
      this.items.splice(0, 0, item);
    },
    update(item) {
      let index = this.items.findIndex((_item) => _item.id == item.id);
      if (index !== -1) {
        this.items.splice(index, 1, item);
      }
    },
    search() {
      this.searchForm.page = 1;
      this.pagination.current = 1;
      this.list();
    },
    openFormModal(item) {
      if (!item.id) {
        getClientNumber().then((data) => {
          this.targetItem = { ...item, ...{ number: data.number } };
        });
      } else {
        this.targetItem = { ...item };
      }

      this.visible = true;
    },
    destroy(id) {
      teamDestroy({ id }).then(() => {
        let index = this.items.findIndex((item) => item.id == id);
        if (index !== -1) {
          this.items.splice(index, 1);
        }

        this.$message.success("删除成功");
      });
    },
    exportExcel() {
      clientExport(this.searchForm)
        .then((resp) => {
          exportExcel(resp.data, "客户列表");
        })
        .catch((err) => {
          this.$message.error(err.response.data.error);
        });
    },
    downloadTemplate() {
      clientTemplate()
        .then((resp) => {
          exportExcel(resp.data, "客户导入模板");
        })
        .catch((err) => {
          this.$message.error(err.response.data.error);
        });
    },
    importExcel(item) {
      let data = new FormData();
      data.append("file", item.file);
      this.importLoading = true;
      setTimeout(() => {
        clientImport(data)
          .then(() => {
            this.$message.success("导入成功");
            this.list();
          })
          .catch((err) => {
            this.$message.error(err.response.data.detail);
          })
          .finally(() => {
            this.importLoading = false;
          });
      }, 1000);
    },
    tableChange(pagination, filters, sorter) {
      this.searchForm.page = pagination.current;
      this.pagination.current = pagination.current;
      this.searchForm.ordering = `${sorter.order == "descend" ? "-" : ""}${sorter.field}`;
      this.list();
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>
