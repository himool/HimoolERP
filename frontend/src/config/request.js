import axios from 'axios';
import NProgress from './nprogress'; // 进度条配置
import config from './api'
import Vue from 'vue'

const service = axios.create({
    baseURL: config.baseUrl,
    timeout: 0,
    withCredentials: true,
});

service.interceptors.request.use(config => {
    NProgress.start();
    return config;
}, error => {
    NProgress.done();
    return Promise.reject();
});


service.interceptors.response.use(response => {
    NProgress.done();

    let { status, statusText } = response;
    var preStatus = parseInt(status / 100);
    if (preStatus === 2) {
        return response;
    } else {
        Vue.prototype.$message.error(`${status}：${statusText}`);
        if (status === 404) {
            // router.push({ path: "/login" })
        }
        return Promise.reject();
    }
}, (error) => {
    var response = error.response;
    if (response.data) {
        var data = response.data;
        // 递归函数，穷尽所有报错
        function outPutErrMsg(msgData) {
            if (Object.prototype.toString.call(msgData) === '[object Object]') {
                for (const key in msgData) {
                    if (Object.hasOwnProperty.call(msgData, key)) {
                        const oneMsg = msgData[key];
                        if (oneMsg && Array.isArray(oneMsg)) {
                            oneMsg.forEach((twoMsg) => {
                                if (twoMsg && Array.isArray(twoMsg)) {
                                    twoMsg.forEach((threeMsg) => {
                                        Vue.prototype.$message.error(`报错字段：${key}\n${threeMsg}`);
                                    });
                                } else {
                                    if (Object.prototype.toString.call(twoMsg) === '[object Object]'
                                    ) {
                                        outPutErrMsg(twoMsg);

                                    } else {
                                        Vue.prototype.$message.error(`报错字段：${key}\n${twoMsg}`);
                                    }
                                }
                            });
                        } else {
                            Vue.prototype.$message.error(`${oneMsg}`);
                        }
                    }
                }
            } else {
                Vue.prototype.$message.error(`${msgData}`);
            }

        }
        outPutErrMsg(data);
    } else {
        Vue.prototype.$message.error(`请求失败:${error}`);
    }
    NProgress.done();
    return Promise.reject();
});

export default service;