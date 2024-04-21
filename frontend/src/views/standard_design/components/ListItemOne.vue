<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">名称</dt>
      <dd class="col-9">{{ formData.name }}</dd>
      <dt class="col-3">备注</dt>
      <dd class="col-9">
        {{ formData.remark }}
      </dd>
    </dl>
  </StandardListItemOne>
</template>
<script scope>
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