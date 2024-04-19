<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <FormInput
      v-model="formData.name"
      :label="$t('same.name')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.brand"
      :label="$t('product.brand')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.model"
      :label="$t('product.model')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormSelect
      v-model="formData.membrane_type"
      :label="$t('product.membrane_type')"
      :options="membrane_types"
      valueKey="value"
      textKey="text"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormSelect
      v-model="formData.module_type"
      :label="$t('product.module_type')"
      :options="module_types"
      valueKey="value"
      textKey="text"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormInput
      v-model="formData.material"
      :label="$t('product.material')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.fa"
      :label="$t('product.fa') + '(m2)'"
      inputType="number"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.flux_per_bar_25"
      :label="$t('product.flux_per_bar_25') + '(LMH/Bar@25℃)'"
      inputType="number"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.liter_inside"
      :label="$t('product.liter_inside') + '(L)'"
      inputType="number"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormSelect
      v-model="formData.is_contained_pv"
      :label="$t('product.is_contained_pv')"
      :options="[
        { text: $t('product.noPv'), value: false },
        { text: $t('product.withPv'), value: true },
      ]"
      valueKey="value"
      textKey="text"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormInput
      v-model="formData.spacer_mil"
      :label="$t('product.spacer_mil') + '(' + $t('product.onlySpiral') + ')'"
      inputType="number"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormSelect
      v-model="formData.module_size"
      :label="$t('product.module_size') + '(' + $t('product.onlySpiral') + ')'"
      :options="sizes"
      valueKey="value"
      textKey="text"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormTextarea
      v-model="formData.description"
      :label="$t('same.description')"
      :col="{ md: 12 }"
      :rows="5"
      :disabled="urlName === 'read'"
    ></FormTextarea>
  </StandardCreateComponent>
</template>

<script>
import { provide, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import {
  readUrlDict,
  createStore,
  membrane_types,
  module_types,
  sizes,
} from "./js";

export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: { StandardCreateComponent, FormSelect, FormTextarea, FormInput },
  setup(props) {
    const storeLocal = createStore();
    //注入 createComponent 所有子组件
    provide("storeLocal", storeLocal);
    const formData = storeLocal.state.fd;
    //此item限定条件
    provide("urlName", props.urlName);
    const moment = inject("moment");
    const store = useStore();
    return {
      formData,
      store,
      moment,
      readUrlDict,
      membrane_types,
      module_types,
      sizes,
    };
  },
};
</script>
