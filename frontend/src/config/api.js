const uploadUrl = 'api/goods_images/'; // 上传地址
const devConfig = {
    baseUrl: 'http://localhost:8080/',
    staticUrl: 'http://localhost:8080/', // 静态资源地址
    uploadUrl: uploadUrl, // 上传地址
};

const prodConfig = {
    baseUrl: 'http://114.218.158.78:9900/',
    staticUrl: 'http://114.218.158.78:9900/', // 静态资源地址
    uploadUrl: uploadUrl, // 上传地址
};

let config;
if (process.env.NODE_ENV === 'development' || !process.env.NODE_ENV) {
    config = devConfig;
} else if (process.env.NODE_ENV === 'production') {
    config = prodConfig;
}

export default config;