<template>
  <div class="row justify-content-center">
    <div class="col-12" v-if="formData.is_deleted">
      <div class="alert alert-warning" role="alert">
        {{ $t("common.deletedWarning") }}
      </div>
    </div>
  </div>
  <div
    class="row my-1 justify-content-end"
    v-if="['create', 'edit'].includes(urlName)"
  >
    <div class="col-12 text-end">
      <div class="btn-group" role="group">
        <button
          class="btn btn-sm btn-primary me-1"
          @click="saveTempToLocalStorage"
        >
          {{ $t("actions.saveTempToLocalStorage") }}
        </button>
        <button class="btn btn-sm btn-success" @click="getTempFromLocalStorage">
          {{ $t("actions.getTempFromLocalStorage") }}
        </button>
      </div>
    </div>
  </div>
  <div class="row" v-if="urlName === 'read'">
    <StandardReadUrls
      :readUrlDict="readUrlDict"
      :formData="formData"
    ></StandardReadUrls>
  </div>
  <MyTab :tabs="tabsFinal" v-model="activeTabIndex"></MyTab>
  <div class="row">
    <slot></slot>
    <slot name="tab0" v-if="activeTabIndex === 0"></slot>
    <slot name="tab1" v-if="activeTabIndex === 1"></slot>
    <slot name="tab2" v-if="activeTabIndex === 2"></slot>
    <slot name="tab3" v-if="activeTabIndex === 3"></slot>
    <slot name="tab4" v-if="activeTabIndex === 4"></slot>
    <slot name="tab5" v-if="activeTabIndex === 5"></slot>
    <slot name="tab6" v-if="activeTabIndex === 6"></slot>
    <slot name="tab7" v-if="activeTabIndex === 7"></slot>
    <slot name="tab8" v-if="activeTabIndex === 8"></slot>
    <slot name="tab9" v-if="activeTabIndex === 9"></slot>
    <slot name="tab10" v-if="activeTabIndex === 10"></slot>
    <slot name="tab11" v-if="activeTabIndex === 11"></slot>
    <slot name="tab12" v-if="activeTabIndex === 12"></slot>
    <slot name="tab13" v-if="activeTabIndex === 13"></slot>
    <slot name="tab14" v-if="activeTabIndex === 14"></slot>
    <StandardActionBtns
      :urlName="urlName"
      :urlModel="urlModel"
      :formData="formData"
    ></StandardActionBtns>
  </div>
</template>

<script>
import {
  onMounted,
  computed,
  defineComponent,
  inject,
  watch,
  ref,
  provide,
} from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from "vue-router";
import { useAxios, useStore } from "@/main";
import StandardActionBtns from "@/components/StandardActionBtns";
import MyTab from "@/components/ui/MyTab";

