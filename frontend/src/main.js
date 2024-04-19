import { createApp, inject } from 'vue'
import App from './App.vue'
// app级别
import { createMyRouter } from './router'
import { createStore } from './store';
import { createAxios } from "@/plugins/axios"
import { i18n } from "@/i18n/index"
import numeral from "numeral";
import moment from 'moment';
import 'moment/locale/zh-cn';
import 'moment/locale/es-us';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
//注册chartjs组件
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const app = createApp(App)
app.use(i18n)
// 使用 vue-router
//创建 Store
const storeInstance = createStore()
// 去往route之前的中间件
const routerInstance = createMyRouter(storeInstance)
app.use(routerInstance)

// 创建 axiosInstance 并且挂载
const axiosInstance = createAxios(storeInstance, routerInstance)
//挂载到ctx上，方便使用
// app.config.globalProperties.$axios = axiosInstance
// app.config.globalProperties.$store = storeInstance
// app.config.globalProperties.$router = routerInstance

// provide 函数 接受 一个 Symbol + 一个object
//相当于在 App.vue最顶层组件Provide 了 Store
//Provide
const symbolStore = Symbol('store');
app.provide(symbolStore, storeInstance);
export const useStore = () => inject(symbolStore);

const symbolAxios = Symbol('axios');
app.provide(symbolAxios, axiosInstance);
export const useAxios = () => inject(symbolAxios);

app.provide('moment', moment);
app.provide('numeral', numeral);

// Mount
app.mount('#app')

