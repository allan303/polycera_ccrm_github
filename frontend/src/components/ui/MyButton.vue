<template>
  <button
    :type="btnType"
    :class="genBtnClass(position, btnClass, other)"
    data-bs-placement="left"
    :title="tooltipData"
    :disabled="disabled"
    @click="clickHandle"
    :data-bs-dismiss="dataBsDismiss"
    :aria-label="ariaLabel"
    :data-bs-toggle="dataBsToggle"
    :data-bs-target="dataBsTarget"
  >
    <i
      :class="`bi-${icon}`"
      :style="`font-size: ${iconSize}rem`"
      v-if="icon"
    ></i>
    {{ label }}
  </button>
</template>
<script scope>
import { computed, defineComponent } from "vue";
import { genBtnClass } from "@/myjs";

export default defineComponent({
  name: "MyButton",
  props: {
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
    // @click
    const clickHandle = () => {
      emit("click");
    };
    const other = computed(() => (props.small ? "mt-2 btn-sm" : "mt-2"));
    return {
      clickHandle,
      genBtnClass,
      other,
    };
  },
});
</script>
