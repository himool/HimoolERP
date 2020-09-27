<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24" :xl="12" style="margin-bottom: 12px;">
        <a-card>
          <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="tableLoading"
            :customRow="customRow" :rowClassName="rowClassName">
            <div slot="action" slot-scope="value, item">
              <a-button-group>
                <a-button type="primary" size="small" @click.stop="copyRole(item)">
                  <a-icon type="copy" />复制
                </a-button>
                <a-popconfirm :title="`删除角色: ${item.name}`" ok-text="确认" cancel-text="取消" @confirm="destroy(item)">
                  <a-button type="danger" size="small" @click.stop>
                    <a-icon type="delete" />删除
                  </a-button>
                </a-popconfirm>
              </a-button-group>
            </div>
          </a-table>
        </a-card>
      </a-col>
      <a-col :span="24" :xl="12" style="margin-bottom: 12px;">
        <a-card :title="selectedRole ? `角色信息: ${selectedRole.name}` : '角色信息'">
          <div>
            <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
              <a-row>
                <a-col :span="24" :md="12">
                  <a-form-model-item prop="name" label="名称">
                    <a-input v-model="form.name" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="24" :md="12">
                  <a-form-model-item prop="remark" label="备注">
                    <a-input v-model="form.remark" />
                  </a-form-model-item>
                </a-col>
              </a-row>
            </a-form-model>
            <a-divider style="margin: 0" />
            <a-checkbox-group v-model="form.permissions">
              <div>
                <div style="font-size: 16px; margin: 12px 0;">商品
                  <a-checkbox value="goods" :indeterminate="checkStatus.goods.indeterminate"
                    :checked="checkStatus.goods.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...goodsOptions1, ...goodsOptions2])" />
                </div>

                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in goodsOptions1" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in goodsOptions2" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
              <div>
                <div style="font-size: 16px; margin: 12px 0;">采购
                  <a-checkbox value="purchase" :indeterminate="checkStatus.purchase.indeterminate"
                    :checked="checkStatus.purchase.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...purchaseOptions])" />
                </div>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in purchaseOptions" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
              <div>
                <div style="font-size: 16px; margin: 12px 0;">销售
                  <a-checkbox value="sales" :indeterminate="checkStatus.sales.indeterminate"
                    :checked="checkStatus.sales.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...salesOptions])" />
                </div>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in salesOptions" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
              <div>
                <div style="font-size: 16px; margin: 12px 0;">公司
                  <a-checkbox value="warehouse" :indeterminate="checkStatus.warehouse.indeterminate"
                    :checked="checkStatus.warehouse.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...warehouseOptions1, ...warehouseOptions2, ...warehouseOptions3])" />
                </div>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in warehouseOptions1" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in warehouseOptions2" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in warehouseOptions3" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
              <div>
                <div style="font-size: 16px; margin: 12px 0;">报表
                  <a-checkbox value="report" :indeterminate="checkStatus.report.indeterminate"
                    :checked="checkStatus.report.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...reportOptions])" />
                </div>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in reportOptions" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
              <div>
                <div style="font-size: 16px; margin: 12px 0;">账户
                  <a-checkbox value="account" :indeterminate="checkStatus.account.indeterminate"
                    :checked="checkStatus.account.isCheckAll" style="margin-left: 4px;"
                    @change="(e) => checkAll(e.target.checked, [...accountOptions])" />
                </div>
                <a-row style="margin: 8px 0;">
                  <a-checkbox v-for="item in accountOptions" :key="item.value" :value="item.value">{{item.label}}
                  </a-checkbox>
                </a-row>
              </div>
            </a-checkbox-group>
          </div>
          <div style="margin: 32px 0 12px 0;">
            <a-button type="primary" @click="form.id ? update() : create()">
              {{form.id ? '保存' : '添加'}}</a-button>
            <a-button style="margin-left: 12px;" @click="resetForm">清空数据</a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import {
    goodsOptions1, goodsOptions2, purchaseOptions, salesOptions, warehouseOptions1,
    warehouseOptions2, warehouseOptions3, reportOptions, accountOptions
  } from './permissions.js'
  import { roleList, roleCreate, roleUpdate, roleDestroy } from '@/api/account'

  export default {
    name: 'Role',
    data() {
      return {
        columns: [
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: '备注',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true,
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            scopedSlots: { customRender: 'action' },
            width: '160px',
          },
        ],
        items: [],
        selectedRole: null,
        form: {
          name: '',
          remark: '',
          permissions: [],
        },
        rules: {
          name: [
            { required: true, message: '请输入角色名称', trigger: 'change' },
          ],
        },

        goodsOptions1,
        goodsOptions2,
        purchaseOptions,
        salesOptions,
        warehouseOptions1,
        warehouseOptions2,
        warehouseOptions3,
        reportOptions,
        accountOptions,

        tableLoading: false,
        buttonLoading: false,
      };
    },
    computed: {
      checkStatus() {
        return {
          goods: this.checkGroup([...this.goodsOptions1, ...this.goodsOptions2]),
          purchase: this.checkGroup([...this.purchaseOptions]),
          sales: this.checkGroup([...this.salesOptions]),
          warehouse: this.checkGroup([...this.warehouseOptions1, ...this.warehouseOptions2, ...this.warehouseOptions3]),
          report: this.checkGroup([...this.reportOptions]),
          account: this.checkGroup([...this.accountOptions]),
        }
      },
    },
    methods: {
      initialize() {
        this.tableLoading = true;
        roleList()
          .then(resp => {
            this.items = resp.data;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.tableLoading = false;
          });
      },
      create() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.buttonLoading = true;
            let form = { ...this.form };
            form.permissions = form.permissions.filter(p => /^[A-Z_]+$/.test(p));

            roleCreate(form)
              .then(resp => {
                this.$message.success('添加成功');
                this.items.push(resp.data);
                this.resetForm();
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.buttonLoading = false;
              });
          }
        });
      },
      update() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.buttonLoading = true;
            let form = { ...this.form };
            form.permissions = form.permissions.filter(p => /^[A-Z_]+$/.test(p));

            roleUpdate(form)
              .then(resp => {
                this.$message.success('修改成功');
                this.items.splice(this.items.findIndex(item => item.id === resp.data.id), 1, resp.data);
              })
              .catch(err => {
                this.$message.error(err.response.data.message);
              })
              .finally(() => {
                this.buttonLoading = false;
              });
          }
        });
      },
      destroy(item) {
        let form = { ...item };
        roleDestroy(form)
          .then(() => {
            this.$message.success('删除成功');
            this.items.splice(this.items.findIndex(item => item.id === form.id), 1);
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          });
      },
      resetForm() {
        this.form = { name: '', remark: '', permissions: [] };
      },
      customRow(item) {
        return {
          on: {
            click: () => {
              this.$refs.form.clearValidate();
              this.form = { ...item };
            },
          },
        }
      },
      rowClassName(item) {
        if (item.id == this.form.id) {
          return 'table-selected'
        }
      },
      copyRole(item) {
        let form = { ...item };
        form.id = undefined;
        form.name += '_复制';
        this.form = form;
      },
      checkAll(checked, items) {
        for (let item of items) {
          let index = this.form.permissions.indexOf(item.value);
          if (checked && index == -1) {
            this.form.permissions.push(item.value);
          }

          if (!checked && index != -1) {
            this.form.permissions.splice(index, 1);
          }
        }
      },
      checkGroup(items) {
        let status = { indeterminate: false, isCheckAll: true };

        for (let item of items) {
          if (this.form.permissions.indexOf(item.value) == -1) {
            status.isCheckAll = false;
          } else {
            status.indeterminate = true;
          }
        }

        if (status.isCheckAll && status.indeterminate) {
          status.indeterminate = false;
        }

        return status
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scope>
  .table-selected {
    background: #e6f7ff;
  }
</style>