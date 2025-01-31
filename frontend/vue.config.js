module.exports = {
  devServer: {
    port: 8081,
    proxy: {
      '^/api': {
        target: 'http://localhost:8080/',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api/': '/', // remove base path
        },
      },
    },
  },
  lintOnSave: false
};
