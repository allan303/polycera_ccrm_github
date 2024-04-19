<template>
  <div :class="finalInputClass">
    <label :for="id" class="form-label mt-3" v-if="useLabel">
      {{ label }}
    </label>
    <div class="input-group">
      <input
        :list="id2"
        :class="rawClass"
        :id="id"
        v-model="valueLocal"
        @blur="resetValue"
        @change="valChange(valueLocal)"
        :disabled="disabled"
        :placeholder="placeholder"
        :readonly="readonly"
        :multiple="multiple"
      />
      <datalist :id="id2">
        <option value=""></option>
        <option
          v-for="(item, index) in options"
          :key="index"
          :value="getOptionValue(item, valueKey)"
        >
          {{ getOptionText(item, textKey) }}
        </option>
      </datalist>
      <span
        class="input-group-text btn"
        @click="valChange(null)"
        v-if="!disabled && !readonly && useDelete"
      >
        <i class="bi-x"></i>
      </span>
    </div>
  </div>
</template>
<script>
import { computed, defineComponent, reactive, ref, toRefs, watch } from "vue";
import { genColClass, genUid, getOptionText, getOptionValue } from "@/myjs";

export default defineComponent({
  // 自定义Component，可以实现V-model双向绑定
  name: "FormDatalist",
  props: {
    modelValue: {
      // 父组件 v-model 没有指定参数名，则默认是 modelValue
      default: "",
    },
    label: { type: String, default: "" },
    disabled: { type: Boolean, default: null },
    col: { type: Object, default: null },
    inputType: { type: String, default: "text" },
    icon: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    readonly: { type: Boolean, default: false },
    useDelete: { type: Boolean, default: true },
    //以下为 select 特有
    valueKey: { type: String, default: "sid" },
    textKey: { default: "name" },
    options: { type: Array, default: Array },
    multiple: { type: Boolean, default: false },

    //以下为 datalist 特有
    //是否 允许采用输入值
    allowInput: { type: Boolean, default: false },
    useLabel: { type: Boolean, default: true },
  },
  setup(props, { emit }) {
    // input初始化
    const valueLocal = ref(props.modelValue);

    const data = reactive({
      rawClass: "form-control",
      defaultInputClass: "",
      id: "",
      id2: "",
      finalInputClass: "",
    });

    // generate default input class
    data.defaultInputClass = genColClass({
      md: 6,
      xl: 4,
    });
    // 生成UID 作为ID
    data.id = genUid();
    data.id2 = genUid();
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
    // Datalist 可以选择 也可以自己输入，
    // 要限制是否允许采用 自己输入值
    const values = computed(() => {
      let ls = [];
      for (let item of props.options) {
        ls.push(getOptionValue(item, props.valueKey));
      }
      return ls;
    });
    const validateData = computed(() => {
      if (["", null, undefined].includes(valueLocal.value)) {
        return true;
      } else if (values.value.includes(valueLocal.value)) {
        return true;
      }
      return false;
    });
    const resetValue = () => {
      if (!props.allowInput) {
        if (!validateData.value) {
          alert("只能选择已存在选项！");
          valueLocal.value = null;
        }
      }
    };
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
      values,
      getOptionText,
      getOptionValue,
      resetValue,
    };
  },
});
</script>
