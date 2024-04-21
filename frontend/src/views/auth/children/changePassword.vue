<template>
  <div class="row justify-content-center">
    <form class="col-md-6">
      <FormInput
        :col="{ md: 12 }"
        :label="$t('auth.oldPwd')"
        icon="lock"
        inputType="password"
        v-model="old_password"
      ></FormInput>
      <FormInput
        :col="{ md: 12 }"
        :label="$t('auth.newPwd')"
        icon="lock"
        inputType="password"
        v-model="new_password"
      ></FormInput>
      <FormInput
        :col="{ md: 12 }"
        :label="$t('auth.confirmPwd')"
        icon="lock"
        inputType="password"
        v-model="new_password2"
      ></FormInput>
      <br />
      <FormButton
        :label="$t('actions.submit')"
        btnType="submit"
        @click="submitForm"
        :useCol="true"
      ></FormButton>
    </form>
  </div>
</template>

<script scope>
import { inject, reactive, toRefs } from "vue";
import { useStore, useAxios } from "@/main";
import { useRouter } from "vue-router";
import { validateForm, genColClass } from "@/myjs";
import FormInput from "@/components/ui/FormInput";
import FormButton from "@/components/ui/FormButton";

export default {
  components: { FormInput, FormButton },
  setup() {
    const data = reactive({
      old_password: "",
      new_password: "",
      new_password2: "",
    });
    const router = useRouter();
    const store = useStore();
    const axios = useAxios();
    const $t = inject("t");
    const submitForm = () => {
      const validateFields = [
        [$t("auth.oldPwd"), "required", data.old_password],
        [$t("auth.newPwd"), "required", data.new_password],
        [$t("auth.confirmPwd"), "required", data.new_password2],
        [
          $t("auth.confirmPwd"),
          "confirmPassword",
          data.new_password,
          data.new_password2,
        ],
      ];
      if (validateForm($t, validateFields)) {
        axios({
          method: "post",
          url: "/auth/change-password",
          data: data,
        }).then(() => {
          alert($t("auth.changePwdSuccess"));
          store.actions.resetState();
          router.push("/auth/login");
          return false;
        });
      }
    };

    return {
      ...toRefs(data),
      submitForm,
      genColClass,
    };
  },
};
</script>
