<template>
  <textarea
    :type="inputType"
    class="form-control"
    v-model="valueLocal"
    @change="valChange(valueLocal)"
    :disabled="disabled"
    :placeholder="placeholder"
    :readonly="readonly"
    :rows="rows"
  ></textarea>
</template>
<script scope>
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  // 自定义Component，可以实现V-model双向绑定
  name: "FormInput",
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      type: String,
      default: "",
    },
    disabled: { type: Boolean, default: null },
    inputType: { type: String, default: "text" },
    icon: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    readonly: { type: Boolean, default: false },
    //text area 特有
    rows: { type: Number, default: 6 },
  },
  setup(props, { emit }) {
    // input初始化
    const valueLocal = ref(props.modelValue);

    // 如果父组件传过来的数据是异步获取的，则需要进行监听
    watch(
      () => props.modelValue,
      () => {
        valueLocal.value = props.modelValue;
      }
    );

    // 数据双向绑定
    const valChange = (e) => {
      emit("update:modelValue", e);
    };

    return {
      valueLocal,
      valChange,
    };
  },
});
</script>
