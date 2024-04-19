<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("same.name") }}</dt>
      <dd class="col-9">
        {{ formData.name }}, {{ formData.module_type
        }}{{ formData.membrane_type.toUpperCase() }}
      </dd>
      <dt class="col-3">{{ $t("product.brand") }}</dt>
      <dd class="col-9">{{ formData.brand }}</dd>
      <dt class="col-3">{{ $t("product.fa") }}</dt>
      <dd class="col-9">{{ formData.model }} {{ formData.fa }}m2</dd>
      <dt class="col-3">{{ $t("same.description") }}</dt>
      <dd class="col-9">{{ formData.description }}</dd>
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