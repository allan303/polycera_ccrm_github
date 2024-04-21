<template>
  <!-- 显示list 信息 -->
  <div class="row mb-2">
    <div class="col-6">
      <p class="">
        <small>
          {{ $t("common.totalItem", { count: count }) }} |
          {{ $t("common.thisPage", { count: count_this_page }) }} |
          {{ $t("common.totalPage", { count: Math.ceil(count / perPage) }) }}
        </small>
      </p>
    </div>
    <div class="col-6 text-end">
      <button
        class="btn btn-primary btn-sm"
        data-bs-toggle="collapse"
        href="#collapseContent"
        role="button"
      >
        {{ $t("common.show") }}
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col-12" id="collapseContent">
      <!-- 最近几天 -->
      <div class="row mb-2">
        <div class="col-lg-6 mb-2">
          <div class="input-group">
            <input
              type="radio"
              class="btn-check"
              autocomplete="off"
              disabled
              id="start"
            />
            <label class="btn btn-warning" for="start">{{
              $t("common.recent")
            }}</label>
            <input
              class="form-control"
              type="number"
              v-model="recent_days"
              :placeholder="`${$t('common.asCreateTime')}...`"
            />
            <input
              type="radio"
              class="btn-check"
              autocomplete="off"
              disabled
              id="day"
            />
            <label class="btn btn-warning" for="day" disabled>
              {{ $t("common.days") }}
            </label>
          </div>
        </div>
        <div class="col-lg-6 mb-2 text-end">
          <div class="btn-group" role="group" aria-label="Basic example">
            <button
              type="button"
              class="btn btn-outline-primary ms-1"
              @click="OnRecent(1)"
            >
              1{{ $t("common.day") }}
            </button>
            <button
              type="button"
              class="btn btn-outline-primary ms-1"
              @click="OnRecent(7)"
            >
              7{{ $t("common.days") }}
            </button>
            <button
              type="button"
              class="btn btn-outline-primary ms-1"
              @click="OnRecent(30)"
            >
              30{{ $t("common.days") }}
            </button>
            <button
              type="button"
              class="btn btn-outline-primary ms-1"
              @click="OnRecent(90)"
            >
              90{{ $t("common.days") }}
            </button>
          </div>
        </div>
      </div>
      <!-- 时间范围 -->
      <div class="row mb-2">
        <div class="col-lg-6 mb-2">
          <div class="input-group">
            <input
              type="radio"
              class="btn-check"
              autocomplete="off"
              disabled
              id="start"
            />
            <label class="btn btn-warning" for="start">{{
              $t("common.start")
            }}</label>
            <input class="form-control" type="date" v-model="start" />
          </div>
        </div>
        <div class="col-lg-6 mb-2">
          <div class="input-group">
            <input
              type="radio"
              class="btn-check"
              autocomplete="off"
              disabled
              id="start"
            />
            <label class="btn btn-warning" for="start">
              {{ $t("common.end") }}
            </label>
            <input class="form-control" type="date" v-model="end" />
          </div>
        </div>
      </div>
      <!-- 筛选及搜索 -->
      <div class="row mb-2">
        <div class="col-lg-6 mb-2">
          <div class="input-group">
            <input type="radio" class="btn-check" autocomplete="off" disabled />
            <label class="btn btn-warning" for="btnradio0">{{
              $t("common.sort")
            }}</label>
            <select class="form-select" v-model="order_by">
              <option v-for="(text, v) in orderKeywords" :key="v" :value="v">
                {{ text }}
              </option>
            </select>
            <div
              class="btn-group"
              role="group"
              aria-label="Basic checkbox toggle button group"
            >
              <input
                type="checkbox"
                class="btn-check"
                id="btncheck1"
                autocomplete="off"
                v-model="desc"
              />
              <label class="btn btn-warning" for="btncheck1">
                <!-- {{ desc ? "倒序" : "正序" }} -->
                <i class="bi-arrow-down" v-if="desc"></i>
                <i class="bi-arrow-up" v-else></i>
              </label>
            </div>
          </div>
        </div>

        <div class="col-lg-6 mb-2">
          <div class="input-group">
            <input
              type="text"
              class="form-control"
              v-model="searchKeyword"
              :placeholder="`${$t('common.search')}...`"
              @keyup.enter="onSearch"
            />
            <button class="btn btn-primary" @click="onSearch">
              {{ $t("common.search") }}
            </button>
            <!-- modal button -->
            <button
              class="btn btn-secondary"
              v-if="canDownloadMany"
              data-bs-toggle="modal"
              data-bs-target="#downloadManyModal"
            >
              {{ $t("actions.download") }}
            </button>
            <button class="btn btn-warning" @click="clearSearch">
              {{ $t("common.reset") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- download-many Modal -->
  <!-- Modal -->
  <div
    class="modal fade"
    id="downloadManyModal"
    tabindex="-1"
    aria-labelledby="downloadManyModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="downloadManyModalLabel">
            {{ $t("actions.download") }}
          </h5>
        </div>
        <div class="modal-body">
          <div class="btn-group" v-if="canDownloadMany">
            <button class="btn btn-primary" @click="goDownloadMany('excel')">
              {{ $t("actions.downloadExcel") }}
            </button>
            <button class="btn btn-success" @click="goDownloadMany('word')">
              {{ $t("actions.downloadWord") }}
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn" data-bs-dismiss="modal">
            {{ $t("common.close") }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- pagination -->
  <div class="row mb-2">
    <div class="col-3">
      <button class="btn btn-success" @click="fetchListItems">
        <i class="bi-arrow-clockwise"></i> {{ $t("common.refresh") }}
      </button>
    </div>
    <div class="col-9" v-if="count">
      <StandardPagination
        :count="count"
        :count_this_page="count_this_page"
        v-model:perPage="perPage"
        v-model:currentPage="currentPage"
        @update_currentPage_perPage="update_currentPage_perPage"
      ></StandardPagination>
    </div>
  </div>
  <!-- item list -->
  <slot></slot>
  <div class="row mb-2" v-if="!count">
    <div class="col-12">
      <h1 class="text-muted">{{ $t("common.noResult") }}...</h1>
    </div>
  </div>
  <!-- 底部pagination -->
  <div class="row mb-2" v-if="count">
    <div class="col-12">
      <StandardPagination
        :count="count"
        :count_this_page="count_this_page"
        v-model:perPage="perPage"
        v-model:currentPage="currentPage"
        @update_currentPage_perPage="update_currentPage_perPage"
      ></StandardPagination>
    </div>
  </div>
</template>

<script scope>
import {
  reactive,
  watch,
  toRefs,
  onMounted,
  computed,
  defineComponent,
  provide,
} from "vue";
// import ListItemOne from "./ListItemOne.vue";
import StandardPagination from "@/components/StandardPagination";
import {
  confirmDo,
  isObjectChanged,
  downloadReport,
  can,
  getTodayStr,
} from "@/myjs";
import { useRoute, useRouter } from "vue-router";
import { useAxios, useStore } from "@/main";
export default defineComponent({
  components: { StandardPagination },
  props: {
    listScope: { required: true, type: String },
    filter_dt_and: { type: Object, default: null },
    urlModel: { type: String, default: null },
  },
  setup(props) {
    //防止 warning （传递到btns）
    provide("isList", true);
    //data 结构，最终通过toRefs
    const data = reactive({
      count: 0,
      count_this_page: 0,
      objs: [], // 子组件获取，ref传给父组件
      // 以下为 可以传入
      perPage: 20,
      searchKeyword: "",
      currentPage: 1,
      order_by: "create_time",
      desc: true,
      start: null,
      end: null,
      recent_days: null,
      lastSearch: {}, //记录当前搜索状态
    });
    const axios = useAxios();
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const modelName = computed(() =>
      props.urlModel ? props.urlModel : route.meta.model
    );
    // 搜索关键字选项
    const orderKeywords = computed(() => {
      if (store.state.cacheInfo.order_keywords) {
        return store.state.cacheInfo.order_keywords[modelName.value];
      }
      return {};
    });
    const listQueryData = computed(() => {
      // 用于listQueryData，fetch data和 download_list
      return {
        scope: props.listScope,
        page: data.currentPage,
        keyword: data.searchKeyword.trim(),
        per_page: data.perPage,
        order_by: data.order_by,
        desc: data.desc ? 1 : 0,
        start: data.start,
        end: data.end,
        recent_days: data.recent_days,
        filter_dt_and: props.filter_dt_and,
        use_workgroup: true,
        workgroup_sid: store.state.local.workgroup_sid,
      };
    });
    const fetchListItems = () => {
      //fetch时 仅仅需要 到同一个api进行list_query,只要传入scope即可
      // console.log(listQueryData.value);
      axios({
        method: "post",
        url: `/${modelName.value}/list-paginate`,
        data: listQueryData.value,
      }).then((res) => {
        Object.assign(data, res.data);
      });
    };
    const goDownloadMany = (fileType) => {
      const file_type = fileType || "word";
      const method = "post";
      const url = `/${modelName.value}/download-many/${file_type}`;
      const data = listQueryData.value;

      let filename = `${getTodayStr()}_${String(
        modelName.value
      ).toUpperCase()}报表`;
      if (file_type === "excel") {
        filename = filename + ".xlsx";
      } else {
        filename = filename + ".docx";
      }
      downloadReport(axios, method, url, data, filename);
      return false;
    };
    const canDownloadMany = computed(() => {
      if (!["project", "post"].includes(modelName.value)) {
        return false;
      }
      if (props.listScope === "me") {
        //自己的列表 可以下载many
        return can(store.state.cu, modelName.value, "download_many", "me", "");
      } else {
        //share,total等需要 download_many total 权限
        return can(
          store.state.cu,
          modelName.value,
          "download_many",
          "total",
          ""
        );
      }
    });
    provide("fetchListItems", fetchListItems);
    const setLastSearch = () => {
      // 记录上一次搜索状态
      data.lastSearch = {
        searchKeyword: data.searchKeyword.trim(),
        order_by: data.order_by,
        desc: data.desc,
        start: data.start,
        end: data.end,
        recent_days: data.recent_days,
      };
    };
    const currentSearch = computed(() => {
      // 获取当前搜索状态
      return {
        searchKeyword: data.searchKeyword.trim(),
        order_by: data.order_by,
        desc: data.desc,
        start: data.start,
        end: data.end,
        recent_days: data.recent_days,
      };
    });
    const onSearch = () => {
      //关键字搜索
      if (!isObjectChanged(data.lastSearch, currentSearch.value)) {
        console.log("搜索条件相等，不操作");
        return false;
      } else {
        setLastSearch();
        data.currentPage = 1;
        fetchListItems();
      }
    };
    const clearSearch = () => {
      //清除搜索
      data.searchKeyword = "";
      data.desc = true;
      data.order_by = "create_time";
      data.start = null;
      data.end = null;
      data.recent_days = null;
      onSearch();
    };

    const update_currentPage_perPage = (currentPage, perPage) => {
      //用于 子组件 pagination emit
      data.currentPage = currentPage;
      data.perPage = perPage;
    };
    const OnRecent = (days) => {
      data.recent_days = days;
      // onSearch();
    };

    watch(
      () => data.currentPage,
      () => {
        fetchListItems();
      }
    );
    watch(
      () => data.perPage,
      () => {
        fetchListItems();
      }
    );
    // axios
    onMounted(() => {
      fetchListItems();
      setLastSearch();
    });
    return {
      ...toRefs(data),
      router,
      fetchListItems,
      confirmDo,
      update_currentPage_perPage,
      onSearch,
      clearSearch,
      OnRecent,
      orderKeywords,
      currentSearch,
      store,
      modelName,
      canDownloadMany,
      goDownloadMany,
      listQueryData,
    };
  },
});
</script>
