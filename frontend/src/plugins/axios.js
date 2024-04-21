"use strict";
// 生成一个axios instance，之后再 main.js 中挂载到vue app instance上
import axios from "axios";
// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
//工厂函数
export const createAxios = (store, router) => {
  let config = {
    baseURL: process.env.VUE_APP_AXIOS_API,
    // baseURL: myconfig.baseURL,
    timeout: 60 * 1000, // Timeout
    // withCredentials: true, // Check cross-site Access-Control

  };
  //创建一个实例
  const axiosInstance = axios.create(config);
  // axiosInstance.defaults.headers.post['Access-Control-Allow-Headers'] = "content-type,XXX";
  // axiosInstance.defaults.headers.post['Access-Control-Allow-Methods'] = '*';
  // // response.setHeader("Access-Control-Allow-Origin", origin);
  // axiosInstance.defaults.headers.post['Access-Control-Allow-Credentials'] = 'true';


  //Axios Request 中间件
  axiosInstance.interceptors.request.use(
    function (config) {
      // Before Request 执行 中间件
      // 1) 添加 AccessToken
      const token_type = store.state.token_type || 'Bearer'
      const access_token = store.state.access_token || ''
      config.headers.Authorization = `${token_type} ${access_token}`
      // console.log("AXIOS::", "METHOD:", config.method, "URL:", config.url,)
      return config;
    },
    function (error) {
      // 返回Request Err 之前执行中间件
      console.log(error)
      return Promise.reject(error);
    }
  );

  //Axios response中间件
  axiosInstance.interceptors.response.use(res => {
    //此处是response成功(Axios设置中已经设定了状态码的成功范围，超出范围则移到error中)
    // const nexturl = route.path
    // if (nexturl) { router.push(nexturl) }
    return res;
  }, error => {
    console.log(error)
    //其他原因导致的错误
    // 这里我们把错误信息扶正, 后面就不需要写 catch 了
    if (error.response) {
      console.log(error.response)
      const code = error.response.status
      const route = router.currentRoute.value
      const nexturl = route.fullPath
      // auth错误
      if (code === 401) {
        //登录失败
        store.actions.resetState()
        router.push({ path: '/auth/login', query: { nexturl: nexturl } })
        alert(error.response.data.detail || error.response.statusText)
        return Promise.reject(error.response.data.detail)
      } else {
        // router.go(-1)
        alert(error.response.data.detail || error.response.statusText)
        return Promise.reject(error)
      }
    }
    else { return Promise.reject(error) }
  })
  return axiosInstance
}
//用于 provide & inject
// export const symbolAxios = Symbol('axios');
// export const useAxios = () => inject(symbolAxios);
// export default createAxios


