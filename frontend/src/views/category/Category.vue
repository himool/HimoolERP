<template>
  <div>
    <a-card title="分类管理">
      <div slot="extra" style="margin: -6px 0;">
        <a-button type="primary" @click="resetForm(); visible = true;">
          <a-icon type="plus" />新增分类
        </a-button>
      </div>

      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="名称" allowClear @pressEnter="handleSearch" />
        </a-col>
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="handleSearch">查询</a-button>
        </a-col>
      </a-row>

      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        @change="handleTableChange">
        <div slot="index" slot-scope="value, item, index">{{index + 1}}</div>
        <div slot="action" slot-scope="value, item">
          <a-button-group>
            <a-button size="small" @click="form = {...item}; visible = true;">
              <a-icon type="edit" />编辑
            </a-button>
            <a-popconfirm :title="`删除商品分类: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
              <a-button type="danger" size="small">
                <a-icon type="delete" />删除
              </a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </a-table>
    </a-card>

    <category-modal :form="form" :visible="visible" @create="create" @update="update" @cancel="visible = false" />
  </div>
</template>

<script>
  import { categoryList, categoryDestroy } from '@/api/goods'

  export default {
    name: 'Category',
    components: {
      CategoryModal: () => import('@/components/CategoryModal/CategoryModal'),
    },
    data() {
      return {
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: '64px',
            scopedSlots: { customRender: 'index' },
          },
          {
            title: '分类名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
          },
          {
            title: '分类描述',
            dataIndex: 'description',
            key: 'description',
            ellipsis: true,
          },
          {
            title: '商品数量',
            dataIndex: 'goods_count',
            key: 'goods_count',
            ellipsis: true,
          },
          {
            title: '排序',
            dataIndex: 'order',
            key: 'order',
            sorter: true,
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px',
          },
        ],
        items: [],
        form: { name: '', description: '', order: 100 },
        loading: false,
        visible: false,
        searchForm: {},
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        categoryList(this.searchForm).then(resp => {
          this.items = resp.data;
        }).catch(err => {
          this.$message.error(err.response.data.message);
        }).finally(() => {
          this.loading = false;
        });
      },
      create(categoryItem) {
        this.items.push(categoryItem);
        this.visible = false;
      },
      update(categoryItem) {
        this.items.splice(this.items.findIndex(item => item.id === categoryItem.id), 1, categoryItem);
        this.visible = false;
      },
      destroy(item) {
        let form = { ...item };
        categoryDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      resetForm() {
        this.form = { name: '', description: '', order: 100 };
      },
      handleSearch() {
        this.list();
      },
      handleTableChange(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>