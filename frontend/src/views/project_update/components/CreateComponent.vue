<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <FormInput
      :modelValue="moment(formData.create_time_local).format('YYYY-MM-D HH:MM')"
      :label="$t('same.create_time')"
      v-if="urlName !== 'create'"
      disabled
    ></FormInput>
    <FormInput
      :modelValue="moment(formData.update_time_local).format('YYYY-MM-D HH:MM')"
      :label="$t('same.update_time')"
      v-if="urlName !== 'create'"
      disabled
    ></FormInput>
    <FormSelect
      :modelValue="formData.owner_sid"
      :label="$t('same.owner')"
      :options="cacheInfo.user"
      disabled
      v-if="urlName !== 'create'"
    ></FormSelect>
    <FormSelect
      v-model="formData.project_sid"
      :options="cacheInfo.project"
      :label="$t('same.name')"
      disabled
    ></FormSelect>
    <FormSelect
      v-model="formData.pjstage"
      :options="cacheInfo.config.pjstage"
      :label="$t('project.pjstage')"
      valueKey="name"
      textKey="name"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormSelect
      v-model="formData.win_percentage"
      :options="cacheInfo.config.pjstage"
      :label="$t('project.win_percentage')"
      valueKey="win_percentage"
      textKey="win_percentage"
      :disabled="urlName === 'read'"
    ></FormSelect>
    <FormInput
      v-model="formData.forecast_date"
      inputType="date"
      :label="$t('project.forecast_date')"
      :disabled="urlName === 'read'"
    ></FormInput>

    <FormTextarea
      v-model="formData.remark"
      :label="$t('same.remark')"
      :col="{ md: 12 }"
      :rows="5"
      :disabled="urlName === 'read'"
    ></FormTextarea>
  </StandardCreateComponent>
</template>

<script scope>
import { provide, computed, watch, inject } from "vue";
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
  components: {
    StandardCreateComponent,
    FormSelect,
    FormTextarea,
    FormInput,
  },
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

    // 以下为方法

    const selectedPjstage = computed(() => {
      //pjstage win_percentage 联动
      // if (!cacheInfo.value.config.pjstage) {
      //   return {};
      // }
      for (let item of cacheInfo.value.config.pjstage) {
        if (formData.pjstage === item.name) {
          return item;
        }
      }
      return {};
    });
    watch(
      () => formData.pjstage,
      () => {
        formData.win_percentage = selectedPjstage.value.win_percentage;
      }
    );
    return {
      store,
      moment,
      cacheInfo,
      readUrlDict,
      selectedPjstage,
      formData,
    };
  },
};
</script>
