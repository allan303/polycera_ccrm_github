<template>
  <div class="row mt-3" v-if="urlName === 'read' && dr">
    <div class="alert alert-warning" role="alert">
      估算运行压力为（膜进口，无循环泵为原水泵出口，如有循环泵则为循环泵出口）：{{
        numeral(dr.real_feed_pressure.feed_bar).format("0.0")
      }}
    </div>
    <div class="alert alert-warning" role="alert">
      估算的单个膜壳压差为：{{
        numeral(dr.real_feed_pressure.dp_per_train).format("0.00")
      }}
      bar
    </div>
    <div class="alert alert-warning" role="alert">
      以上估算为膜系统未污染状态，请注意进水泵/循环增压泵是否留有余量。
    </div>
  </div>
  <div class="alert alert-warning mt-3" role="alert">
    如果反洗泵不采用变频，则CEB注药通量只能和反洗通量一致，无法自定义设置
  </div>
  <fieldset class="row mt-3" :disabled="urlName === 'read'">
    <FormInput
      v-model="formData.feed_pump"
      label="原水泵(bar)"
      inputType="number"
    ></FormInput>

    <FormInput
      v-model="formData.cir_pump"
      label="循环泵(bar)"
      inputType="number"
    ></FormInput>
    <FormInput
      v-model="formData.backwash_pump"
      label="反洗泵(bar)"
      inputType="number"
    ></FormInput>
    <FormInput
      v-model="formData.cip_pump"
      label="化学清洗泵(bar)"
      inputType="number"
    ></FormInput>
    <div class="row my-3">
      <FormCheckbox
        v-model="formData.feed_vfd"
        label="原水泵采用变频"
      ></FormCheckbox>
      <FormCheckbox
        v-model="formData.backwash_vfd"
        label="反洗泵采用变频"
      ></FormCheckbox>
      <FormCheckbox
        v-model="formData.cir_vfd"
        label="循环泵采用变频"
      ></FormCheckbox>
      <FormCheckbox
        v-model="formData.cip_vfd"
        label="清洗泵采用变频"
      ></FormCheckbox>
    </div>
  </fieldset>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import FormCheckbox from "@/components/ui/FormCheckbox";
export default defineComponent({
  components: { FormInput, FormCheckbox },
  setup() {
    const numeral = inject("numeral");
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const op = storeLocal.state.fd.options;
    const formData = storeLocal.state.fd.options.pumps_pressure;
    const dr = storeLocal.state.fd.design_result;
    return { storeLocal, formData, store, urlName, op, dr, numeral };
  },
});
</script>