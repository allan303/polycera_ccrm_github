import { createRouter, createWebHashHistory } from 'vue-router'
import config from './children/config';
import auth from './children/auth';
import oem from './children/oem';
import project from './children/project';
import project_update from './children/project_update';
import project_oem from './children/project_oem';
import contact from './children/contact';
import post from './children/post';
import order from './children/order';
import order_update from './children/order_update';
// import comment from './children/comment';
import pilot from './children/pilot';
import product from './children/product';
import user from './children/user';
import role from './children/role';
import workgroup from './children/workgroup';
import design from './children/design';
import standard_design from './children/standard_design';
import design_module from './children/design_module';

// 工厂函数，这样可以传递 store

export const createMyRouter = (store) => {
  const routes = [
    //非su
    ...post,
    ...project,
    ...oem,
    ...contact,
    ...order,
    ...pilot,
    ...design,
    ...standard_design,
    ...auth,
    //admin
    // ...comment,
    ...design_module,
    ...product,
    ...project_update,
    ...project_oem,
    ...order_update,
    ...user,
    ...role,
    ...workgroup,
    ...config,

    {
      path: '/',
      name: 'Home',
      meta: { loginRequired: false, title: 'home' },
      component: () => import('@/views/common/Home'),
    },
    {
      //新的版本 不能直接用 '*'
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/common/404')
    }
  ];

  const router = createRouter({
    history: createWebHashHistory(process.env.BASE_URL),
    routes,
  })

  // 每次request的中间函数
  router.beforeEach((to, from) => {
    //登录权限
    // console.log("from", from.path)
    // console.log("to", to.path)
    //本页面操作时候不到页面顶部（如 表格中删除某一个行）
    if (to.path !== from.path) { window.scrollTo(0, 0) }
    // from;
    //依然没有时候
    if (!store.getters.isLogin() && (to.meta.loginRequired || to.meta.suRequired)) {
      router.push({ path: '/auth/login', query: { nexturl: to.path } });
      alert('请先登录！')
      return false
    } else if (!store.getters.isSu() && to.meta.suRequired) {
      alert('仅限超级管理员！')
      //返回上一页
      router.go(-1)
      return false
    }
  })

  return router
}



