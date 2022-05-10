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
      'moment': 'moment',
      'number-precision': 'NP',
      'vuex': 'Vuex',
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
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true,
      }
    }
  },
  devServer: {
    proxy: {
        '/api': {
          target: 'http://114.218.158.78:12223',
          changeOrigin: true,
        }
    }
  },
}