<template>
  <div class="row mb-2">
    <StandardBread :items="items"></StandardBread>
  </div>
  <div class="row mb-2">
    <div class="col-12">
      <!-- slot用于插入一些只需要点击的功能 -->
      <slot></slot>
    </div>
  </div>
  <div class="row mb-2" v-if="useSearch">
    <div class="col-12">
      <div class="input-group">
        <MyAutoSelect
          :options="cache"
          :placeholder="placeholder"
          :textKey="textKey"
          :valueKey="valueKey"
          v-model="sid"
        ></MyAutoSelect>
        <span class="input-group-text btn btn-primary" @click="goRead">
          {{ $t("actions.goTo") }}
        </span>
      </div>
    </div>
  </div>
  <div class="row mb-2">
    <div class="col-12">
      <router-view :key="dt"></router-view>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, inject, provide, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "@/main";
import StandardBread from "@/components/StandardBread";
import MyAutoSelect from "@/components/ui/MyAutoSelect.vue";
export default defineComponent({
  // const items = [
  //     { label: "我的档案", route: "/auth/myprofile" },
  //     { label: "修改密码", route: "/auth/change-password" },
  // ];
  props: {
    items: { type: Array },
    textKey: { default: "name" },
    valueKey: { default: "sid" },
    useSearch: { type: Boolean, default: true },
  },
  components: { StandardBread, MyAutoSelect },
  setup() {
    provide("storeLocal", null);
    const sid = ref(null);
    const route = useRoute();
    const model = route.meta.model;
    const router = useRouter();
    const store = useStore();
    const $t = inject("t");
    const cache = computed(() => {
      // 用于查重
      const model = route.meta.model;
      return store.state.cacheInfo[model] || [{ name: "t", sid: "v" }];
    });
    const placeholder = computed(
      //重名查询 placeholder
      () => `${$t(route.meta.title_root)} ${$t("common.duplication")}...`
    );
    const dt = String(new Date());
    const goRead = () => {
      //选择后 跳转
      if (!sid.value) {
        return false;
      }
      router.push(`/${model}/read/${sid.value}`);
    };
    return { dt, cache, placeholder, sid, goRead, model };
  },
});
</script>