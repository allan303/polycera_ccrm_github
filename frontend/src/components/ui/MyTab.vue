<template>
  <div class="row">
    <ul class="nav nav-tabs">
      <li class="nav-item" v-for="(item, index) in tabs" :key="index">
        <OneTab
          :index="index"
          :tabName="item"
          :activeTabIndex="valueLocal"
          @click="onClick(index)"
        ></OneTab>
      </li>
    </ul>
  </div>
</template>
<script>
import { watch, ref, defineComponent } from "vue";
import OneTab from "./OneTab";
export default defineComponent({
  props: {
    modelValue: { default: 0 }, // 此为绑定值，即ActiveIndex
    tabs: { type: Array },
  },
  components: { OneTab },
  setup(props, { emit }) {
    const valueLocal = ref(props.modelValue);
    // 如果父组件传过来的数据是异步获取的，则需要进行监听
    watch(
      () => props.modelValue,
      () => {
        valueLocal.value = props.modelValue;
      }
    );
    // 数据双向绑定
    const onClick = (index) => {
      valueLocal.value = index;
      emit("update:modelValue", valueLocal.value);
    };
    return { onClick, valueLocal };
  },
});
</script>