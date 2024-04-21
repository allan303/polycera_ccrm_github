<template>
  <button
    class="btn-toggle align-items-center rounded collapsed"
    data-bs-toggle="collapse"
    :data-bs-target="`#${id}`"
    aria-expanded="true"
  >
    <i class="bi bi-chevron-right"></i> {{ $t(item.title) }}
  </button>
  <div class="collapse" :id="id">
    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
      <li
        v-for="(item, index) in sideMenuChildItems"
        :key="index"
        class="d-grid"
      >
        <a @click="router.push(item.route)" class="link-dark btn btn-link">{{
          $t(item.label)
        }}</a>
      </li>
      <!-- <li class="d-grid">
        <a @click="router.push(item.route)" class="link-dark btn btn-link">{{
          $t("role.saveToJson")
        }}</a>
      </li> -->
    </ul>
  </div>
</template>
<script scope>
import { useStore } from "@/main";
import { computed, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { can } from "@/myjs";
export default defineComponent({
  props: {
    //item  = route.meta
    item: { type: Object },
  },
  setup(props) {
    const id = props.item.model + Math.random().toString(36).slice(-8);
    const store = useStore();
    const router = useRouter();
    const perm = store.state.cu.perm;
    const defaultItems = [];
    const setDefaultItems = () => {
      if (can(store.state.cu, props.item.model, "create")) {
        defaultItems.push({
          label: "actions.create",
          id: "create",
          route: `/${props.item.model}/create`,
        });
      }
      // 没有 Owner的模块 不需要
      if (props.item.hasOwner) {
        defaultItems.push({
          label: "actions.listMe",
          id: "list-me",
          route: `/${props.item.model}/list-me`,
        });
        if (props.item.hasShared) {
          defaultItems.push({
            label: "actions.listShared",
            id: "list-shared",
            route: `/${props.item.model}/list-shared`,
          });
        }
      }
      // can(cu, model, action, scope, ownerSid)
      if (can(store.state.cu, props.item.model, "read", "total")) {
        defaultItems.push({
          label: "actions.listTotal",
          id: "list-total",
          route: `/${props.item.model}/list-total`,
        });
      }
      if (store.state.cu.is_su) {
        defaultItems.push({
          label: "actions.listDeleted",
          id: "list-deleted",
          route: `/${props.item.model}/list-deleted`,
        });
        if (props.item.model === "contact") {
          defaultItems.push({
            label: "common.excelFile",
            id: "insertByExcel",
            route: `/${props.item.model}/insert-by-excel`,
          });
        }
      }
      // if (can(store.state.cu, props.item.model, "dashboard", "me")) {
      //   defaultItems.push({
      //     label: "我的数据",
      //     id: "chart-me",
      //     route: `/${props.item.model}/chart-me`,
      //   });
      // }
    };
    //生成 默认
    setDefaultItems();
    const sideMenuChildItems = computed(() => {
      let arr = defaultItems;
      if (props.item.sideRoutes) {
        arr = props.item.sideRoutes;
      }
      const ls = [];
      for (let ar of arr) {
        if (ar.id === "list-total") {
          //仅限 具有 read-total权限的人
          //can(cu, model, action, scope, ownerSid)
          if (can(store.state.cu, props.item.model, "read", "total")) {
            ls.push(ar);
          }
        } else if (ar.id == "list-deleted") {
          //仅限管理员
          if (store.state.cu.is_su) {
            ls.push(ar);
          }
        } else {
          ls.push(ar);
        }
      }
      return ls;
    });
    return {
      store,
      sideMenuChildItems,
      perm,
      id,
      router,
    };
  },
});
</script>
<style scoped>
.collapsible-header {
  padding: 10px;
}
.collapsible-body {
  padding: 0px;
}
</style>