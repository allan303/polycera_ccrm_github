<template>
  <div
    class="modal fade"
    id="assignModal"
    tabindex="-1"
    aria-labelledby="assignModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="assignModalLabel">
            {{ $t("actions.assign") }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            {{ $t("auth.currentOwner") }}:
            {{ store.getters.objName("owner_sid", formData.owner_sid) }}
          </p>
          <FormAutoSelect
            :options="store.state.cacheInfo.user"
            :label="$t('actions.assign')"
            v-model="userSid"
            textKey="name"
            valueKey="sid"
            :col="{ md: 12 }"
          ></FormAutoSelect>
          <button
            class="btn btn-primary mt-3"
            @click="goAssign(formData.sid, userSid)"
          >
            {{ $t("actions.submit") }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script scope>
import { defineComponent, ref } from "vue";
import { useStore } from "@/main";
import FormAutoSelect from "./ui/FormAutoSelect.vue";
export default defineComponent({
  props: {
    formData: { type: Object },
    goAssign: { type: Function },
  },
  components: { FormAutoSelect },
  setup() {
    const store = useStore();
    const userSid = ref(null);
    return { userSid, store };
  },
});
</script>