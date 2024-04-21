<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="alert alert-warning" role="alert">
        {{ $t("auth.forgetPwd") }}
      </div>
    </div>
  </div>
  <div class="row justify-content-center">
    <form class="col-md-6">
      <FormInput
        :label="$t('auth.email_phone')"
        icon="account_circle"
        inputType="text"
        :col="{ md: 12 }"
        v-model="username"
        @keyup.enter="submitForm"
      ></FormInput>
      <FormInput
        :label="$t('auth.pwd')"
        icon="lock"
        inputType="password"
        :col="{ md: 12 }"
        v-model="password"
        @keyup.enter="submitForm"
      ></FormInput
      ><br />
      <div class="row">
        <div class="col-12">
          <FormButton
            iconSize="1"
            :label="$t('auth.login')"
            @click="submitForm"
            :useCol="true"
          ></FormButton>
        </div>
      </div>
    </form>
  </div>
</template>
<script scope>
import { validateForm, genColClass } from "@/myjs";
import { inject, reactive, toRefs } from "vue";
import { useStore, useAxios } from "@/main";
import { useRoute, useRouter } from "vue-router";
import FormInput from "@/components/ui/FormInput";
import FormButton from "@/components/ui/FormButton";

export default {
  components: { FormInput, FormButton },
  setup() {
    const data = reactive({
      username: "",
      password: "",
    });
    const axios = useAxios();
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const $t = inject("t");
    // 如果已经登录，则在此页面直接跳转
    if (store.getters.isLogin()) {
      const nexturl = route.query.nexturl;
      if (nexturl) {
        router.push(nexturl);
      } else {
        router.push({
          path: "/",
        });
      }
    }
    const updateLocale = inject("updateLocale");
    // submit Login
    const submitForm = () => {
      const validateFields = [
        [$t("user.email"), "required", data.username],
        [$t("user.password"), "required", data.password],
        [$t("user.password"), "len_ge", data.password, 2],
      ];
      if (validateForm($t, validateFields)) {
        axios({
          method: "post",
          url: "/auth/login",
          data: `username=${data.username}&password=${data.password}`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }).then((res) => {
          store.actions.setState(res.data);
          store.actions.setTokenRecieveTime();
          //登录成功后： 1） 更新user_config 到本地
          store.actions.updateLocal(res.data.cu.user_config);
          store.actions.updateLocalByKey(
            "workgroup_sid",
            store.state.cu.workgroup_sid
          );
          alert($t("auth.loginSuccess"));
          const nexturl = route.query.nexturl;
          if (nexturl) {
            router.push(nexturl);
          } else {
            router.push({
              path: "/",
            });
          }
          updateLocale();
          setTimeout(function () {
            store.actions.updateCacheInfo(axios, "");
          }, 2000);
        });
      }
    };
    return { ...toRefs(data), submitForm, genColClass };
  },
};
</script>
<style scoped>
w-form {
  max-width: 200px;
}
</style>