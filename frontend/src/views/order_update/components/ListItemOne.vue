<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("models.order") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("order_sid", formData.order_sid) }}
      </dd>
      <dt class="col-3">{{ $t("order.status") }}</dt>
      <dd class="col-9">{{ formData.status }}</dd>
      <dt class="col-3">{{ $t("same.remark") }}</dt>
      <dd class="col-9">{{ formData.remark }}</dd>
    </dl>
  </StandardListItemOne>
</template>
<script>
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
import { useStore } from "@/main";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup() {
    const store = useStore();
    return { readUrlDict, store };
  },
};
</script>