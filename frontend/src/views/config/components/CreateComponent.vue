<template>
  <div class="row">
    <MyButton
      @click="confirmDo($t('msg.confirm'), goReset)"
      btnClass="btn-warning"
      :label="$t('config.reset')"
    ></MyButton>
    <FormSelect
      v-model="keyName"
      :options="configKeys"
      :label="$t('config.chooseConfig')"
      :col="{ md: 12 }"
    ></FormSelect>
  </div>
  <div class="row mt-3">
    <ChemList :keyName="keyName" v-if="keyName === 'chem'"></ChemList>
    <PjstageList
      :keyName="keyName"
      v-else-if="keyName === 'pjstage'"
    ></PjstageList>
    <TextList :keyName="keyName" v-else></TextList>
  </div>
  <MyButton
    @click="goSubmit"
    btnClass="btn-primary"
    :label="$t('actions.submit')"
  ></MyButton>
</template>

<script scope>
import { computed, provide, reactive, toRefs, onMounted } from "vue";
import { useAxios, useStore } from "@/main";
import FormSelect from "@/components/ui/FormSelect";
import MyButton from "@/components/ui/MyButton";
import { createStore } from "./js";
import TextList from "./child/TextList";
import ChemList from "./child/ChemList";
import PjstageList from "./child/PjstageList";
import { confirmDo } from "@/myjs";
export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: { FormSelect, MyButton, TextList, ChemList, PjstageList },
  setup(props) {
    const axios = useAxios();
    const store = useStore();
    const storeLocal = createStore();
    //注入 createComponent 所有子组件
    provide("storeLocal", storeLocal);
    //此item限定条件
    provide("urlName", props.urlName);
    const formData = storeLocal.state.fd;
    console.log(storeLocal.state.fd);

    const configKeys = computed(() =>
      Object.keys(store.state.cacheInfo.config)
    );
    const data = reactive({
      keyName: "location",
    });
    // 以下为方法
    const getCurrentObj = () => {
      axios({
        method: "get",
        url: `/config/read`,
      }).then((res) => {
        Object.assign(formData, res.data);
      });
    };
    onMounted(() => {
      getCurrentObj();
    });
    const goSubmit = () => {
      axios({
        method: "post",
        url: `/config/edit`,
        data: formData,
      }).then(() => {
        store.actions.updateCacheInfo(axios, "config");
      });
    };
    const goReset = () => {
      //重置 keyName
      axios({
        method: "post",
        url: `/config/reset/${data.keyName}`,
      }).then((res) => {
        Object.assign(formData, res.data);
        store.actions.updateCacheInfo(axios, "config");
      });
    };
    return {
      formData,
      configKeys,
      goSubmit,
      ...toRefs(data),
      confirmDo,
      goReset,
    };
  },
};
</script>
