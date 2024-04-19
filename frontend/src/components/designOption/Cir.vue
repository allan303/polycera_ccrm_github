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
  <fieldset class="row" :disabled="urlName === 'read'" v-if="formData.is_use">
    <FormInput
      label="循环量(m3/h),每个膜壳(如果为2段设计，则为第一段膜壳)"
      v-model="formData.m3ph_per_train"
      inputType="number"
      :col="{ md: 12 }"
    ></FormInput>
  </fieldset>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";

export default defineComponent({
  components: { FormInput },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const formData = storeLocal.state.fd.options.cir;
    return { storeLocal, formData, store, urlName };
  },
});
</script>