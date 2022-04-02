<template>
  <div>
    <a-row :gutter="[8, 8]">
      <a-col :span="8">
        <a-card title="今日销售额" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">1200</div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="今日销售笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">33</div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="今日采购笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">10</div>
        </a-card>
      </a-col>

      <a-col :span="24">
        <a-card title="待办事项" size="small">
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;">
            <a-statistic title="待入库" :value="33" />
          </a-card-grid>
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;">
            <a-statistic title="待出库" :value="23" />
          </a-card-grid>
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;">
            <a-statistic title="库存预警" :value="5" />
          </a-card-grid>
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;">
            <a-statistic title="应收欠款" :value="3121" />
          </a-card-grid>
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;">
            <a-statistic title="应付欠款" :value="13230" />
          </a-card-grid>
        </a-card>
      </a-col>

      <a-col :span="24">
        <a-card title="ERP操作快捷入口" size="small">
          <a-row gutter="0">
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">采购开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">销售开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">入库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">出库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">盘点</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">调拨</div>
              </a-card-grid>
            </a-col>
          </a-row>
        </a-card>
      </a-col>

      <a-col :span="12">
        <sales-trend />
      </a-col>

      <a-col :span="12">
        <sales-goods />
      </a-col>
    </a-row>
  </div>
</template>

<script>
export default {
  components: {
    SalesTrend: () => import("./salesTrend.vue"),
    SalesGoods: () => import("./salesGoods.vue"),
  },
};
</script>

<style scoped></style>
