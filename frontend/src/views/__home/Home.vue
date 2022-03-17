<template>
  <div>
    <a-row :gutter="[8, 8]">
      <a-col :span="6">
        <a-card title="今日销售额" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">12</div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card title="今日销售笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">12</div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card title="今日采购笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">12</div>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card title="今日资金入账" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">12</div>
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

      <a-col :span="8">
        <sales-trend />

        <!-- <a-card title="销售统计" size="small">
        </a-card> -->
      </a-col>

      <a-col :span="8">
        <sales-goods />

        <!-- <a-card title="销售前十商品" size="small">
        </a-card> -->
      </a-col>

      <a-col :span="8">
        <a-card title="采购前十商品" size="small">1</a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
export default {
  components: {
      SalesTrend: () => import('./salesTrend.vue'),
      SalesGoods: () => import('./salesGoods.vue'),
    },
};
</script>

<style scoped></style>
