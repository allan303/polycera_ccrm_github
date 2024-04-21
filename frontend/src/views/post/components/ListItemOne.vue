<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
    :cardHeaderClass="cardHeaderClass"
    :cardHeaderTextClass="cardHeaderTextClass"
  >
    <p v-html="formData.body"></p>
  </StandardListItemOne>
</template>
<script scope>
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
import { computed } from "@vue/runtime-core";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup(props) {
    const cardHeaderClass = computed(() =>
      // 系统自动创建的，不同样式
      props.formData.is_system ? " bg-secondary text-white" : ""
    );
    const cardHeaderTextClass = computed(() =>
      props.formData.is_system ? "text-white" : ""
    );
    return { readUrlDict, cardHeaderClass, cardHeaderTextClass };
  },
};
</script>