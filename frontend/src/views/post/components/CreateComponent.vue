<template>
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <FormAutoSelect
      :disabled="urlName === 'read'"
      :options="cacheInfo.user"
      :label="$t('same.share_list')"
      v-model="formData.share_list"
      :col="{ md: 12 }"
      mode="multiple"
      :default_content="[{ sid: 'all', name: $t('same.allUser') }]"
    ></FormAutoSelect>
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
      v-model="formData.contact_sid"
      :options="cacheInfo.contact"
      :label="$t('same.related', { v: $t('models.contact') })"
      :disabled="urlName === 'read'"
      textKey="name"
    ></FormAutoSelect>
    <FormAutoSelect
      v-model="formData.order_sid"
      :options="cacheInfo.order"
      :label="$t('same.related', { v: $t('models.order') })"
      :disabled="urlName === 'read'"
    ></FormAutoSelect>
    <FormAutoSelect
      v-model="formData.pilot_sid"
      :options="cacheInfo.pilot"
      :label="$t('same.related', { v: $t('models.pilot') })"
      :disabled="urlName === 'read'"
    ></FormAutoSelect>
    <FormHtml
      :modelValue="formData.body"
      :label="$t('same.content')"
      :col="{ md: 12 }"
      v-if="urlName === 'read'"
    ></FormHtml>
    <FormRichtext
      v-model="formData.body"
      :disabled="urlName === 'read'"
      theme="snow"
      :label="$t('same.content')"
      :col="{ md: 12 }"
      v-if="urlName !== 'read'"
    ></FormRichtext>
  </StandardCreateComponent>
</template>

<script scope>
import { provide, computed, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormRichtext from "@/components/ui/FormRichtext";
import { readUrlDict, createStore } from "./js";
import FormAutoSelect from "@/components/ui/FormAutoSelect";
import FormHtml from "@/components/ui/FormHtml";

export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    FormRichtext,
    FormAutoSelect,
    FormHtml,
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
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
    };
  },
};
</script>
