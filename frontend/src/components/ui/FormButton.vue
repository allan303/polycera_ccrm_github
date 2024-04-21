<template>
  <div :class="finalInputClass" v-if="useCol">
    <MyButton
      :label="label"
      :btnType="btnType"
      :btnClass="finalBtnClass"
      :icon="icon"
      :iconSize="iconSize"
      :disabled="disabled"
      :tooltipData="tooltipData"
      :position="position"
      :small="small"
      @click="clickHandle"
      :data-bs-dismiss="dataBsDismiss"
      :aria-label="ariaLabel"
      :data-bs-toggle="dataBsToggle"
      :data-bs-target="dataBsTarget"
    ></MyButton>
  </div>
  <MyButton
    :label="label"
    :btnType="btnType"
    :btnClass="finalBtnClass"
    :icon="icon"
    :iconSize="iconSize"
    :disabled="disabled"
    :tooltipData="tooltipData"
    :position="position"
    :small="small"
    @click="clickHandle"
    :data-bs-dismiss="dataBsDismiss"
    :aria-label="ariaLabel"
    :data-bs-toggle="dataBsToggle"
    :data-bs-target="dataBsTarget"
    v-else
  ></MyButton>
</template>
<script scope>
import { computed, defineComponent, onMounted, reactive, toRefs } from "vue";
import MyButton from "./MyButton.vue";
import { genColClass, genUid } from "@/myjs";

export default defineComponent({
  name: "FormButton",
  components: { MyButton },
  props: {
    col: { type: Object, default: null },
    useCol: { type: Boolean, default: false },
    //以下为MyButton
    label: { type: String, default: "Button" },
    btnType: { type: String, default: "button" },
    btnClass: { type: String, default: "btn-primary" },
    icon: { type: String, default: "" },
    iconSize: { type: String, default: "1" },
    disabled: { type: Boolean, default: null },
    tooltipData: { type: String, default: "" },
    position: { type: String, default: "" },
    small: { type: Boolean, default: false },
    dataBsDismiss: { type: String, default: "" },
    ariaLabel: { type: String, default: "" },
    dataBsToggle: { type: String, default: "" },
    dataBsTarget: { type: String, default: "" },
  },
  // 动作
  emits: {
    click: null,
  },
  setup(props, { emit }) {
    const data = reactive({
      rawClass: "form-control",
      defaultInputClass: "",
      id: "",
      finalInputClass: "",
    });
    // generate default input class
    data.defaultInputClass = genColClass({
      md: 12,
    });
    // 生成UID 作为ID
    data.id = genUid();
    // generate final input class if has props
    const setInputClass = () => {
      if (!props.useCol) {
        data.finalInputClass = "";
        return false;
      }
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
    const finalBtnClass = computed(() =>
      props.useCol
        ? `${data.rawClass} btn ${props.btnClass}`
        : `btn ${props.btnClass}`
    );
    // @click
    const clickHandle = () => {
      emit("click");
    };
    onMounted(() => {});
    return {
      clickHandle,
      ...toRefs(data),
      finalBtnClass,
    };
  },
});
</script>
