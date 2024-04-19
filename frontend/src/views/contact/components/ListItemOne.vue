<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("contact.name") }}</dt>
      <dd class="col-9">{{ formData.name }}</dd>
      <dt class="col-3">{{ $t("user.company") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("oem_sid", formData.oem_sid) }}
      </dd>
      <dt class="col-3">{{ $t("user.title") }}</dt>
      <dd class="col-9">{{ formData.title }}</dd>
      <dt class="col-3">{{ $t("contact.department") }}</dt>
      <dd class="col-9">{{ formData.department }}</dd>
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