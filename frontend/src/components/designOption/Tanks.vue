<template>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <FormInput
      v-model="formData.feed.hrt_minutes"
      label="原水箱停留时间(分钟),通常30~120分钟"
      inputType="number"
      :col="{ s: 12 }"
    ></FormInput>
    <FormInput
      v-model="formData.perm.hrt_minutes"
      label="产水箱停留时间(分钟),通常30~120分钟"
      inputType="number"
      :col="{ s: 12 }"
    ></FormInput>
    <FormInput
      v-model="formData.cip.hrt_minutes"
      label="化学清洗箱停留时间(分钟),通常1.5~3分钟"
      inputType="number"
      :col="{ s: 12 }"
    ></FormInput>
  </fieldset>
</template>
<script scope>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
export default defineComponent({
  components: { FormInput },
  setup() {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const op = storeLocal.state.fd.options;
    const formData = op.tanks;
    return { storeLocal, formData, store, urlName };
  },
});
</script>