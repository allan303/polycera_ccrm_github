<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <FormInput
      v-model="formData.name"
      :label="$t('same.name')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.model"
      :label="$t('product.model')"
      :disabled="urlName === 'read'"
    ></FormInput>
    <FormInput
      v-model="formData.unit_price"
      :label="$t('same.unit_price') + '(RMB)'"
      :disabled="urlName === 'read'"
      inputType="number"
    ></FormInput>
    <FormSelect
      v-model="formData.unit"
      :options="cacheInfo.config.product_units"
      :label="$t('same.unit')"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormTextarea
      v-model="formData.description"
      :label="$t('same.description')"
      :col="{ md: 12 }"
      :rows="3"
      :disabled="urlName === 'read'"
    ></FormTextarea>
    <FormTextarea
      v-model="formData.remark"
      :label="$t('same.remark') + '(Only Inside)'"
      :col="{ md: 12 }"
      :rows="5"
      :disabled="urlName === 'read'"
    ></FormTextarea>
  </StandardCreateComponent>
</template>

<script>
import { provide, computed, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";

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
    const cacheInfo = computed(() => store.state.cacheInfo);

    return {
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
    };
  },
};
</script>
