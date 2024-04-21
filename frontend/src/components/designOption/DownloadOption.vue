<template>
  <fieldset class="row mt-3" :disabled="urlName !== 'read'">
    <div class="row mb-2">
      <FormSelect
        v-model="formData.tpl_name"
        label="报告模板"
        valueKey="value"
        textKey="name"
        :options="tpl_names"
        :col="{ md: 12 }"
      ></FormSelect>
    </div>
    <FormCheckbox
      v-model="formData.show_bom"
      label="显示设备清单"
    ></FormCheckbox>
    <FormCheckbox
      v-model="formData.show_tree"
      label="显示设备树状图"
    ></FormCheckbox>
    <FormCheckbox
      v-model="formData.show_kw_consumer"
      label="显示能耗"
    ></FormCheckbox>
    <FormCheckbox
      v-model="formData.show_chem_consumer"
      label="显示药剂消耗"
    ></FormCheckbox>
    <FormCheckbox
      v-model="formData.show_time"
      label="显示时间平衡"
    ></FormCheckbox>
    <FormCheckbox v-model="formData.show_cip" label="显示CIP"></FormCheckbox>
    <FormCheckbox v-model="formData.show_ceb" label="显示CEB"></FormCheckbox>
  </fieldset>
</template>
<script scope>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormCheckbox from "@/components/ui/FormCheckbox";
import FormSelect from "@/components/ui/FormSelect";
import { tpl_names } from "./js";
export default defineComponent({
  components: { FormCheckbox, FormSelect },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const formData = storeLocal.state.fd.downloadOption;
    return { storeLocal, formData, store, urlName, tpl_names };
  },
});
</script>