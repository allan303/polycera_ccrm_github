<template>
  <a :class="`nav-link btn ${cls}`" @click="clickHandle">
    {{ $t(tabName) }}
  </a>
</template>
<script scope>
import { computed, defineComponent } from "vue";
export default defineComponent({
  props: {
    index: { type: Number },
    activeTabIndex: { type: Number },
    tabName: { type: String, default: "tabName" },
  },
  setup(props, { emit }) {
    // 如果父组件传过来的数据是异步获取的，则需要进行监听
    const cls = computed(() => {
      if (props.index === props.activeTabIndex) {
        return "active";
      } else {
        return "";
      }
    });
    // 数据双向绑定
    const clickHandle = () => {
      emit("click");
    };
    return {
      clickHandle,
      cls,
    };
  },
});
</script>