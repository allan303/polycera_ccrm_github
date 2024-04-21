<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <div class="col-md-6">
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          v-model="formData.is_use"
          id="is_use"
        />
        <label class="form-check-label" for="is_use"> 启用运行连续加药 </label>
      </div>
    </div>
  </fieldset>
  <div class="row mt-4" v-if="formData.is_use">
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="chem"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        药剂
      </button>
      <ul class="dropdown-menu" aria-labelledby="chem">
        <li>
          <a class="dropdown-item btn" @click="addChem">增加药剂</a>
        </li>
      </ul>
    </div>
    <fieldset class="row mt-3" :disabled="urlName === 'read'">
      <table class="table">
        <thead>
          <tr>
            <th>化学品名称</th>
            <th>原液浓度 wt%</th>
            <th>加药浓度 wt%</th>
            <th>单价rmb/kg</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in formData.chem_dosings" :key="item">
            <!-- 传递 index，并用key=item实现 更新dom -->
            <ChemDosingForDosing
              :chem_dosing_index="index"
            ></ChemDosingForDosing>
          </tr>
        </tbody>
      </table>
    </fieldset>
  </div>
</template>
<script scope>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import ChemDosingForDosing from "./ChemDosingForDosing";
import { defaultChem } from "./js";
import { arrayMoveNext, arrayMovePre } from "@/myjs";

export default defineComponent({
  components: { ChemDosingForDosing },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    // 获取 formData
    const options = storeLocal.state.fd.options;
    const formData = options.dosing;

    const addChem = () => {
      formData.chem_dosings.push(defaultChem());
    };

    return {
      storeLocal,
      formData,
      store,
      urlName,
      addChem,
      arrayMoveNext,
      arrayMovePre,
    };
  },
});
</script>