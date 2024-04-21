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
      <FormInput
        v-model="formData.module_name"
        :label="$t('product.model')"
        disabled
        v-if="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.module_nums"
        :label="$t('same.nums', { v: $t('product.module') + ' ' })"
        disabled
        v-if="urlName === 'read'"
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

    <template v-slot:tab12>
      <DownloadOption v-if="urlName === 'read'"></DownloadOption
    ></template>
    <template v-slot:tab13>
      <Result v-if="urlName === 'read'"></Result>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { computed, provide, inject, onMounted } from "vue";
import { useStore, useAxios } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormInput from "@/components/ui/FormInput";
import FormSelect from "@/components/ui/FormSelect";
import MainBalance from "@/components/designOption/MainBalance";
import Backwash from "@/components/designOption/Backwash";
import Cir from "@/components/designOption/Cir";
import Backflow from "@/components/designOption/Backflow";
import Ceb from "@/components/designOption/Ceb";
import Cip from "@/components/designOption/Cip";
import OtherInfo from "@/components/designOption/OtherInfo";
import RawFlow from "@/components/designOption/RawFlow";
import DownloadOption from "@/components/designOption/DownloadOption";
import PumpsPressure from "@/components/designOption/PumpsPressure";
import Dosing from "@/components/designOption/Dosing";
import Tanks from "@/components/designOption/Tanks";
import Result from "@/components/designOption/Result";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

import { readUrlDict, createStore } from "./js";
import { useRoute } from "vue-router";

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
    DownloadOption,
    PumpsPressure,
    Result,
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
    //考虑来自于标准设计
    const route = useRoute();
    const getStandardDesign = () => {
      const standard_design_sid = route.query.standard_design;
      if (!standard_design_sid) {
        return false;
      }
      const axios = useAxios();
      axios({
        method: "get",
        url: `/standard_design/read/${standard_design_sid}`,
      }).then((res) => {
        const sds_options = res.data.options;
        formData.options = sds_options;
      });
    };
    onMounted(() => {
      getStandardDesign();
    });
    return {
      store,
      moment,
      cacheInfo,
      readUrlDict,
      formData,
      storeLocal,
      route,
    };
  },
};
</script>
