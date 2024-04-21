<template>
  <div :class="finalInputClass">
    <div class="form-check">
      <input
        :class="rawClass"
        type="checkbox"
        v-model="valueLocal"
        @change="valChange(valueLocal)"
        :id="id"
        :disabled="disabled"
        :readonly="readonly"
      />
      <label class="form-check-label" :for="id"> {{ label }} </label>
    </div>
  </div>
</template>
<script scope>
import { defineComponent, reactive, ref, toRefs, watch } from "vue";
import { genColClass, genUid } from "@/myjs";

export default defineComponent({
  // 自定义Component，可以实现V-model双向绑定
  name: "FormInput",
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      default: "",
    },
    label: { type: String, default: "" },
    disabled: { type: Boolean, default: null },
    col: { type: Object, default: null },
    readonly: { type: Boolean, default: false },
  },
  setup(props, { emit }) {
    // input初始化
    const valueLocal = ref(props.modelValue);
    const data = reactive({
      rawClass: "form-check-input",
      defaultInputClass: "",
      id: "",
      finalInputClass: "",
    });
    // generate default input class
    data.defaultInputClass = genColClass({
      md: 6,
      xl: 4,
    });
    // 生成UID 作为ID
    data.id = genUid();

    // generate final input class if has props
    const setInputClass = () => {
      if (props.col) {
        const colObj = Object.assign(props.col);
        colObj.other = colObj.other ? colObj.other : "";
        data.finalInputClass = genColClass(colObj);
      } else {
        data.finalInputClass = data.defaultInputClass;
      }
    };
    setInputClass();
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
      ...toRefs(data),
    };
  },
});
</script>
