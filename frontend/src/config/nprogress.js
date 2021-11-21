import NProgress from 'nprogress';// vue nprogress loading bar
import 'nprogress/nprogress.css';// 进度条样式
NProgress.configure({// NProgress 进度条配置
    minimum: 0.1,//在开始使用的最小百分比变化
    easing: 'ease',
    speed: 1500,
    showSpinner: false,//关闭旋转圈
});

export default NProgress