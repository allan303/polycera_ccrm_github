<template>
  <div class="row">
    <div class="col-12">
      <h1 class="text-primary bold">PolyCera CCRM</h1>
      <p>
        本系统仅用于Polycera聚瓷（上海）科技有限公司内部项目管理、客户管理、设计软件等。
      </p>
      <p>如有疑问或者发现BUG，请联系Jack Li ： jack.li@polycera.com</p>
      <i class="bi-alarm"></i>
    </div>
  </div>
</template>
<script scope>
import { useStore } from "@/main";

import { reactive, toRefs } from "@vue/reactivity";
export default {
  setup() {
    const store = useStore();
    const data = reactive({
      a: "",
      b: [],
      c: "",
      d: "",
      e: "",
      op: [
        { text: "a", value: "a1" },
        { text: "b", value: "b1只是个" },
        { text: "c", value: "c1试试" },
      ],
      op2: ["aa", "adsa", "cc"],
      activeTab: 0,
    });
    const go = (hhh) => {
      alert(hhh);
    };
    const getLabels = (items) => {
      console.log(items);
      const ls = [];
      for (let item of items) {
        ls.push(item.name);

        console.log(str);
      }
      let str = ls.join(",");
      return str;
    };
    return { store, ...toRefs(data), data, go, getLabels };
  },
};
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
