<template>
  <div :class="cls">
    <div class="card border-primary">
      <div :class="`card-header ${headerClass}`">
        <div class="d-flex justify-content-between">
          <slot name="header"></slot>
          <!-- 用于放大缩小 -->
          <div class="btn-toolbar">
            <button
              type="button"
              class="btn btn-sm"
              @click="useFull = !useFull"
            >
              <i class="bi-arrows-fullscreen text-white"></i>
            </button>
          </div>
        </div>
      </div>
      <div :class="`card-body ${bodyClass}`">
        <slot name="body"></slot>
      </div>
      <div class="card-action">
        <slot name="action"></slot>
      </div>
    </div>
  </div>
</template>
<script scope>
import { computed, ref, defineComponent } from "vue";
export default defineComponent({
  props: {
    col: { type: String, default: "6" },
    headerClass: {
      type: String,
      default: " text-white bg-primary  ",
    },
    bodyClass: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    const useFull = ref(false);
    const cls = computed(() => {
      if (useFull.value) {
        return `col-12 mt-2`;
      } else {
        return `col-md-${props.col} mt-2`;
      }
    });
    return { cls, useFull };
  },
});
</script>