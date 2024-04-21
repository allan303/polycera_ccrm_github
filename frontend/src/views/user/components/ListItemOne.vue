<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("user.name") }}</dt>
      <dd class="col-9">{{ formData.name }}</dd>
      <dt class="col-3">{{ $t("user.gender") }}</dt>
      <dd class="col-9">{{ formData.gender }}</dd>
      <dt class="col-3">{{ $t("models.role") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("role_sid", formData.role_sid) }}
      </dd>
      <dt class="col-3">{{ $t("user.username") }}</dt>
      <dd class="col-9">{{ formData.username }}</dd>
      <dt class="col-3">{{ $t("user.email") }}</dt>
      <dd class="col-9">{{ formData.email }}</dd>
      <dt class="col-3">{{ $t("user.company") }}</dt>
      <dd class="col-9">{{ formData.company }}</dd>
      <dt class="col-3">{{ $t("user.phone") }}</dt>
      <dd class="col-9">{{ formData.phone }}</dd>
      <dt class="col-3">{{ $t("same.location") }}</dt>
      <dd class="col-9">{{ formData.country }} {{ formData.province }}</dd>
      <dt class="col-3">{{ $t("user.last_seen") }}</dt>
      <dd class="col-9">{{ last }}</dd>
    </dl>
  </StandardListItemOne>
</template>
<script scope>
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
import { useStore } from "@/main";
import { computed, inject } from "vue";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup(props) {
    const moment = inject("moment");
    const store = useStore();
    const last = computed(() => {
      if (props.formData.last_seen_local) {
        return moment(props.formData.last_seen_local).format("YYYY-MM-D H:MM");
      }
      return "";
    });
    return { readUrlDict, moment, last, store };
  },
};
</script>