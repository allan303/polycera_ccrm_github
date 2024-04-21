<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <template v-slot:tab0>
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

      <FormInput
        v-model="formData.name"
        :label="$t('same.name')"
        :disabled="urlName !== 'create'"
      ></FormInput>

      <FormTextarea
        v-model="formData.remark"
        :label="$t('same.remark')"
        :col="{ md: 12 }"
        :rows="5"
        :disabled="urlName === 'read'"
      ></FormTextarea>
    </template>
    <template v-slot:tab1>
      <PermModel></PermModel>
    </template>
    <template v-slot:tab2 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="user"
        :filter_dt_and="{ role_sid: formData.sid }"
      ></StandardToCreateBtn>
      <UserListComponent
        listScope="related"
        urlModel="user"
        :filter_dt_and="{ role_sid: formData.sid }"
      ></UserListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { computed, provide, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
// import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";
// 非标
import StandardToCreateBtn from "@/components/StandardToCreateBtn";
import UserListComponent from "@/views/user/components/ListComponent";
import PermModel from "./PermModel";
export default {
  props: {
    urlName: { type: String, required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    // FormSelect,
    FormTextarea,
    FormInput,
    UserListComponent,
    StandardToCreateBtn,
    PermModel,
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

    return {
      store,
      moment,
      cacheInfo,
      readUrlDict,
      formData,
    };
  },
};
</script>
