<template>
  <div class="row mt-3">
    <div class="col-md-6" v-if="urlName !== 'read'">
      <!-- 新增权限dropdown -->
      <div class="dropdown">
        <button
          class="btn btn-primary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi-plus-lg"></i>
          {{ $t("actions.add") }}
        </button>

        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li v-for="(item, index) in permModelsFilter" :key="index">
            <button class="dropdown-item" @click="addPermModel(item.value)">
              {{ item.text }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <!-- 筛选框 -->
    <div class="col-md-6">
      <div class="input-group mb-3">
        <span class="input-group-text" id="basic-addon1">{{
          $t("common.filter")
        }}</span>
        <MyAutoSelect
          v-model="search"
          :options="existPermModelsFilter"
          valueKey="value"
          textKey="text"
        >
        </MyAutoSelect>
      </div>
    </div>
  </div>
  <!-- 展示card -->
  <div class="row">
    <div :class="cls" v-for="(v, k) in permFilter" :key="k">
      <PermAction :permModel="k"></PermAction>
    </div>
  </div>
</template>
<script scope>
import { computed, defineComponent, ref, inject } from "vue";
import PermAction from "./PermAction.vue";
import { useStore } from "@/main";
import { defaultPermModel } from "./js";
import MyAutoSelect from "@/components/ui/MyAutoSelect";
export default defineComponent({
  components: { PermAction, MyAutoSelect },
  setup() {
    const store = useStore();
    const permOption = store.state.perm_option;
    const storeLocal = inject("storeLocal");
    const perm = storeLocal.state.fd.perm;
    const search = ref("");
    const urlName = inject("urlName");
    //computed
    const cls = computed(() =>
      store.state.local.use_half ? "col-lg-6 mb-2" : "col-12 mb-2"
    );
    const permFilter = computed(() => {
      const p = Object.assign({}, perm);
      delete p["auth"];
      if (!search.value) {
        return p;
      } else {
        for (let k in p) {
          if (k !== search.value) {
            delete p[k];
          }
        }
        return p;
      }
    });
    const options = computed(() => {
      return Object.keys(permFilter.value);
    });
    const permModelsFilter = computed(() => {
      //新增权限 去掉已存在
      const ls = permOption.models;
      const ls1 = [];
      for (let x of ls) {
        if (!perm[x.value]) {
          ls1.push(x);
        }
      }
      return ls1;
    });

    const existPermModelsFilter = computed(() => {
      //此用户具备的权限模块，用于显示筛选
      const ls = permOption.models;
      const ls1 = [];
      for (let x of ls) {
        //perm['project'] !==null
        if (typeof perm[x.value] === "object") {
          ls1.push(x);
        }
      }
      return ls1;
    });

    const addPermModel = (key) => {
      perm[key] = defaultPermModel();
    };
    //watch
    return {
      permFilter,
      addPermModel,
      permModelsFilter,
      urlName,
      cls,
      search,
      options,
      perm,
      permOption,
      existPermModelsFilter,
    };
  },
});
</script>