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
      <fieldset class="row mt-3" :disabled="urlName === 'read'">
        <div class="col-md-6">
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              v-model="formData.use_ceb_pump"
              id="is_use"
            />
            <label class="form-check-label" for="is_use">
              设置独立CEB泵，而不是复用反洗泵
            </label>
          </div>
        </div>
      </fieldset>
      <div class="card mt-3 p-2">
        <div class="alert alert-warning" role="alert">
          如果反洗泵不采用变频，且不设置独立的CEB泵，则CEB注药通量只能和反洗通量一致，无法自定义设置
        </div>
        <div class="row">
          <FormInput
            label="CEB通量 LMH (即注药时反洗通量)"
            v-model="formData.lmh"
            inputType="number"
            :col="{ md: 12 }"
            v-if="pumps_pressure.backwash_vfd"
          ></FormInput>
          <FormInput
            label="CEB通量 LMH (即注药时反洗通量)"
            v-model="backwash.lmh"
            inputType="number"
            :col="{ md: 12 }"
            v-if="!pumps_pressure.backwash_vfd"
            disabled
          ></FormInput>
        </div>
        <div class="btn-group" role="group" v-if="urlName !== 'read'">
          <MyButton
            label="增加默认配置- 盐酸 HCl"
            btnClass=" btn-primary"
            @click="addCeb(defaultCebHcl())"
          ></MyButton>
          <MyButton
            label="增加默认配置- 氢氧化钠 NaOH"
            btnClass=" btn-primary"
            @click="addCeb(defaultCebNaOH())"
          ></MyButton>
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
<script scope>
import { inject, defineComponent, provide } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import MyButton from "@/components/ui/MyButton";
import OneClean from "./OneClean";
import { defaultCebHcl, defaultCebNaOH } from "./js";

export default defineComponent({
  components: { FormInput, OneClean, MyButton },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    provide("cleanName", "ceb");
    const pumps_pressure = storeLocal.state.fd.options.pumps_pressure;
    const backwash = storeLocal.state.fd.options.backwash;
    const formData = storeLocal.state.fd.options.ceb;
    const addCeb = (ceb) => {
      formData.oneclean_list.push(ceb);
    };

    return {
      storeLocal,
      formData,
      store,
      urlName,
      pumps_pressure,
      backwash,
      addCeb,
      defaultCebHcl,
      defaultCebNaOH,
    };
  },
});
</script>