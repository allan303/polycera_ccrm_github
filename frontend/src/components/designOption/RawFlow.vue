<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <FormSelect
      label="原水类型"
      :options="store.state.cacheInfo.config.wwtype"
      textKey="name"
      valueKey="name"
      v-model="formData.wwtype"
    ></FormSelect>
    <FormInput
      label="*水量"
      v-model="formData.q"
      inputType="number"
    ></FormInput>
    <FormSelect
      label="*单位"
      :options="['m3/h', 'm3/d']"
      v-model="formData.q_unit"
    ></FormSelect>
    <FormSelect
      label="*目标"
      :options="[
        { text: '净产水量', value: true },
        { text: '净处理量', value: false },
      ]"
      textKey="text"
      valueKey="value"
      v-model="ops.is_target_perm"
    ></FormSelect>
    <FormInput
      label="*设计工作时间"
      v-model="formData.hpd"
      inputType="number"
    ></FormInput>

    <div class="card mt-3" v-if="formData.concs_dt">
      <div class="card-header text-primary">水质参数</div>
      <div class="card-body">
        <div class="row">
          <FormInput
            label="*设计温度℃"
            v-model="formData.temp"
            inputType="number"
          ></FormInput>
          <FormInput
            label="PH"
            v-model="formData.ph"
            inputType="number"
          ></FormInput>
          <FormInput
            label="COD(mg/L)"
            v-model="formData.concs_dt.cod"
            inputType="number"
          ></FormInput>
          <FormInput
            label="含盐量TDS(mg/L)"
            v-model="formData.concs_dt.tds"
            inputType="number"
          ></FormInput>
          <FormInput
            label="悬浮物SS(mg/L)"
            v-model="formData.concs_dt.ss"
            inputType="number"
          ></FormInput>
          <FormInput
            label="浊度TUB(NTU)"
            v-model="formData.concs_dt.ntu"
            inputType="number"
          ></FormInput>
          <FormInput
            label="油类(mg/L)"
            v-model="formData.concs_dt.oil"
            inputType="number"
          ></FormInput>
        </div>
      </div>
    </div>
    <FormTextarea
      label="原水说明(体现方案中)"
      v-model="formData.remark"
      :col="{ md: 12 }"
      :rows="3"
    ></FormTextarea>
  </fieldset>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import FormSelect from "@/components/ui/FormSelect";
import FormTextarea from "@/components/ui/FormTextarea";
export default defineComponent({
  components: { FormInput, FormTextarea, FormSelect },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const formData = storeLocal.state.fd.options.raw_flow;
    const ops = storeLocal.state.fd.options;
    return { storeLocal, formData, store, urlName, ops };
  },
});
</script>