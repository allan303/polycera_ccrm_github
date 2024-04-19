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
        v-model="formData.name"
        :label="$t('user.name')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.name_en"
        :label="$t('user.name_en')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.username"
        :label="$t('user.username')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormSelect
        v-model="formData.gender"
        :options="['male', 'female']"
        :label="$t('user.gender')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormSelect
        v-model="formData.role_sid"
        :options="cacheInfo.role"
        :label="$t('models.role')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormSelect
        v-model="formData.workgroup_sid"
        :options="cacheInfo.workgroup"
        :label="$t('models.workgroup')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormInput
        v-model="formData.email"
        :label="$t('user.email')"
        :disabled="urlName !== 'create'"
      ></FormInput>
      <FormInput
        v-model="formData.phone"
        :label="$t('user.phone')"
        :disabled="urlName !== 'create'"
      ></FormInput>

      <FormInput
        v-model="formData.company"
        :label="$t('user.company')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.title"
        :label="$t('user.title')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-model="formData.country"
        :label="$t('user.country')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormSelect
        v-model="formData.province"
        :options="cacheInfo.config.location"
        :label="$t('same.location')"
        :disabled="urlName === 'read'"
      ></FormSelect>
      <FormTextarea
        v-model="formData.remark"
        :label="$t('same.remark')"
        :col="{ md: 12 }"
        :rows="5"
        :disabled="urlName === 'read'"
      ></FormTextarea>
      <div class="border-top my-3"></div>
      <h6 class="mb-3 text-primary">{{ $t("user.user_config") }}</h6>
      <FormSelect
        v-model="formData.user_config.locale"
        :label="$t('user.locale')"
        :options="['zh', 'en']"
      ></FormSelect>
      <FormSelect
        v-model="formData.user_config.use_half"
        :label="$t('user.display')"
        :options="[
          { text: $t('auth.displayNormal'), value: false },
          { text: $t('auth.displayTwoCols'), value: true },
        ]"
        textKey="text"
        valueKey="value"
      ></FormSelect>
    </template>
    <template v-slot:tab1 v-if="urlName === 'read'">
      <ProjectListComponent
        listScope="related"
        urlModel="project"
        :filter_dt_and="{ owner_sid: formData.sid }"
      ></ProjectListComponent>
    </template>

    <template v-slot:tab2 v-if="urlName === 'read'">
      <OemListComponent
        listScope="related"
        urlModel="oem"
        :filter_dt_and="{ owner_sid: formData.sid }"
      >
      </OemListComponent>
    </template>

    <template v-slot:tab3 v-if="urlName === 'read'">
      <ContactListComponent
        listScope="related"
        urlModel="contact"
        :filter_dt_and="{ owner_sid: formData.sid }"
      >
      </ContactListComponent>
    </template>
    <template v-slot:tab4 v-if="urlName === 'read'">
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ owner_sid: formData.sid }"
      >
      </PostListComponent>
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
// 非标
import ProjectListComponent from "@/views/project/components/ListComponent";
import OemListComponent from "@/views/oem/components/ListComponent";
import ContactListComponent from "@/views/contact/components/ListComponent";
import PostListComponent from "@/views/post/components/ListComponent";

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
    OemListComponent,
    ProjectListComponent,
    ContactListComponent,
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
      store,
      moment,
      cacheInfo,
      readUrlDict,
      formData,
    };
  },
};
</script>
