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

    <FormAutoSelect
      v-model="formData.project_sid"
      :options="cacheInfo.project"
      :label="$t('models.project')"
      :disabled="urlName === 'read'"
    ></FormAutoSelect>
    <FormAutoSelect
      v-model="formData.oem_sid"
      :options="cacheInfo.oem"
      :label="$t('models.oem')"
      :disabled="urlName === 'read'"
    ></FormAutoSelect>
    <FormInput
      v-model="formData.is_filing"
      :label="$t('project.is_filing')"
      :disabled="urlName === 'read'"
      inputType="checkbox"
      rawClass="form-check-input"
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

<script>
import { provide, computed, watch, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormAutoSelect from "@/components/ui/FormAutoSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";

export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    FormAutoSelect,
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
        if (["", null, undefined].includes(formData.win_percentage)) {
          formData.win_percentage = selectedPjstage.value.win_percentage;
        }
      }
    );
    return {
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
      selectedPjstage,
    };
  },
};
</script>
