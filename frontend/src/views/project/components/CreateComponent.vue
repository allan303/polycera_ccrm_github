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
      <FormSelect
        v-model="formData.pjtype"
        :options="cacheInfo.config.pjtype"
        :label="$t('same.type')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormSelect
        v-model="formData.industry"
        :options="cacheInfo.config.industry"
        :label="$t('project.industry')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormAutoSelect
        v-model="formData.location"
        :options="cacheInfo.config.location"
        :label="$t('same.location')"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormSelect
        v-model="formData.source"
        :options="cacheInfo.config.source"
        :label="$t('project.source')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormAutoSelect
        v-model="formData.module"
        :options="cacheInfo.product"
        :label="$t('product.module')"
        :disabled="urlName === 'read'"
        textKey="model"
        valueKey="model"
      ></FormAutoSelect>
      <FormInput
        :modelValue="formData.module_nums"
        :label="$t('same.nums', { v: $t('product.module') })"
        inputType="number"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        :modelValue="formData.forecast_amount_cal"
        :label="$t('project.forecast_amount_cal')"
        inputType="number"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormSelect
        v-model="formData.pjstage"
        :options="cacheInfo.config.pjstage"
        :label="$t('project.pjstage')"
        valueKey="name"
        textKey="name"
        :disabled="urlName !== 'create'"
      ></FormSelect>
      <FormSelect
        v-model="formData.win_percentage"
        :options="cacheInfo.config.pjstage"
        :label="$t('project.win_percentage')"
        valueKey="win_percentage"
        textKey="win_percentage"
        :disabled="urlName !== 'create'"
      ></FormSelect>
      <FormInput
        v-model="formData.forecast_date"
        inputType="date"
        :label="$t('project.forecast_date')"
        :disabled="urlName !== 'create'"
      ></FormInput>
      <FormTextarea
        v-model="formData.filing_summary"
        :label="$t('project.filing_summary')"
        :col="{ md: 12 }"
        :rows="1"
        v-if="urlName === 'read'"
        disabled
      ></FormTextarea>
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
        urlModel="project_oem"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></StandardToCreateBtn>
      <ProjectOemListComponent
        listScope="related"
        urlModel="project_oem"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></ProjectOemListComponent>
    </template>
    <template v-slot:tab2 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="post"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ project_sid: formData.sid }"
      >
      </PostListComponent>
    </template>

    <template v-slot:tab3 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="project_update"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></StandardToCreateBtn>
      <ProjectUpdateListComponent
        listScope="related"
        urlModel="project_update"
        :filter_dt_and="{ project_sid: formData.sid }"
      >
      </ProjectUpdateListComponent>
    </template>

    <template v-slot:tab4 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="pilot"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PilotListComponent
        listScope="related"
        urlModel="pilot"
        :filter_dt_and="{ project_sid: formData.sid }"
      >
      </PilotListComponent>
    </template>
    <template v-slot:tab5 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="design"
        :filter_dt_and="{ project_sid: formData.sid }"
      ></StandardToCreateBtn>
      <desingListComponent
        listScope="related"
        urlModel="design"
        :filter_dt_and="{ project_sid: formData.sid }"
      >
      </desingListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script>
import { provide, computed, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import { readUrlDict, createStore } from "./js";
import FormAutoSelect from "@/components/ui/FormAutoSelect";

// 非标
import StandardToCreateBtn from "@/components/StandardToCreateBtn";
import PostListComponent from "@/views/post/components/ListComponent";
import ProjectOemListComponent from "@/views/project_oem/components/ListComponent";
import ProjectUpdateListComponent from "@/views/project_update/components/ListComponent";
import PilotListComponent from "@/views/pilot/components/ListComponent";
import desingListComponent from "@/views/design/components/ListComponent";
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
    ProjectUpdateListComponent,
    ProjectOemListComponent,
    StandardToCreateBtn,
    PilotListComponent,
    desingListComponent,
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
