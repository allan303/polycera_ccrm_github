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
        <label class="form-check-label" for="is_use"> *启用 </label>
      </div>
    </div>
    <div class="col-md-6" v-if="formData.is_use">
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          v-model="formData.use_wash"
          id="use_wash"
        />
        <label class="form-check-label" for="use_wash"> 反洗同时正冲 </label>
      </div>
    </div>
    <div class="col-md-6" v-if="formData.is_use">
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          v-model="formData.is_drain_out"
          id="is_drain_out"
        />
        <label class="form-check-label" for="is_drain_out">
          反洗水排空(不勾选则为：反洗水回流到前端)
        </label>
      </div>
    </div>
  </fieldset>
  <fieldset class="row" :disabled="urlName === 'read'" v-if="formData.is_use">
    <FormInput
      label="*反洗通量 LMH"
      v-model="formData.lmh"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*反洗时间(秒)"
      v-model="formData.duration.val"
      inputType="number"
    ></FormInput>
    <FormInput
      label="*反洗间隔(分钟)"
      v-model="formData.interval.val"
      inputType="number"
    ></FormInput>
    <FormInput
      label="每次损耗(秒)-阀门切换等"
      v-model="formData.duration_add.val"
      inputType="number"
    ></FormInput>
    <FormInput
      label="反洗压力(Bar)"
      v-model="formData.pressure.val"
      inputType="number"
    ></FormInput>
    <FormInput
      label="正冲流量-每个并列膜壳(m3/h), 可留空"
      v-model="formData.backwash_wash_m3ph_per_train"
      inputType="number"
      v-if="formData.use_wash"
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
    const formData = storeLocal.state.fd.options.backwash;
    return { storeLocal, formData, store, urlName };
  },
});
</script>