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
      <dt class="col-3">{{ $t("models.oem") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("oem_sid", formData.oem_sid) }}
      </dd>
      <dt class="col-3">{{ $t("project.is_filing") }}</dt>
      <dd class="col-9">
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            :checked="formData.is_filing"
            disabled
          />
        </div>
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
// 非标
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
    const store = useStore();
    return { readUrlDict, cls, store };
  },
};
</script>