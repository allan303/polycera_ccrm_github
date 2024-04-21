<template>
  <div class="row">
    <div class="clo-6">
      <MyButton
        :label="label || $t('actions.add')"
        @click="goCreate"
        icon="plus-lg"
      ></MyButton>
    </div>
  </div>
</template>
<script scope>
//在ins页面下的子list清单中，新增关联的子项
import MyButton from "./ui/MyButton.vue";
import { useRouter } from "vue-router";
import { defineComponent } from "vue";
export default defineComponent({
  components: { MyButton },
  props: {
    urlModel: { type: String, required: true },
    label: { type: String },
    filter_dt_and: { type: Object },
  },
  setup(props) {
    const router = useRouter();
    // console.log("props.filter_dt_and:::", props.filter_dt_and);
    const goCreate = () => {
      // const { href } = router.resolve({
      //   path: `/${props.urlModel}/create`,
      //   query: props.filter_dt_and,
      // });
      // window.open(href, "_blank");
      // return Promise.resolve(false);
      router.push({
        path: `/${props.urlModel}/create`,
        query: props.filter_dt_and,
      });
    };
    return { goCreate };
  },
});
</script>