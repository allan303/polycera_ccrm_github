<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("models.project") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("project_sid", formData.project_sid) }}
      </dd>
      <dt class="col-3">{{ $t("project.pjstage") }}</dt>
      <dd class="col-9">{{ formData.pjstage }}</dd>
      <dt class="col-3">{{ $t("project.win_percentage") }}</dt>
      <dd :class="`col-9 ${cls}`">{{ formData.win_percentage }} %</dd>
      <dt class="col-3">{{ $t("project.forecast_date") }}</dt>
      <dd class="col-9">
        {{ formData.forecast_date }}
      </dd>
      <dt class="col-3">{{ $t("same.remark") }}</dt>
      <dd class="col-9">
        {{ formData.remark }}
      </dd>
    </dl>
  </StandardListItemOne>
</template>
<script>
import { computed } from "vue";
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
import { useStore } from "@/main";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup(props) {
    const store = useStore();
    const cls = computed(() => {
      if (props.formData.win_percentage === 100) {
        return "bg-primary text-white";
      } else if (props.formData.win_percentage === 0) {
        return "bg-secondary text-white";
      }
      return "";
    });
    return { readUrlDict, cls, store };
  },
};
</script>