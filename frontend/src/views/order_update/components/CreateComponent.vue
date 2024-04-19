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
    <!-- 订单不能手动修改 -->
    <FormSelect
      v-model="formData.order_sid"
      :options="cacheInfo.order"
      :label="$t('models.order')"
      disabled
    ></FormSelect>
    <FormSelect
      v-model="formData.status"
      :options="cacheInfo.config.order_status"
      :label="$t('order.status')"
      :disabled="urlName === 'read'"
    ></FormSelect>
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
import { provide, computed, defineComponent, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";

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
