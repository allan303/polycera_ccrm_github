<template>
  <nav style="--bs-breadcrumb-divider: ''" aria-label="breadcrumb" v-if="urls">
    <ol class="breadcrumb">
      <li class="breadcrumb-item" v-for="(url, index) in urls" :key="index">
        <router-link :to="url.url" class="link-primary fs-6"
          >#{{ url.name }}</router-link
        >
      </li>
    </ol>
  </nav>
</template>
<script scope>
import { ref, defineComponent, watch, onMounted, inject } from "vue";

import { getRelatedUrls1 } from "@/myjs";
import { useStore } from "@/main";
export default defineComponent({
  props: { formData: { type: Object }, readUrlDict: { type: Object } },
  setup(props) {
    const moment = inject("moment");
    const store = useStore();
    const urls = ref();
    const setUrls = () => {
      urls.value = getRelatedUrls1(props.readUrlDict, props.formData, store);
    };
    onMounted(() => setUrls);

    watch(
      () => props.formData,
      () => {
        setTimeout(setUrls, 500);
        setUrls();
      },
      { deep: true, immediate: true }
    );
    return { moment, urls };
  },
});
</script>