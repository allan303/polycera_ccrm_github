<template>
  <header
    class="
      d-flex
      flex-wrap
      align-items-center
      justify-content-center justify-content-md-between
      py-3
      mb-4
      border-bottom
    "
  >
    <a
      class="
        d-flex
        align-items-center
        col-md-3
        mb-2 mb-md-0
        text-dark text-decoration-none
      "
    >
      <!-- <h3 class="text-primary">Company LOGO</h3> -->
      <img src="@/assets/logo.png" alt="COMPANY LOGO" class="img-fluid" />
    </a>

    <!-- <div class="col-md-3 text-end">
      <button type="button" class="btn btn-outline-primary me-2">请登录</button>
    </div> -->
    <div class="d-flex">
      <button
        class="btn btn-primary"
        type="submit"
        v-if="!store.getters.isLogin()"
        @click.prevent="router.push('/auth/login')"
      >
        {{ $t("auth.login") }}
      </button>
      <button
        class="btn btn-light"
        v-if="!store.getters.isLogin()"
        @click="switchLang"
      >
        {{ $t("auth.lang") }}
      </button>
      <!-- workgroup切换 -->
      <div class="flex-shrink-0 btn dropdown" v-if="store.getters.isSu()">
        <a
          href="#"
          class="dropdown-toggle btn fw-bolder"
          id="dropdownUser2"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{
            store.getters.objName(
              "workgroup_sid",
              store.state.local.workgroup_sid,
              "name"
            ) || "No workgroup"
          }}
        </a>
        <ul
          class="dropdown-menu text-small shadow"
          aria-labelledby="dropdownUser2"
        >
          <li
            v-for="(workgroup, index) in store.state.cacheInfo.workgroup"
            :key="index"
          >
            <AppHeaderWorkgroup :workgroup="workgroup"></AppHeaderWorkgroup>
          </li>
        </ul>
      </div>
      <!-- 用户下拉菜单 -->
      <div class="flex-shrink-0 btn dropdown" v-if="store.getters.isLogin()">
        <a
          href="#"
          class="dropdown-toggle btn fw-bolder"
          id="dropdownUser2"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{ store.state.cu.username }}
        </a>
        <ul
          class="dropdown-menu text-small shadow"
          aria-labelledby="dropdownUser2"
        >
          <li>
            <a class="dropdown-item" @click="router.push('/')">{{
              $t("auth.home")
            }}</a>
          </li>
          <li>
            <a class="dropdown-item" @click="switchLang">{{
              $t("auth.lang")
            }}</a>
          </li>
          <li>
            <a class="dropdown-item" @click="router.push('/auth/myprofile')">{{
              $t("auth.profile")
            }}</a>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li v-if="!store.state.local.use_half">
            <a
              class="dropdown-item"
              @click="store.actions.updateLocalByKey('use_half', true)"
              >{{ $t("auth.displayTwoCols") }}</a
            >
          </li>
          <li v-else>
            <a
              class="dropdown-item"
              @click="store.actions.updateLocalByKey('use_half', false)"
              >{{ $t("auth.displayNormal") }}</a
            >
          </li>
          <li>
            <a class="dropdown-item" @click="reGetAllCache">{{
              $t("auth.reGetAllCache")
            }}</a>
          </li>
          <li v-if="store.getters.isSu()">
            <a class="dropdown-item" @click="resetAllCacheBackend">{{
              $t("auth.resetAllCacheBackend")
            }}</a>
          </li>
          <li>
            <a class="dropdown-item" @click="updateToken">{{
              $t("auth.updateToken")
            }}</a>
          </li>
          <li>
            <a class="dropdown-item" @click="showLogoutConfirm">{{
              $t("auth.logout")
            }}</a>
          </li>
        </ul>
      </div>
      <button
        class="btn ms-3 d-none d-md-block"
        @click="switchSide"
        v-if="store.getters.isLogin()"
      >
        <!-- 切换 侧边栏（大屏幕） -->
        <i class="bi-grid-fill" style="font-size: 1em"></i>
      </button>
      <!-- 切换 侧边栏（小屏幕） -->
      <AppSideOff v-if="store.getters.isLogin()"></AppSideOff>
    </div>
  </header>
</template>
<script>
import { useRoute, useRouter } from "vue-router";
import { useStore, useAxios } from "@/main";
import { toRefs, reactive, defineComponent, inject } from "vue";
import AppHeaderWorkgroup from "./AppHeaderWorkgroup.vue";
import { confirmDo } from "@/myjs";
// import { i18n } from "@/i18n";
import AppSideOff from "./AppSideOff.vue";
export default defineComponent({
  name: "App",
  props: { switchSide: { type: Function } },
  components: { AppSideOff, AppHeaderWorkgroup },
  setup() {
    const data = reactive({
      on: false,
      openMenu: false,
    });
    const store = useStore();
    const axios = useAxios();
    const router = useRouter();
    const route = useRoute();
    const updateToken = inject("updateToken");
    const logout = () => {
      store.actions.resetState();
      router.push("/auth/login");
      return false;
    };
    const showLogoutConfirm = () => {
      confirmDo("确定退出？", logout);
    };
    // const clickHandle = () => {
    //   emit("click");
    // };
    //手动更新 选项
    const reGetAllCache = () => {
      store.actions.updateCacheInfo(axios);
      alert("更新选项成功!");
    };
    const resetAllCacheBackend = () => {
      //更新后台的所有cache
      axios({
        method: "post",
        url: "/auth/reset_all_cache_info",
      }).then(() => {
        //后台更新缓存后，前台再全部获取
        reGetAllCache();
      });
    };
    const updateLocale = inject("updateLocale");
    const switchLang = () => {
      store.actions.switchLocale();
      updateLocale();
      store.actions.setStateToLocalStorage();
    };
    return {
      router,
      route,
      store,
      ...toRefs(data),
      showLogoutConfirm,
      reGetAllCache,
      switchLang,
      resetAllCacheBackend,
      updateToken,
    };
  },
});
</script>
<style scoped>
.form-control-dark {
  color: #fff;
  background-color: var(--bs-dark);
  border-color: var(--bs-gray);
}
.form-control-dark:focus {
  color: #fff;
  background-color: var(--bs-dark);
  border-color: #fff;
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}

.bi {
  vertical-align: -0.125em;
  fill: currentColor;
}

.text-small {
  font-size: 85%;
}

.dropdown-toggle {
  outline: 0;
}
</style>
