<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <FormInput label="版本" v-model="formData.version"></FormInput>
    <FormTextarea
      label="项目概述(体现方案中)"
      v-model="formData.project_remark"
      :col="{ md: 12 }"
      :rows="3"
    ></FormTextarea>
    <FormTextarea
      label="工艺(体现方案中)"
      v-model="formData.treatment_process"
      :col="{ md: 12 }"
      :rows="3"
    ></FormTextarea>
    <FormTextarea
      label="工艺说明(体现方案中)"
      v-model="formData.treatment_process_note"
      :col="{ md: 12 }"
      :rows="3"
    ></FormTextarea>
    <FormTextarea
      label="特殊说明(体现方案中)"
      v-model="formData.special_note"
      :col="{ md: 12 }"
      :rows="3"
    ></FormTextarea>

    <h4 class="row mt-3">以下为性能保证（仅体现在方案中）</h4>
    <FormInput label="浊度NTU" v-model="formData.ntu"></FormInput>
    <FormInput label="悬浮物TSS mg/L" v-model="formData.tss"></FormInput>
    <FormInput label="SDI" v-model="formData.sdi"></FormInput>
    <FormInput label="回收率%" v-model="formData.rec"></FormInput>
    <FormInput label="膜寿命" v-model="formData.lifetime"></FormInput>
  </fieldset>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import FormTextarea from "@/components/ui/FormTextarea";
export default defineComponent({
  components: { FormInput, FormTextarea },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const formData = storeLocal.state.fd.options.other_info;
    return { storeLocal, formData, store, urlName };
  },
});
</script>