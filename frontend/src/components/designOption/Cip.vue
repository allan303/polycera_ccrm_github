<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <div class="col-md-6">
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          v-model="formData.is_use"
          id="is_use"
        />
        <label class="form-check-label" for="is_use"> 启用 </label>
      </div>
    </div>
  </fieldset>
  <div class="row" v-if="formData.is_use">
    <fieldset class="row" :disabled="urlName === 'read'">
      <div class="card mt-3 p-2">
        <div class="row">
          <FormInput
            label="CIP设备数量(整个系统)"
            v-model="formData.cip_nums"
            inputType="number"
            :col="{ md: 6 }"
          ></FormInput>
          <FormInput
            label="单膜壳流量,留空为5(m3/h)"
            v-model="formData.m3ph_per_train"
            inputType="number"
            :col="{ md: 6 }"
          ></FormInput>
        </div>
        <div class="btn-group" role="group" v-if="urlName !== 'read'">
          <FormButton
            label="增加默认配置- 盐酸 HCl"
            btnClass=" btn-primary"
            @click="addCip(defaultCipHCl())"
          ></FormButton>
          <FormButton
            label="增加默认配置- 柠檬酸"
            btnClass=" btn-primary"
            @click="addCip(defaultCipCitric())"
          ></FormButton>
          <FormButton
            label="增加默认配置- 氢氧化钠 NaOH"
            btnClass=" btn-primary"
            @click="addCip(defaultCipNaOH())"
          ></FormButton>
        </div>
      </div>
      <div class="card mt-3 p-2">
        <div v-for="(item, index) in formData.oneclean_list" :key="item">
          <!-- 传递 index，并用key=item实现 更新dom -->
          <OneClean :oneclean_index="index"></OneClean>
        </div>
      </div>
    </fieldset>
  </div>
</template>
<script>
import { inject, defineComponent, provide } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import FormButton from "@/components/ui/FormButton";
import OneClean from "./OneClean";
import { defaultCipHCl, defaultCipNaOH, defaultCipCitric } from "./js";

export default defineComponent({
  components: { FormInput, OneClean, FormButton },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    provide("cleanName", "cip");
    const formData = storeLocal.state.fd.options.cip;
    const addCip = (cip) => {
      formData.oneclean_list.push(cip);
    };

    return {
      storeLocal,
      formData,
      store,
      urlName,
      addCip,
      defaultCipHCl,
      defaultCipNaOH,
      defaultCipCitric,
    };
  },
});
</script>