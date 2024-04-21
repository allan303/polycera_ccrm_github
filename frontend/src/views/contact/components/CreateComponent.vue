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
      <div class="row mt-2">
        <FormCheckbox
          v-model="useNewOem"
          :label="$t('contact.newOem')"
          v-if="urlName === 'create'"
        ></FormCheckbox>
      </div>
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
        :label="$t('contact.name')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormAutoSelect
        v-model="formData.oem_sid"
        :options="cacheInfo.oem"
        :label="$t('user.company')"
        :disabled="urlName === 'read'"
        v-if="!useNewOem"
      ></FormAutoSelect>
      <FormInput
        v-model="formData.new_oemname"
        :label="$t('oem.name')"
        v-if="urlName === 'create' && useNewOem"
      ></FormInput>
      <FormSelect
        v-model="formData.new_oemtype"
        :options="cacheInfo.config.oemtype"
        :label="$t('same.type')"
        v-if="urlName === 'create' && useNewOem"
      ></FormSelect>
      <FormInput
        v-model="formData.department"
        :label="$t('contact.department')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.title"
        :label="$t('user.title')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.phone"
        :label="$t('user.phone')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.email"
        :label="$t('user.email')"
        :disabled="urlName === 'read'"
      ></FormInput>

      <FormInput
        v-model="formData.company_zipcode"
        :label="$t('contact.zip_code')"
        :disabled="urlName === 'read'"
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
        :filter_dt_and="{ contact_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ contact_sid: formData.sid }"
      ></PostListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { computed, inject, provide, ref } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";
import FormAutoSelect from "@/components/ui/FormAutoSelect";
import FormCheckbox from "@/components/ui/FormCheckbox";

// 非标
import PostListComponent from "@/views/post/components/ListComponent";
import StandardToCreateBtn from "@/components/StandardToCreateBtn";
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
    PostListComponent,
    StandardToCreateBtn,
    FormAutoSelect,
    FormCheckbox,
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
    const useNewOem = ref(false);
    // 以下为方法

    return {
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
      useNewOem,
    };
  },
};
</script>
