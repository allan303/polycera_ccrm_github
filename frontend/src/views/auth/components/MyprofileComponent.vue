<template>
  <div class="row justify-content-center">
    <form class="row">
      <fieldset class="row" :disabled="!isEdit">
        <FormInput
          v-model="last_seen_local_str"
          :label="$t('user.last_seen')"
          :disabled="true"
        ></FormInput>
        <FormInput
          v-model="formData.name"
          :label="$t('user.name')"
          :disabled="true"
        ></FormInput>
        <FormInput
          v-model="formData.name_en"
          :label="$t('user.name_en')"
          :disabled="urlName === 'read'"
        ></FormInput>
        <FormInput
          v-model="formData.email"
          :label="$t('user.email')"
          disabled
        ></FormInput>
        <FormInput
          v-model="formData.phone"
          :label="$t('user.phone')"
          :disabled="true"
        ></FormInput>
        <FormSelect
          v-model="formData.role_sid"
          :label="$t('models.role')"
          disabled
          :options="cacheInfo.role"
        ></FormSelect>
        <FormSelect
          v-model="formData.workgroup_sid"
          :options="cacheInfo.workgroup"
          :label="$t('models.workgroup')"
          disabled
        ></FormSelect>
        <FormInput
          v-model="formData.username"
          :label="$t('user.username')"
          :disabled="true"
        ></FormInput>
        <FormSelect
          v-model="formData.gender"
          :options="['male', 'female']"
          :label="$t('user.gender')"
          :disabled="urlName === 'read'"
        ></FormSelect>
        <FormInput
          v-model="formData.company"
          :label="$t('user.company')"
          :disabled="urlName === 'read'"
        ></FormInput>

        <FormInput
          v-model="formData.title"
          :label="$t('user.title')"
        ></FormInput>
        <FormInput
          v-model="formData.country"
          :label="$t('user.country')"
          :disabled="urlName === 'read'"
        ></FormInput>
        <FormInput
          v-model="formData.province"
          :label="$t('user.province')"
          :disabled="urlName === 'read'"
        ></FormInput>
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
      </fieldset>
      <div class="row">
        <div class="col-12">
          <FormButton
            v-if="isEdit"
            @click="submitForm"
            :label="$t('actions.submit')"
          ></FormButton>
          <FormButton
            v-if="!isEdit"
            @click="router.push('/auth/myprofile/edit')"
            :label="$t('actions.edit')"
          ></FormButton>
          <FormButton
            v-if="isEdit"
            @click="router.push('/auth/myprofile')"
            :label="$t('actions.cancel')"
            btnClass="btn"
          ></FormButton>
        </div>
      </div>
    </form>
  </div>
</template>

<script scope>
import { reactive, onMounted, toRefs, computed, inject } from "vue";
import { useRouter } from "vue-router";
import { useAxios, useStore } from "@/main";
import { genColClass } from "@/myjs";
import FormInput from "@/components/ui/FormInput";
import FormSelect from "@/components/ui/FormSelect";
import FormButton from "@/components/ui/FormButton";
export default {
  props: {
    isEdit: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  components: { FormInput, FormButton, FormSelect },
  setup() {
    const data = reactive({
      formData: {
        sid: "",
        create_time_local: "",
        update_time_local: "",
        is_deleted: false,
        username: "",
        email: "",
        role_sid: "",
        company: "",
        name: "",
        name_en: "",
        title: "",
        country: "",
        province: "",
        gender: "",
        is_su: true,
        last_seen_local: "",
        user_config: {
          locale: "zh",
          use_half: false,
        },
      },
    });
    const $t = inject("t");

    const moment = inject("moment");
    const last_seen_local_str = computed(() =>
      moment(data.formData.last_seen_local).format("YYYY-MM-D H:mm")
    );
    const axios = useAxios();
    const router = useRouter();
    const store = useStore();
    const cacheInfo = computed(() => store.state.cacheInfo);

    const getData = () => {
      axios({
        method: "get",
        url: "/auth/myprofile",
      }).then((res) => {
        data.formData = res.data;
      });
    };
    const submitForm = () => {
      if (!data.formData.email && !data.formData.phone) {
        alert($t("user.no_email_phone"));
        return false;
      }
      axios({
        method: "post",
        url: "/auth/myprofile/edit",
        data: data.formData,
      }).then(() => {
        router.push("/auth/myprofile");
        return false;
      });
    };
    onMounted(() => {
      getData();
    });
    return {
      ...toRefs(data),
      submitForm,
      router,
      genColClass,
      last_seen_local_str,
      cacheInfo,
    };
  },
};
</script>
