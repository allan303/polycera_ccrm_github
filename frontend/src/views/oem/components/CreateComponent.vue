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
        :label="$t('same.name', { v: $t('models.oem') + ' ' })"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormAutoSelect
        v-model="formData.location"
        :options="cacheInfo.config.location"
        :label="$t('same.location')"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormSelect
        v-model="formData.oemtype"
        :options="cacheInfo.config.oemtype"
        :label="$t('same.type')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormInput
        v-model="formData.company_code"
        :label="$t('oem.company_code')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.company_bank_account"
        :label="$t('oem.company_bank_account')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.company_bank"
        :label="$t('oem.company_bank')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.company_address"
        :label="$t('oem.company_address')"
        :col="{ md: 12 }"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.company_telephone"
        :label="$t('oem.company_telephone')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.company_zipcode"
        :label="$t('oem.company_zipcode')"
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
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></PostListComponent>
    </template>
    <template v-slot:tab2 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="contact"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></StandardToCreateBtn>
      <ContactListComponent
        listScope="related"
        urlModel="contact"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></ContactListComponent>
    </template>
    <template v-slot:tab3 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="project_oem"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></StandardToCreateBtn>
      <ProjectOemListComponent
        listScope="related"
        urlModel="project_oem"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></ProjectOemListComponent>
    </template>
    <template v-slot:tab4 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="order"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></StandardToCreateBtn>
      <OrderListComponent
        listScope="related"
        urlModel="order"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></OrderListComponent>
    </template>
    <template v-slot:tab5 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="design"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></StandardToCreateBtn>
      <DesignListComponent
        listScope="related"
        urlModel="design"
        :filter_dt_and="{ oem_sid: formData.sid }"
      ></DesignListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { provide, computed, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

import { readUrlDict, createStore } from "./js";

// 非标
import PostListComponent from "@/views/post/components/ListComponent";
import ContactListComponent from "@/views/contact/components/ListComponent";
import ProjectOemListComponent from "@/views/project_oem/components/ListComponent";
import OrderListComponent from "@/views/order/components/ListComponent";
import DesignListComponent from "@/views/design/components/ListComponent";
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
    ContactListComponent,
    StandardToCreateBtn,
    ProjectOemListComponent,
    OrderListComponent,
    FormAutoSelect,
    DesignListComponent,
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
