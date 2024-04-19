<template>
  <div :class="finalInputClass">
    <label :for="id" class="form-label mt-3" v-if="label">{{ label }}</label>
    <div>
      <quillEditor
        :id="id"
        v-model:value="valueLocal"
        @change="valChange(valueLocal)"
        :disabled="disabled"
        :options="editorOption"
      ></quillEditor>
    </div>
  </div>
</template>
<script>
import { defineComponent, reactive, ref, toRefs, watch } from "vue";
import { genColClass, genUid } from "@/myjs";
import { quillEditor } from "vue3-quill";

export default defineComponent({
  // 自定义Component，可以实现V-model双向绑定
  name: "FormRichtext",
  components: { quillEditor },
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      type: String,
      default: "",
    },
    label: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    disabled: { type: Boolean, default: false },
    col: { type: Object, default: null },
    icon: { type: String, default: "" },
    theme: { type: String, default: "bubble" },
  },
  setup(props, { emit }) {
    // input初始化
    const valueLocal = ref(props.modelValue);
    const data = reactive({
      rawClass: "form-control",
      defaultInputClass: "",
      id: "",
      finalInputClass: "",
    });
    const editorOption = {
      theme: props.theme,
      placeholder: props.placeholder,
    };
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
      editorOption,
    };
  },
});
</script>
