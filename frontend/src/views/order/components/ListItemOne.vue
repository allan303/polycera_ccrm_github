<template>
  <StandardListItemOne
    :formData="formData"
    :readUrlDict="readUrlDict"
    :urlModel="urlModel"
  >
    <dl class="row">
      <dt class="col-3">{{ $t("order.name") }}</dt>
      <dd class="col-9">{{ formData.name }}</dd>
      <dt class="col-3">{{ $t("order.status") }}</dt>
      <dd class="col-9 bg-info text-white">{{ formData.status }}</dd>
      <dt class="col-3">{{ $t("models.oem") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("oem_sid", formData.oem_sid) }}
      </dd>
      <dt class="col-3">{{ $t("models.contact") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("contact_sid", formData.contact_sid) }}
      </dd>
      <dt class="col-3">{{ $t("models.project") }}</dt>
      <dd class="col-9">
        {{ store.getters.objName("project_sid", formData.project_sid) }}
      </dd>
      <dt class="col-3" v-if="storeLocal === null">{{ $t("order.price") }}</dt>
      <dd class="col-9" v-if="storeLocal === null">
        {{ numeral(formData.price).format("0,0.00") }} RMB
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
import { computed, inject } from "vue";
import { useStore } from "@/main";
export default {
  props: {
    formData: {
      type: Object,
      default() {
        return {};
      },
    },
    urlModel: { type: String, default: null },
  },
  components: { StandardListItemOne },
  setup(props) {
    const numeral = inject("numeral");
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const cls = computed(() => {
      if (props.formData.win_percentage === 100) {
        return "bg-primary text-white";
      } else if (props.formData.win_percentage === 0) {
        return "bg-secondary text-white";
      }
      return "";
    });
    return { readUrlDict, cls, numeral, storeLocal, store };
  },
};
</script>