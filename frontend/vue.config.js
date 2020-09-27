const CompressionWebpackPlugin = require('compression-webpack-plugin');


module.exports = {
  assetsDir: 'static',
  configureWebpack: {
    externals: {
      'ant-design-vue': 'Antd',
      'vue-router': 'VueRouter',
      'js-cookie': 'Cookies',
      'axios': 'axios',
      'vue': 'Vue',
      'qs': 'Qs',
      'moment': 'moment',
      'number-precision': 'NP',
      '@antv/g2': 'Chart',
      'html2canvas': 'html2canvas',
      'jspdf': 'jspdf',
    },
    plugins: [
      new CompressionWebpackPlugin({
        algorithm: 'gzip',
        test: /\.(js|css|json|txt|html|ico|svg)(\?.*)?$/i,
        threshold: 2048,
        deleteOriginalAssets: false,
        minRatio: 0.8
      })]
  },
}
