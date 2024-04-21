<template>
  <div class="row mt-2">
    <div class="dropdown">
      <button
        class="btn btn-info dropdown-toggle"
        type="button"
        id="dropdownMenuButton1"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ name }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <a class="dropdown-item btn" @click="deleteSelf">删除此配置</a>
        </li>
        <li>
          <a
            class="dropdown-item btn"
            @click="arrayMovePre(cleanList, oneclean_index)"
            >上移</a
          >
        </li>
        <li>
          <a
            class="dropdown-item btn"
            @click="arrayMoveNext(cleanList, oneclean_index)"
            >下移</a
          >
        </li>
      </ul>
    </div>
  </div>
  <fieldset class="row my-2" :disabled="urlName === 'read'">
    <FormInput :label="$t('same.name')" v-model="formData.name"></FormInput>
    <FormInput
      label="周期（天）"
      inputType="number"
      v-model="formData.interval.val"
    ></FormInput>
    <FormInput
      label="操作温度（℃）"
      inputType="number"
      v-model="formData.temp"
    ></FormInput>
  </fieldset>
  <div class="row mt-4">
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
  </div>
  <div class="row">
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
          <ChemDosing
            :chem_dosing_index="index"
            :oneclean_index="oneclean_index"
          ></ChemDosing>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="row mt-2">
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="chem"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        操作流程
      </button>
      <ul class="dropdown-menu" aria-labelledby="chem">
        <li>
          <a class="dropdown-item btn" @click="addProcess">增加操作</a>
        </li>
      </ul>
    </div>
  </div>
  <div class="row">
    <table class="table">
      <thead>
        <tr>
          <th>操作</th>
          <th>时间</th>
          <th>单位</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in formData.process_list" :key="item">
          <!-- 传递 index，并用key=item实现 更新dom -->
          <Process
            :process_index="index"
            :oneclean_index="oneclean_index"
          ></Process>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script scope>
import { inject, defineComponent, computed } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import ChemDosing from "./ChemDosing";
import Process from "./Process";
import { defaultChem, defaultProcess } from "./js";
import { arrayMoveNext, arrayMovePre } from "@/myjs";

export default defineComponent({
  props: { oneclean_index: { required: true, type: Number } },
  components: { FormInput, ChemDosing, Process },
  setup(props) {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const cleanName = inject("cleanName");
    // 获取 formData
    const Clean = storeLocal.state.fd.options[cleanName];
    const cleanList = Clean.oneclean_list;
    const formData = cleanList[props.oneclean_index]; //本页数据
    const deleteSelf = () => {
      cleanList.splice(props.oneclean_index, 1);
    };
    const name = computed(() => {
      return `${cleanName.toUpperCase()}-${props.oneclean_index + 1}: ${
        formData.name
      }`;
    });
    const addChem = () => {
      formData.chem_dosings.push(defaultChem());
    };
    const addProcess = () => {
      formData.process_list.push(defaultProcess());
    };
    return {
      storeLocal,
      cleanList,
      formData,
      store,
      urlName,
      deleteSelf,
      name,
      addProcess,
      addChem,
      arrayMoveNext,
      arrayMovePre,
    };
  },
});
</script>