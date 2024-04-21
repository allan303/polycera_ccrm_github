<template>
  <nav aria-label="Page navigation example">
    <ul class="pagination justify-content-end">
      <li class="page-item">
        <MySelect
          :options="pageOption"
          v-model="perPage1"
          valueKey="value"
          textKey="text"
        ></MySelect>
      </li>
      <li :class="currentPage1 === 1 ? ' page-item disabled' : 'page-item'">
        <a class="page-link btn text-dark" tabindex="-1" @click="currentPage1--"
          ><i class="bi-chevron-left"></i
        ></a>
      </li>
      <li class="page-item">
        <MySelect :options="pageList" v-model="currentPage1"></MySelect>
      </li>
      <li
        :class="currentPage1 === totalPage ? 'page-item disabled' : 'page-item'"
      >
        <a class="page-link btn text-dark" @click="currentPage1++"
          ><i class="bi-chevron-right"></i
        ></a>
      </li>
    </ul>
  </nav>
</template>
<script scope>
import { ref, watch, computed, defineComponent, inject } from "vue";
import MySelect from "@/components/ui/MySelect";
export default defineComponent({
  components: { MySelect },
  props: {
    //需要v-model的参数
    currentPage: { type: Number, default: 1 },
    perPage: { type: Number, default: 20 },
    // 以下仅仅引用
    count: { type: Number, default: 1 },
    count_this_page: { type: Number, default: 1 },
  },
  emits: { update_currentPage_perPage: null },
  setup(props, { emit }) {
    const $t = inject("t");
    const locale = inject("locale");
    const createPageOption = () => {
      let ls = [];
      for (let i of [10, 20, 30, 40]) {
        ls.push({ value: i, text: $t("common.eachPage", { count: i }) });
      }
      return ls;
    };
    const currentPage1 = ref(props.currentPage);
    const perPage1 = ref(props.perPage);
    const clickChangeCurrentPage = (page) => {
      //点击 时候 更改page
      currentPage1.value = page;
    };
    const totalPage = computed(() => {
      return Math.ceil(props.count / props.perPage);
    });
    const pageList = computed(() => {
      const ls = [];
      for (let i = 1; i <= totalPage.value; i++) {
        ls.push(i);
      }
      return ls;
    });
    const pageOption = ref(createPageOption());
    watch(
      () => props.currentPage,
      () => {
        currentPage1.value = props.currentPage;
      }
    );
    watch(
      () => props.perPage,
      () => {
        perPage1.value = props.perPage;
      }
    );
    watch(
      () => perPage1.value,
      (newVal, oldVal) => {
        if (
          Math.ceil(props.count / oldVal) === 1 &&
          Math.ceil(props.count / newVal) === 1
        ) {
          return false;
        }
        currentPage1.value = 1;
        emit("update_currentPage_perPage", currentPage1.value, perPage1.value);
      }
    );
    watch(
      () => currentPage1.value,
      () => {
        emit("update_currentPage_perPage", currentPage1.value, perPage1.value);
      }
    );
    watch(
      () => locale.value,
      () => {
        pageOption.value = createPageOption();
      }
    );
    return {
      currentPage1,
      perPage1,
      pageOption,
      clickChangeCurrentPage,
      totalPage,
      pageList,
    };
  },
});
</script>