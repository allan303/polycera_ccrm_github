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
      <dt class="col-3">{{ $t("project.industry") }}</dt>
      <dd class="col-9">{{ formData.industry }}</dd>
      <dt class="col-3">{{ $t("same.type") }}</dt>
      <dd class="col-9">{{ formData.pjtype }}</dd>
      <dt class="col-3">{{ $t("project.pjstage") }}</dt>
      <dd class="col-9">{{ formData.pjstage }}</dd>
      <dt class="col-3">{{ $t("project.win_percentage") }}</dt>
      <dd :class="`col-9 ${cls}`">{{ formData.win_percentage }} %</dd>
      <dt class="col-3">{{ $t("project.filing_summary") }}</dt>
      <dd class="col-9">
        {{ formData.filing_summary }}
      </dd>
      <dt class="col-3">{{ $t("same.remark") }}</dt>
      <dd class="col-9">
        {{ formData.remark }}
      </dd>
    </dl>
  </StandardListItemOne>
</template>
<script scope>
import StandardListItemOne from "@/components/StandardListItemOne";
import { readUrlDict } from "./js";
import { computed } from "@vue/runtime-core";
export default {
  props: {
    formData: { type: Object },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup(props) {
    const cls = computed(() => {
      if (props.formData.win_percentage === 100) {
        return "bg-primary text-white";
      } else if (props.formData.win_percentage === 0) {
        return "bg-secondary text-white";
      }
      return "";
    });
    return { readUrlDict, cls };
  },
};
</script>