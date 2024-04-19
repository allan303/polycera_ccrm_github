<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <p>{{ formData.body }}</p>
  </StandardListItemOne>
</template>
<script>
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup() {
    return { readUrlDict };
  },
};
</script>