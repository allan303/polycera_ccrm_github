<template>
  <div :class="finalInputClass">
    <label :for="id" class="form-label mt-3" v-if="label">{{ label }} </label>
    <div class="input-group">
      <slot></slot>
      <Multiselect
        :id="id"
        v-model="valueLocal"
        :options="optionsLocal"
        :mode="mode"
        valueProp="value"
        label="text"
        :searchable="true"
        trackBy="text"
        :multipleLabel="getLabels"
        :disabled="disabled"
      ></Multiselect>
    </div>
  </div>
</template>
<script>
import { computed, defineComponent, reactive, ref, toRefs, watch } from "vue";
import { genColClass, genUid, getOptionText, getOptionValue } from "@/myjs";
import Multiselect from "@vueform/multiselect";

export default defineComponent({
  components: { Multiselect },
  // 自定义Component，可以实现V-model双向绑定
  name: "FormSelect",
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      default: null,
    },
    label: { type: String, default: "" },
    disabled: { type: Boolean, default: null },
    col: { type: Object, default: null },
    icon: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    readonly: { type: Boolean, default: false },
    useDelete: { type: Boolean, default: true },
    //以下为 select 特有
    valueKey: { type: String, default: "sid" },
    textKey: { default: "name" },
    options: {},
    mode: { type: String, default: "single" },
    default_content: { type: Array, default: null },
  },
  setup(props, { emit }) {
    // input初始化
    const valueLocal = ref(props.modelValue);

    const data = reactive({
      rawClass: "form-select",
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
    const getLabels = (items) => {
      // 多选后显示的labels
      const ls = [];
      for (let item of items) {
        ls.push(item.text);
      }
      let str = ls.join(", ");
      return str;
    };
    // 数据双向绑定
    const valChange = (e) => {
      console.log("valChange");
      emit("update:modelValue", e);
    };
    // 如果父组件传过来的数据是异步获取的，则需要进行监听
    watch(
      () => props.modelValue,
      () => {
        valueLocal.value = props.modelValue;
      }
    );
    watch(
      () => valueLocal.value,
      () => {
        valChange(valueLocal.value);
      }
    );

    const optionsLocal = computed(() => {
      // 可以增加 预设 选项；
      // 此处进行 option的转换
      let ls = [];
      if (props.default_content) {
        ls.push(...props.default_content);
      }
      ls.push(...props.options);
      // 以下为生成 实际的option
      let ls0 = [];
      for (let item of ls) {
        ls0.push({
          value: getOptionValue(item, props.valueKey),
          text: getOptionText(item, props.textKey),
        });
      }
      return ls0;
      // const ls = [{ sid: "all", name: "全部用户" }];
    });
    return {
      valueLocal,
      valChange,
      ...toRefs(data),
      getOptionText,
      getOptionValue,
      getLabels,
      optionsLocal,
    };
  },
});
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
