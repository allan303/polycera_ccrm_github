<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <FormAutoSelect
      v-model="md.brand"
      label="*膜元件品牌"
      :options="brand_options"
      :disabled="urlName === 'read'"
      :col="{ md: 12 }"
    ></FormAutoSelect>
    <FormAutoSelect
      v-model="md.model"
      label="*膜元件"
      :options="module_options"
      :disabled="urlName === 'read'"
      :col="{ md: 12 }"
    ></FormAutoSelect>
    <FormInput
      label="组件形式"
      :modelValue="selectedModule.module_type"
      disabled
    ></FormInput>
    <FormInput
      label="膜面积m2"
      :modelValue="selectedModule.fa"
      disabled
    ></FormInput>
    <FormSelect
      label="含膜壳"
      :modelValue="selectedModule.is_contained_pv"
      valueKey="value"
      textKey="text"
      :options="[
        { text: '含膜壳', value: true },
        { text: '不含膜壳', value: false },
      ]"
      disabled
    ></FormSelect>
    <FormInput
      label="*系列运行数量"
      v-model="formData.serie_nums"
      inputType="number"
    ></FormInput>
    <FormInput
      label="系列备用数量"
      v-model="formData.serie_nums_backup"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*组/系列(即一台供水泵对几组)"
      v-model="formData.group_nums_per_serie"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*串联长度(卷式即几芯膜壳)"
      v-model="formData.module_nums_per_train"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*设计通量LMH"
      v-model="formData.lmh_design"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*设计运行回收率%"
      v-model="formData.rec_operate"
      inputType="number"
    ></FormInput>
    <FormSelect
      v-model="formData.install"
      label="安装方式"
      :options="['立式', '卧式']"
    ></FormSelect>
  </fieldset>
</template>
<script scope>
import { inject, defineComponent, computed, watch } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import FormSelect from "@/components/ui/FormSelect";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

export default defineComponent({
  components: { FormInput, FormSelect, FormAutoSelect },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const options = storeLocal.state.fd.options;
    const formData = options.main_balance;
    const md = storeLocal.state.fd.options.module;
    const raw_options = store.state.cacheInfo.design_module;
    //现有 品牌选项
    const brand_options = computed(() => {
      let ls = [];
      for (let x of raw_options) {
        ls.push(x.brand);
      }
      let newset = new Set(ls);
      return Array.from(newset);
    });
    const module_options = computed(() => {
      let ls = [];
      for (let x of raw_options) {
        if (String(x.brand).toLowerCase() === String(md.brand).toLowerCase()) {
          ls.push(x.model);
        }
      }
      return ls;
    });
    const selectedModule = computed(() => {
      for (let x of raw_options) {
        if (x.model === md.model && x.brand === md.brand) {
          return x;
        }
      }
      return {};
    });
    watch(
      () => md.brand,
      (oldvalue, newvalue) => {
        if (oldvalue !== newvalue) {
          md.model = null;
        }
      }
    );
    return {
      storeLocal,
      formData,
      store,
      md,
      urlName,
      selectedModule,
      brand_options,
      module_options,
    };
  },
});
</script>