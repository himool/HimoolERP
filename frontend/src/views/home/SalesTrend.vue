<template>
  <div>
    <a-card style="height: calc(50vh - 48px);">
      <div slot="title">
        <span>销售走势</span>
        <a-range-picker v-model="dateRange" :ranges="ranges" :disabled="loading" :allowClear="false"
          @change="changeDateRange" style="float: right;" />
        <div id="salesTrend" style="margin-top: 36px;"></div>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesValueList } from '@/api/sales'
  import moment from 'moment'

  export default {
    name: 'SalesTrend',
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
        this.chart = new window.G2.Chart({ container: 'salesTrend', autoFit: true, height, });
        this.chart.scale({ _date: { range: [0, 1] }, _amount: { nice: true } });
        this.chart.tooltip({ showCrosshairs: true, shared: true });
        this.chart.line().position('_date*_amount').color('_warehouse').shape('smooth');
        this.chart.point().position('_date*_amount').color('_warehouse').shape('circle');
        this.list();
      },
      list() {
        let form = {
          start_date: this.dateRange[0].format(),
          end_date: this.dateRange[1].format(),
        };

        this.loading = true;
        salesValueList(form)
          .then(resp => {
            let data = [...resp.data.results, ...this.fillData(resp.data.results, resp.data.warehouse_list)];
            this.chart.changeData(data);
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
      fillData(items, warehouseList) {
        let startDate = moment(this.dateRange[0]);
        let endData = moment(this.dateRange[1]);
        let days = endData.diff(startDate, 'days');
        let fillItems = [];
        
        for (let i = 0; i <= days; i++) {
          for (let w of warehouseList) {
            if (items.findIndex(item => item._warehouse === w && item._date === startDate.format('YYYY-MM-DD')) === -1) {
              fillItems.push({ _date: startDate.format('YYYY-MM-DD'), _warehouse: w, _amount: 0 });
            }
          }
          startDate.add(1, 'days');
        }
        return fillItems;
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>