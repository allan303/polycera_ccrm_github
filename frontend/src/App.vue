<template>
  <div class="container-sm bg-light" id="all">
    <div class="row">
      <AppHeader :switchSide="switchSide"></AppHeader>
    </div>
    <div class="row mx-2">
      <div
        :class="`col-md-${side_col} d-none d-md-block`"
        v-if="showSide && store.getters.isLogin()"
      >
        <AppSide></AppSide>
      </div>

      <div :class="` col-md-${main_col}`">
        <main class="main-view">
          <router-view :key="route.fullPath"></router-view>
        </main>
      </div>
    </div>
    <div class="row">
      <AppFooter></AppFooter>
    </div>
  </div>
</template>
<script>
import {
  computed,
  onMounted,
  reactive,
  toRefs,
  provide,
  getCurrentInstance,
} from "vue";
import { useRoute } from "vue-router";
import { useStore, useAxios } from "@/main";
import AppFooter from "@/components/AppFooter";
import AppSide from "@/components/AppSide";
import AppHeader from "@/components/AppHeader";
import { useI18n } from "vue-i18n/index";

export default {
  name: "App",
  components: { AppSide, AppHeader, AppFooter },
  setup() {
    const route = useRoute();
    const store = useStore();
    const axios = useAxios();
    const data = reactive({
      // user showSide boolean
      showSide: true,
      // side bar col grid
      side_col: 3,
    });
    const { t, locale } = useI18n();
    provide("t", t);
    provide("locale", locale);

    // main-content col grid
    const main_col = computed(() => {
      if (!store.getters.isLogin()) {
        return 12;
      } else {
        //登录环境
        if (data.showSide) {
          return 12 - data.side_col;
        } else {
          return 12;
        }
      }
    });
    const { proxy } = getCurrentInstance();
    const updateLocale = () => {
      // 更新locale 仅仅与 state.local关联
      proxy.$i18n.locale = store.state.local.locale;
    };

    provide("updateLocale", updateLocale);
    onMounted(() => {
      // init localstorage
      store.actions.getStateFromLocalStorage();
      if (store.getters.isTokenExpired()) {
        //15分钟时候 更新token
        updateToken(); //如果token已经过期则会跳到登录
      }
      setTimeout(function () {
        store.actions.updateCacheInfo(axios, "");
      }, 2000);

      updateLocale();
    });
    const switchSide = () => {
      data.showSide = !data.showSide;
    };
    const updateToken = () => {
      //通过token，申请新的token，更新token时间及所有信息
      axios({
        method: "post",
        url: `/auth/update_token`,
      }).then((res) => {
        store.actions.setState(res.data);
        store.actions.setTokenRecieveTime();
      });
    };
    provide("updateToken", updateToken);

    return {
      ...toRefs(data),
      main_col,
      route,
      store,
      switchSide,
      t,
    };
  },
};
</script>
<style >
/* .main-part {
  padding: 15px;
} */
/* #all {
  background-color: #d2f4ea;
} */
.main-view {
  min-height: 750px;
}

.bi {
  vertical-align: -0.125em;
  pointer-events: none;
  fill: currentColor;
}

.dropdown-toggle {
  outline: 0;
}

.nav-flush .nav-link {
  border-radius: 0;
}

.btn-toggle {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.65);
  background-color: transparent;
  border: 0;
}
.btn-toggle:hover,
.btn-toggle:focus {
  color: rgba(0, 0, 0, 0.85);
  background-color: #d2f4ea;
}

.btn-toggle::before {
  width: 1.25em;
  line-height: 0;
  /* content: url("data:image/svg+xml,%3csvg xmlns='@/assets/dot.svg' width='16' height='16' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%280,0,0,.5%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 14l6-6-6-6'/%3e%3c/svg%3e"); */
  transition: transform 0.35s ease;
  transform-origin: 0.5em 50%;
}

.btn-toggle[aria-expanded="true"] {
  color: rgba(0, 0, 0, 0.85);
}
.btn-toggle[aria-expanded="true"]::before {
  transform: rotate(90deg);
}

.btn-toggle-nav a {
  display: inline-flex;
  padding: 0.1875rem 0.5rem;
  margin-top: 0.125rem;
  margin-left: 1.25rem;
  text-decoration: none;
}
.btn-toggle-nav a:hover,
.btn-toggle-nav a:focus {
  background-color: #d2f4ea;
}

.scrollarea {
  overflow-y: auto;
}

.fw-semibold {
  font-weight: 600;
}
.lh-tight {
  line-height: 1.25;
}
</style>