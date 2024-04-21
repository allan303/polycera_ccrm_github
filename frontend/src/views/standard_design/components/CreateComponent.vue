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
        :col="{ md: 12 }"
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
    <template v-slot:tab1> <RawFlow></RawFlow></template>
    <template v-slot:tab2><OtherInfo></OtherInfo> </template>
    <template v-slot:tab3><MainBalance></MainBalance> </template>
    <template v-slot:tab4> <Backwash></Backwash> </template>
    <template v-slot:tab5><Cir></Cir> </template>
    <template v-slot:tab6><Backflow></Backflow> </template>
    <template v-slot:tab7><Ceb></Ceb></template>
    <template v-slot:tab8> <Cip></Cip></template>
    <template v-slot:tab9> <PumpsPressure></PumpsPressure></template>
    <template v-slot:tab10> <Dosing></Dosing></template>
    <template v-slot:tab11> <Tanks></Tanks></template>
  </StandardCreateComponent>
</template>

<script scope>
import { computed, provide, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormInput from "@/components/ui/FormInput";
import MainBalance from "@/components/designOption/MainBalance";
import Backwash from "@/components/designOption/Backwash";
import Cir from "@/components/designOption/Cir";
import Backflow from "@/components/designOption/Backflow";
import Ceb from "@/components/designOption/Ceb";
import Cip from "@/components/designOption/Cip";
import OtherInfo from "@/components/designOption/OtherInfo";
import RawFlow from "@/components/designOption/RawFlow";
import PumpsPressure from "@/components/designOption/PumpsPressure";
import Dosing from "@/components/designOption/Dosing";
import Tanks from "@/components/designOption/Tanks";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

import { readUrlDict, createStore } from "./js";

export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    // FormSelect,
    FormTextarea,
    FormInput,
    MainBalance,
    Backwash,
    OtherInfo,
    Cir,
    Ceb,
    Cip,
    Backflow,
    RawFlow,
    Dosing,
    Tanks,
    PumpsPressure,
    FormAutoSelect,
  },
  setup(props) {
    const storeLocal = createStore();
    //注入 createComponent 所有子组件
    provide("storeLocal", storeLocal);
    const formData = storeLocal.state.fd;
    formData.options.raw_flow.q = 100;
    //此item限定条件
    provide("urlName", props.urlName);
    const moment = inject("moment");
    const store = useStore();
    const cacheInfo = computed(() => store.state.cacheInfo);
    //注入：将函数 交给 子组件（函数不能用 props）
    return {
      store,
      moment,
      cacheInfo,
      readUrlDict,
      formData,
      storeLocal,
    };
  },
};
</script>
