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
      <UserListComponent
        listScope="related"
        urlModel="user"
        :filter_dt_and="{ workgroup_sid: formData.sid }"
      ></UserListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script>
import { provide, computed, defineComponent, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";

// 非标
import UserListComponent from "@/views/user/components/ListComponent";

export default defineComponent({
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    FormTextarea,
    FormInput,
    UserListComponent,
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
