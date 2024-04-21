<template>
  <StandardIndex :useSearch="false" :items="items"></StandardIndex>
</template>

<script scope>
import StandardIndex from "@/components/StandardIndex";

export default {
  components: { StandardIndex },
  setup() {
    const items = [];

    return { items };
  },
};
</script>