<template>
  <div class="input-group mt-2">
    <span class="input-group-text" id="basic-addon3">{{ actionCnName }}</span>
    <!-- v-model必须绑定actions[action]，不能绑定scope（是个str） -->
    <select
      class="form-select"
      v-model="actions[action]"
      :disabled="urlName === 'read' || ['create', 'edit'].includes(action)"
    >
      <option
        v-for="(item, index) in permOption.scopes"
        :key="index"
        :label="item.text"
      >
        {{ item.value }}
      </option>
    </select>
    <button
      class="btn btn-danger"
      v-if="urlName !== 'read'"
      @click="deleteSelf"
    >
      <i class="bi-trash"></i>
    </button>
  </div>
</template>
<script>
import { computed, defineComponent, inject } from "vue";
import { useStore } from "@/main";
export default defineComponent({
  props: { action: { type: String }, permModel: { type: String } },
  setup(props) {
    const urlName = inject("urlName");
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const permOption = store.state.perm_option;
    const perm = storeLocal.state.fd.perm;
    const actions = perm[props.permModel]; //{read:me,assign:me}
    const actionCnName = computed(() => {
      for (let x of permOption.actions) {
        if (props.action === x.value) {
          return x.text;
        }
      }
      return props.action;
    });
    //直接 赋值，影响了reactive
    const deleteSelf = () => {
      delete actions[props.action];
    };
    return { deleteSelf, urlName, actions, permOption, actionCnName };
  },
});
</script>