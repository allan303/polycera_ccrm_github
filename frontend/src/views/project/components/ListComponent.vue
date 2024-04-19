<template>
  <StandardListComponent
    :listScope="listScope"
    :urlModel="urlModel"
    :filter_dt_and="filter_dt_and"
    ref="child"
  >
    <div class="row">
      <div :class="cls" v-for="(obj, index) in child.objs" :key="index">
        <ListItemOne :formData="obj" :urlModel="urlModel"></ListItemOne>
      </div>
    </div>
  </StandardListComponent>
</template>

<script>
import StandardListComponent from "@/components/StandardListComponent";
import ListItemOne from "./ListItemOne";
import { computed, ref } from "vue";
import { useStore } from "@/main";
export default {
  components: { StandardListComponent, ListItemOne },
  props: {
    listScope: { required: true, type: String },
    urlModel: { type: String, default: null },
    filter_dt_and: { type: Object, default: null },
  },
  setup() {
    //从子组件获取 objs, 获取的值为  child setup return 的值
    //异步获取，结构先保证 渲染不出问题
    const child = ref({ value: {} });
    const store = useStore();
    const cls = computed(() =>
      store.state.local.use_half ? "col-lg-6 mb-2" : "col-12 mb-2"
    );
    return { child, cls };
  },
};
</script>
