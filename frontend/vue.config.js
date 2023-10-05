const CompressionWebpackPlugin = require("compression-webpack-plugin");

module.exports = {
  assetsDir: "static",
  configureWebpack: {
    plugins: [
      new CompressionWebpackPlugin({
        algorithm: "gzip",
        test: /\.(js|css|json|txt|html|ico|svg)(\?.*)?$/i,
        threshold: 2048,
        deleteOriginalAssets: false,
        minRatio: 0.8,
      }),
    ],
  },
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true,
      },
    },
  },
  devServer: {
    proxy: {
      "/api": {
        // target: "http://114.218.158.78:12223",
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
};
