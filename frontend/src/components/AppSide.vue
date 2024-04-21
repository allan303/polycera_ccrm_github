<template>
  <div class="flex-shrink-0" style="width: auto">
    <ul class="list-unstyled ps-0">
      <li class="d-grid mb-1">
        <button
          class="btn-toggle align-items-center rounded"
          aria-expanded="true"
          @click="router.push('/')"
        >
          <i class="bi bi-arrow-right-short text-white"></i
          >{{ $t("auth.home") }}
        </button>
      </li>
      <li class="d-grid mb-1" v-for="(item, index) in modelsUser" :key="index">
        <AppSideOneModel :item="item.meta"></AppSideOneModel>
      </li>
      <div v-if="store.state.cu.is_su">
        <li class="border-top my-3"></li>
        <li class="d-grid mb-1" v-for="(item, index) in modelsSu" :key="index">
          <AppSideOneModel :item="item.meta"></AppSideOneModel>
        </li>
      </div>
    </ul>
  </div>
</template>
<script scope>
import { useStore } from "@/main";
import { can } from "@/myjs";
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import AppSideOneModel from "./AppSideOneModel";
export default defineComponent({
  components: { AppSideOneModel },
  setup() {
    const store = useStore();
    const router = useRouter();
    // const modelsCu1 = [
    //   { title: "models.post", model: "post", hasOwner: true },
    //   { title: "models.project", model: "project", hasOwner: true },
    //   { title: "models.oem", model: "oem", hasOwner: true },
    //   { title: "models.contact", model: "contact", hasOwner: true },
    //   { title: "models.order", model: "order", hasOwner: true },
    //   { title: "models.pilot", model: "pilot", hasOwner: true },
    //   { title: "models.design", model: "design", hasOwner: true },
    //   { title: "models.standardDesign", model: "standard_design", hasOwner: true },

    //   {
    //     title: "models.personal",
    //     model: "auth",
    //     sideRoutes: [
    //       {
    //         label: "auth.profile",
    //         id: "myprofile",
    //         route: `/auth/myprofile`,
    //       },
    //       {
    //         label: "auth.changePwd",
    //         id: "change-password",
    //         route: `/auth/change-password`,
    //       },
    //     ],
    //   },
    // ];
    const createModelsList = () => {
      let modelsUser = [];
      let modelsSu = [];
      for (let route of router.options.routes) {
        if (route.meta && route.meta.title) {
          if (can(store.state.cu, route.meta.model) && !route.meta.forSu) {
            modelsUser.push(route);
          } else if (route.meta.forSu) {
            modelsSu.push(route);
          }
        }
      }
      return { modelsUser, modelsSu };
    };

    // const modelsSu = [
    //   { title: "models.projectOem", model: "project_oem" },
    //   { title: "models.projectUpdate", model: "project_update" },
    //   { title: "models.orderUpdate", model: "order_update" },
    //   { title: "models.orderProduct", model: "product" },
    //   { title: "models.designModule", model: "design_module" },
    //   { title: "models.role", model: "role" },
    //   { title: "models.user", model: "user" },
    //   {
    //     title: "models.config",
    //     model: "config",
    //     sideRoutes: [
    //       {
    //         label: "models.config",
    //         id: "config-read",
    //         route: `/config/read`,
    //       },
    //     ],
    //   },
    // ];

    return {
      store,
      ...createModelsList(),
      router,
    };
  },
});
</script>
