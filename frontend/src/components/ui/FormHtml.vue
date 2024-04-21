<template>
  <div :class="finalInputClass">
    <label :for="id" class="form-label mt-3" v-if="label">{{ label }}</label>
    <p :class="rawClass" :id="id" v-html="modelValue"></p>
  </div>
</template>
<script scope>
import { defineComponent, reactive, toRefs } from "vue";
import { genColClass, genUid } from "@/myjs";

export default defineComponent({
  // 自定义Component，可以实现V-model双向绑定
  name: "FormInput",
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      type: String,
      default: "",
    },
    label: { type: String, default: "" },
    col: { type: Object, default: null },
    icon: { type: String, default: "" },
    small: { type: Boolean, default: false },
    rawClass: { type: String, default: "form-control" },
  },
  setup(props) {
    // input初始化
    const data = reactive({
      defaultInputClass: "",
      id: "",
      finalInputClass: "",
      rawClass: props.rawClass,
    });
    if (props.small) {
      data.rawClass = "form-control-sm";
    }
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

    return {
      ...toRefs(data),
    };
  },
});
</script>
