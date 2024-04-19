<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("same.name") }}</dt>
      <dd class="col-9">{{ formData.name }}</dd>
      <dt class="col-3">{{ $t("same.location") }}</dt>
      <dd class="col-9">{{ formData.location }}</dd>
      <dt class="col-3">{{ $t("same.type") }}</dt>
      <dd class="col-9">{{ formData.oemtype }}</dd>
      <dt class="col-3">{{ $t("same.remark") }}</dt>
      <dd class="col-9">
        {{ formData.remark }}
      </dd>
    </dl>
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