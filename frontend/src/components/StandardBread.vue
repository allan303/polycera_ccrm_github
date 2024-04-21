<template>
  <nav
    style="--bs-breadcrumb-divider: '>'"
    aria-label="breadcrumb"
    v-if="store.getters.isLogin()"
  >
    <ol class="breadcrumb">
      <li class="breadcrumb-item active text-primary" aria-current="page">
        <strong>{{ $t(route.meta.title_root) }}</strong>
      </li>
      <li
        class="breadcrumb-item"
        v-for="(item, index) in itemsNew"
        :key="index"
      >
        <router-link :to="item.route" class="text-dark">
          {{ $t(item.label) }}
        </router-link>
      </li>
      <li class="breadcrumb-item active" aria-current="page">
        {{ $t(route.meta.title) }}
      </li>
    </ol>
  </nav>
</template>

<script scope>
import { defineComponent, inject, watch, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "@/main";
import { can } from "@/myjs";
export default defineComponent({
  props: { items: { type: Array } },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const modelName = route.meta.model;
    // project_oem, project_update 不允许 全部Bread
    const useTotal = !["project_oem", "project_update"].includes(modelName);
    // 创建 默认的 bread
    const locale = inject("locale");
    const createItems = () => {
      if (props.items) {
        return [
          ...props.items,
          // 增加 当前route meta 属性
          // { label: route.meta.title, route: route.path },
        ];
      } else {
        const itemsDefault = [];
        if (can(store.state.cu, modelName, "create")) {
          itemsDefault.push({
            label: "actions.create",
            route: `/${modelName}/create`,
          });
        }
        if (route.meta.hasOwner) {
          itemsDefault.push({
            label: "actions.listMe",
            route: `/${modelName}/list-me`,
          });
          if (route.meta.hasShared) {
            itemsDefault.push({
              label: "actions.listShared",
              route: `/${modelName}/list-shared`,
            });
          }
        }
        if (can(store.state.cu, modelName, "read", "total") && useTotal) {
          itemsDefault.push({
            label: "actions.listTotal",
            route: `/${modelName}/list-total`,
          });
        }
        if (store.state.cu.is_su) {
          itemsDefault.push({
            label: "actions.listDeleted",
            route: `/${modelName}/list-deleted`,
          });
        }
        return itemsDefault;
      }
    };
    const itemsNew = ref(createItems());
    watch(
      () => locale.value,
      () => {
        // console.log(locale.value);
        itemsNew.value = createItems();
      }
    );
    return {
      itemsNew,
      router,
      route,
      store,
    };
  },
});
</script>