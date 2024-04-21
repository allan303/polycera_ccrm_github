<template >
  <!-- 仅md以下可见 -->

  <button
    class="btn d-xs-block d-sm-block d-md-none"
    type="button"
    data-bs-toggle="offcanvas"
    data-bs-target="#myOffcanvas"
    aria-controls="myOffcanvas"
  >
    <!-- 用于切换是否显示 -->
    <i class="bi-grid-fill" style="font-size: 1em"></i>
  </button>

  <div :class="cls" tabindex="-1" id="myOffcanvas" aria-labelledby="sideMenu">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="sideMenu"></h5>
      <button
        type="button"
        class="btn-close text-reset"
        data-bs-dismiss="offcanvas"
        aria-label="Close"
      ></button>
    </div>
    <div class="offcanvas-body small">
      <AppSide></AppSide>
    </div>
  </div>
</template>
<script scope>
import { defineComponent, watch, ref, computed, inject } from "vue";
import { useRoute } from "vue-router";
import AppSide from "./AppSide.vue";
import { useStore } from "@/main";

// import bootstrap from "bootstrap/dist/js/bootstrap.bundle.min.js";

export default defineComponent({
  components: { AppSide },
  setup() {
    const store = useStore();
    // const axios = useAxios();
    const route = useRoute();
    const show = ref("");
    const cls = computed(
      () => `offcanvas offcanvas-start overflow-auto ${show.value}`
    );
    // const updateToken = () => {
    //   //更新token时间及所有信息
    //   axios({
    //     method: "post",
    //     url: `/auth/update_token`,
    //   }).then((res) => {
    //     store.actions.setState(res.data);
    //   });
    // };
    const updateToken = inject("updateToken");
    watch(
      () => route.fullPath,
      () => {
        // var myOffcanvas = document.getElementById("myOffcanvas");
        // myOffcanvas.addEventListener("hidden.bs.offcanvas", function () {
        // });
        // console.log("点击侧边栏");
        // event.preventDefault();
        // console.log("过期时间还剩几分钟", store.getters.isTokenExpired() / 60);
        console.log(
          `还剩下${store.getters.expireRemainMinutes()}分钟token过期`
        );
        if (store.getters.isTokenExpired()) {
          //15分钟时候 更新token
          updateToken();
        }
        console.log("path change");
        show.value = "";
        // var myOffcanvas = document.getElementById("myOffcanvas");
        // var bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
        // console.log(myOffcanvas);
        // bsOffcanvas.hide();
      }
    );
    return { cls };
  },
});
</script>
