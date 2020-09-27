<template>
  <div>
    <a-card style="height: calc(50vh - 48px);">
      <div slot="title">
        <span>销售前十商品</span>
        <a-range-picker v-model="dateRange" :ranges="ranges" :disabled="salesLoading" :allowClear="false"
          @change="changeDateRange" style="float: right;" />
        <div id="salesGoods" style="margin-top: 36px; padding-left: 32px;"></div>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesTopTenList } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'SalesGoods',
    data() {
      return {
        ranges: {
          '7天': [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
          '15天': [moment().add(-15, 'days').startOf('day'), moment().startOf('day')],
          '30天': [moment().add(-30, 'days').startOf('day'), moment().startOf('day')],
        },
        dateRange: [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
        chart: null,
        loading: false,
      };
    },
    methods: {
      initialize() {
        let height = window.innerHeight / 2 - 141;
        this.chart = new window.G2.Chart({ container: 'salesGoods', autoFit: true, height });
        this.chart.scale('_quantity', { alias: '销量' });
        this.chart.interval().position('_goods*_quantity');
        this.list();
      },
      list() {
        let form = {
          start_date: this.dateRange[0].format(),
          end_date: this.dateRange[1].format(),
        };

        this.loading = true;
        salesTopTenList(form)
          .then(resp => {
            this.chart.changeData(resp.data.results);
            this.chart.forceFit();
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      changeDateRange(dateRange) {
        this.dateRange = dateRange;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>