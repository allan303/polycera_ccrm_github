<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <template v-slot:tab0>
      <FormAutoSelect
        :disabled="urlName === 'read'"
        :options="cacheInfo.user"
        :label="$t('same.share_list')"
        v-model="formData.share_list"
        :col="{ md: 12 }"
        mode="multiple"
        :default_content="[{ sid: 'all', name: $t('same.allUser') }]"
      ></FormAutoSelect>
      <FormInput
        :modelValue="
          moment(formData.create_time_local).format('YYYY-MM-D HH:MM')
        "
        :label="$t('same.create_time')"
        v-if="urlName !== 'create'"
        disabled
      ></FormInput>
      <FormInput
        :modelValue="
          moment(formData.update_time_local).format('YYYY-MM-D HH:MM')
        "
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
      <FormInput
        v-model="formData.name"
        :label="$t('same.name')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormAutoSelect
        v-model="formData.project_sid"
        :options="cacheInfo.project"
        :label="$t('same.related', { v: $t('models.project') })"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormAutoSelect
        v-model="formData.oem_sid"
        :options="cacheInfo.oem"
        :label="$t('same.related', { v: $t('models.oem') })"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormAutoSelect
        v-model="formData.location"
        :options="cacheInfo.config.location"
        :label="$t('same.location')"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormSelect
        v-model="formData.industry"
        :options="cacheInfo.config.industry"
        :label="$t('project.industry')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormInput
        v-model="formData.start"
        :label="$t('common.start')"
        inputType="date"
        :disabled="urlName === 'read'"
        :useDelete="true"
      ></FormInput>
      <FormInput
        v-model="formData.end"
        :label="$t('common.end')"
        inputType="date"
        :disabled="urlName === 'read'"
        :useDelete="true"
      ></FormInput>
      <FormTextarea
        v-model="formData.remark"
        :label="$t('same.remark')"
        :col="{ md: 12 }"
        :rows="5"
        :disabled="urlName === 'read'"
      ></FormTextarea>
    </template>
    <template v-slot:tab1 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="post"
        :filter_dt_and="{ pilot_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ pilot_sid: formData.sid }"
      ></PostListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { provide, computed, defineComponent, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

// 非标
import PostListComponent from "@/views/post/components/ListComponent";
import StandardToCreateBtn from "@/components/StandardToCreateBtn";

export default defineComponent({
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    FormSelect,
    FormTextarea,
    FormInput,
    PostListComponent,
    StandardToCreateBtn,
    FormAutoSelect,
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
    //注入：将函数 交给 子组件（函数不能用 props）

    // 以下为方法
    return {
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
    };
  },
});
</script>
