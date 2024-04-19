<template>
  <a class="dropdown-item" @click="switchWorkgroup">{{ workgroup.name }}</a>
</template>
<script>
import { defineComponent } from "vue";
import { useStore } from "@/main";
import { useRouter } from "vue-router";
export default defineComponent({
  props: {
    workgroup: { type: Object },
  },
  setup(props) {
    //切换workgroup并刷新页面
    const store = useStore();
    const router = useRouter();
    const switchWorkgroup = () => {
      store.actions.updateLocalByKey("workgroup_sid", props.workgroup.sid);
      router.go(0);
    };
    return { switchWorkgroup };
  },
});
</script>