// import FormTextarea from "@/components/ui/FormTextarea";
// import FormSelect from "@/components/ui/FormSelect";
import StandardReadUrls from "./StandardReadUrls";
// import FormInput from "@/components/ui/FormInput";
export default defineComponent({
  props: {
    readUrlDict: { type: Object },
    urlModel: { type: String, default: null },
  },
  // components: { StandardActionBtns, FormSelect, FormTextarea, FormInput },
  components: {
    StandardActionBtns,
    StandardReadUrls,
    MyTab,
  },
  setup() {
    provide("isList", false);
    provide("fetchListItems", null);
    const urlName = inject("urlName");
    const storeLocal = inject("storeLocal");
    const tabs = storeLocal.state.tabs;
    const tabsNoCreate = storeLocal.state.tabsNoCreate;
    const tabsFinal = computed(() => {
      if (typeof tabs !== "object") {
        //判定类型
        return [];
      }
      if (urlName === "create") {
        return tabs;
      } else {
        return tabs.concat(tabsNoCreate);
      }
    });
    const activeTabIndex = ref(0);
    const formData = storeLocal.state.fd;
    const route = useRoute();
    const moment = inject("moment");
    const axios = useAxios();
    const store = useStore();
    const cacheInfo = computed(() => store.state.cacheInfo);

    // 以下为方法
    const getCurrentObj = () => {
      axios({
        method: "get",
        url: `/${route.meta.model}/read/${route.params.sid}`,
      }).then((res) => {
        Object.assign(formData, res.data);
      });
    }; //路由显性传递的参数

    //数据
    const setFromParams = () => {
      //从query中提取 数据
      const queries = route.query;
      if (!queries || Object.keys(queries).length === 0) {
        return false;
      }
      const sids = [
        "project_sid",
        "oem_sid",
        "contact_sid",
        "design_sid",
        "order_sid",
        "quote_sid",
        "pilot_sid",
        "post_sid",
      ];
      for (let k in queries) {
        if (sids.includes(k)) {
          formData[k] = queries[k];
        }
      }
    };

    onMounted(() => {
      if (["read", "edit"].includes(urlName)) {
        getCurrentObj();
      } else if (urlName === "create") {
        setTimeout(setFromParams, 1000);
      }
    });
    watch(
      () => route,
      () => {
        setFromParams();
      },
      { immediate: true }
    );

    const getPageTempInfo = () => {
      // 获取 页面临时信息，用于保存到LocalStore 中
      return {
        urlName: urlName,
        activeTabIndex: activeTabIndex.value,
        formData: formData,
        model: route.meta.model,
      };
    };
    const $t = inject("t");
    const saveTempToLocalStorage = () => {
      const currentPageInfo = getPageTempInfo();
      const vs = JSON.stringify(currentPageInfo);
      localStorage.setItem("currentPageInfo", vs);
      alert($t("msg.successSaveTempToLocalStorage"));
    };
    const getTempFromLocalStorage = () => {
      let v0 = localStorage.getItem("currentPageInfo");
      if (v0) {
        try {
          let local = JSON.parse(v0);
          // local中的信息是否符合当前页面信息
          if (!local.model === route.meta.model) {
            return false;
          }
          if (urlName === "edit" && !local.formData.sid === formData.sid) {
            return false;
          }
          activeTabIndex.value = local.activeTabIndex;
          Object.assign(formData, local.formData);
        } catch {
          // 全部设置为默认值
          console.log("get Temp info from localstorage出错");
          return false;
        }
      }
    };
    // 将当前页面的 activityIndex 保存到 LocalStorage pages:{} 中
    const saveActiveIndexToLocalStorage = () => {
      let pagesLocal = localStorage.getItem("pages");
      try {
        const pages = JSON.parse(pagesLocal);
        pages[route.path] = activeTabIndex.value;
        localStorage.setItem("pages", JSON.stringify(pages));
      } catch {
        // 全部设置为默认值
        console.log("save Activity Index to localstorage出错");
        return false;
      }
    };
    const getActiveIndexFromLocalStorage = () => {
      // 获取目前的 active index
      if (urlName === "create") {
        return false;
      }
      let pagesLocal = localStorage.getItem("pages");
      if (!pagesLocal) {
        localStorage.setItem("pages", JSON.stringify({}));
      } else {
        const pages = JSON.parse(pagesLocal);
        if (![null, undefined].includes(pages[route.path])) {
          try {
            activeTabIndex.value = pages[route.path];
          } catch {
            // 全部设置为默认值
            console.log("get Activity Index from localstorage出错");
            return false;
          }
        }
      }
    };
    onBeforeRouteUpdate(() => {
      getActiveIndexFromLocalStorage();
    });
    onBeforeRouteLeave(() => {
      saveActiveIndexToLocalStorage();
    });
    return {
      store,
      moment,
      cacheInfo,
      formData,
      urlName,
      activeTabIndex,
      storeLocal,
      tabsFinal,
      saveTempToLocalStorage,
      getTempFromLocalStorage,
    };
  },
});
</script>
