<template>
  <div class="row my-2">
    <div :class="btnPostionClass">
      <div class="btn-group me-1">
        <MyButton
          v-if="
            urlName === 'read' && canRead && useReadBtn && modelName !== 'post'
          "
          @click="goRead"
          :label="$t('actions.read')"
          :position="position"
          btnClass="btn-light"
          :small="small"
        ></MyButton>
        <MyButton
          v-if="urlName === 'read' && canEdit && !formData.is_deleted"
          @click="goEdit"
          btnClass="btn-primary"
          :small="small"
          :label="$t('actions.edit')"
        ></MyButton>
        <MyButton
          v-if="urlName !== 'read' && !formData.is_deleted"
          @click="goSubmit"
          btnClass="btn-primary"
          :small="small"
          :label="$t('actions.submit')"
          :position="position"
        ></MyButton>

        <MyButton
          v-if="urlName === 'edit'"
          @click="goRead(true)"
          btnClass="btn-light"
          :small="small"
          :label="$t('actions.cancel')"
        ></MyButton>
        <!-- 这是dropdown按钮，集合复杂功能 -->
        <MyButton
          v-if="urlName === 'read'"
          btnClass="btn-outline-primary dropdown-toggle"
          :label="$t('common.action')"
          :position="position"
          :small="small"
          dataBsToggle="dropdown"
          aria-expanded="false"
        ></MyButton>
        <ul class="dropdown-menu">
          <li v-if="urlName === 'read' && canDelete && !formData.is_deleted">
            <MyButton
              @click="goDelete"
              btnClass="dropdown-item"
              :label="$t('actions.delete')"
            ></MyButton>
          </li>
          <li v-if="urlName === 'read' && canCreateDesignByStandardDesign">
            <MyButton
              @click="goCreateDesignByStandardDesign"
              btnClass="dropdown-item"
              :label="$t('actions.createDesignByStandardDesign')"
            ></MyButton>
          </li>
          <li
            v-if="urlName === 'read' && canDownloadOne && !formData.is_deleted"
          >
            <MyButton
              @click="goDownload"
              btnClass="dropdown-item"
              :label="$t('actions.download')"
              dataBsToggle="modal"
              :dataBsTarget="'#' + downloadModalId"
            ></MyButton>
          </li>
          <li v-if="urlName === 'read' && formData.is_deleted">
            <MyButton
              @click="goUnDelete"
              btnClass="dropdown-item"
              :label="$t('actions.undelete')"
            ></MyButton>
          </li>
          <li v-if="urlName === 'read' && formData.is_deleted">
            <MyButton
              @click="goRealDelete"
              btnClass="dropdown-item"
              :label="$t('actions.realDelete')"
            ></MyButton>
          </li>
          <li
            v-if="
              urlName === 'read' && !formData.is_deleted && modelName === 'user'
            "
          >
            <MyButton
              @click="confirmDo($t('actions.resetPwdConfirm'), goResetPassword)"
              btnClass="dropdown-item"
              :label="$t('actions.resetPwdToEmail')"
            ></MyButton>
          </li>
          <li v-if="urlName === 'read' && canAssign && !formData.is_deleted">
            <MyButton
              btnClass="dropdown-item"
              :label="$t('actions.assign')"
              dataBsToggle="modal"
              :dataBsTarget="'#' + assignModalId"
            ></MyButton>
          </li>
          <li v-if="urlName === 'read' && canMerge && !formData.is_deleted">
            <MyButton
              btnClass="dropdown-item"
              :label="$t('actions.mergeTo')"
              dataBsToggle="modal"
              :dataBsTarget="'#' + mergeModalId"
            ></MyButton>
          </li>
          <slot></slot>
        </ul>
      </div>
    </div>
  </div>
  <!-- 所有modal -->
  <div class="text-start">
    <!-- Modal download -->
    <div
      class="modal fade"
      :id="downloadModalId"
      tabindex="-1"
      aria-labelledby="downloadModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content bg-dark">
          <div class="modal-header">
            <h5 class="modal-title text-white" id="downloadModalLabel">
              {{ $t("msg.downloadWaiting") }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal assign -->
    <div
      class="modal fade"
      :id="assignModalId"
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
              v-model="assignUserSid"
              textKey="name"
              valueKey="sid"
              :col="{ md: 12 }"
            ></FormAutoSelect>
            <button class="btn btn-primary mt-3" @click="goAssign">
              {{ $t("actions.submit") }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal merge -->
    <div
      class="modal fade"
      :id="mergeModalId"
      tabindex="-1"
      aria-labelledby="mergeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="mergeModalLabel">
              {{ $t("actions.merge") }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <FormAutoSelect
              :options="store.state.cacheInfo[modelName]"
              :label="'[' + formData.name + ']' + $t('actions.mergeTo')"
              v-model="mergeSid"
              textKey="name"
              valueKey="sid"
              :col="{ md: 12 }"
            ></FormAutoSelect>
            <button class="btn btn-primary mt-3" @click="goMerge">
              {{ $t("actions.submit") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script scope>
import { useRoute, useRouter } from "vue-router";
import { can, validateForm, downloadReport, confirmDo } from "@/myjs";
import { computed, defineComponent, inject, reactive, toRefs } from "vue";
import { useAxios, useStore } from "@/main";
import MyButton from "./ui/MyButton.vue";
// import FormButton from "./ui/FormButton.vue";
import FormAutoSelect from "./ui/FormAutoSelect.vue";
export default defineComponent({
  props: {
    urlName: { type: String, default: "" },
    position: { type: String, default: "" },
    small: { type: Boolean, default: false },
    useReadBtn: { type: Boolean, default: false },
    urlModel: { type: String, default: null },
    formData: { type: Object },
  },
  components: { MyButton, FormAutoSelect },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const axios = useAxios();
    const store = useStore();
    const $t = inject("t");
    const isList = inject("isList");
    const modelName = computed(() => {
      return props.urlModel || route.meta.model;
    });

    const data = reactive({
      assignUserSid: null,
      mergeSid: null,
      downloadModalId: "download" + props.formData.sid,
      assignModalId: "assign" + props.formData.sid,
      mergeModalId: "merge" + props.formData.sid,
    });
    const updateCacheAfter = () => {
      //限定 更新 state cache 的范围
      if (
        [
          "user",
          "project",
          "oem",
          "contact",
          "order",
          "pilot",
          "role",
          "config",
          "design_module",
          "design",
          "standard_design",
          "product",
          "workgroup",
        ].includes(modelName.value)
      ) {
        store.actions.updateCacheInfo(axios, modelName.value);
      }
    };
    const canRead = computed(() => {
      return can(
        store.state.cu,
        modelName.value,
        "read",
        "",
        props.formData.owner_sid,
        props.formData.share_list
      );
    });
    const canEdit = computed(() => {
      return can(
        store.state.cu,
        modelName.value,
        "edit",
        "",
        props.formData.owner_sid
      );
    });
    const canDelete = computed(() => {
      return can(
        store.state.cu,
        modelName.value,
        "delete",
        "",
        props.formData.owner_sid
      );
    });
    const canMerge = computed(() => {
      return (
        can(
          store.state.cu,
          modelName.value,
          "merge",
          "",
          props.formData.owner_sid
        ) && ["project", "oem", "contact", "pilot"].includes(modelName.value)
      );
    });
    const canDownloadOne = computed(() => {
      return (
        ["design", "order", "project"].includes(modelName.value) &&
        can(
          store.state.cu,
          modelName.value,
          "download_one",
          "",
          props.formData.owner_sid
        )
      );
    });
    const canAssign = computed(() => {
      if (
        !can(
          store.state.cu,
          modelName.value,
          "assign",
          "",
          props.formData.owner_sid
        )
      ) {
        return false;
      }
      return ["project", "oem", "contact", "pilot", "design"].includes(
        modelName.value
      );
    });
    //某些模块 不显示read 和 edit
    const showRead = computed(() => {
      if (["project_oem", "project_update"].includes(modelName.value)) {
        return false;
      }
      return true;
    });
    const showEdit = computed(() => {
      if (["project_oem", "project_update"].includes(modelName.value)) {
        return false;
      }
      return true;
    });
    // 只有显示单个Create环境下，才需要 GoSubmit
    // submit
    const storeLocal = inject("storeLocal");
    const goSubmit = () => {
      if (!storeLocal) {
        //没有provide，则代表为List环境，无Submit
        console.log("NO STORELOCAL");
        return false;
      }
      //rules 验证
      let v1 = validateForm($t, storeLocal.actions.getValidateFields());
      //非标准验证
      let v2 = storeLocal.actions.validateFormDataNonStandard();

      if (v1 !== true) {
        return false;
      }
      if (v2 !== true) {
        alert($t(v2));
        return false;
      }
      let url = "";
      if (props.urlName === "create") {
        url = `/${modelName.value}/create`;
      } else if (props.urlName === "edit") {
        url = `/${modelName.value}/edit/${route.params.sid}`;
      }
      axios({
        method: "post",
        url: url,
        data: props.formData,
      }).then((res) => {
        // 更新 cache
        updateCacheAfter();
        const sid = res.data.sid;
        const nexturl = route.query.nexturl;
        if (nexturl) {
          router.push(nexturl);
          return false;
        }
        router.push(`/${modelName.value}/read/${sid}`);
        return false;
      });
    };
    const goRead = (reusePage) => {
      //打开新的页面
      if (reusePage) {
        // 取消的话，不打开新的页面
        router.push(`/${modelName.value}/read/${props.formData.sid}`);
      } else {
        const url = router.resolve(
          `/${modelName.value}/read/${props.formData.sid}`
        );
        window.open(url.href, "_blank");
      }
    };
    const goEdit = () => {
      router.push(`/${modelName.value}/edit/${props.formData.sid}`);
    };
    const fetchListItems = inject("fetchListItems");

    const goDelete = () => {
      const r = confirm("确定删除？");
      if (r) {
        axios({
          method: "post",
          url: `/${modelName.value}/delete-switch/${props.formData.sid}`,
        }).then(() => {
          // 删除需要
          updateCacheAfter();
          //列表页面: 本页刷新
          if (isList) {
            fetchListItems();
            // router.push(route.path + "?tm=" + new Date().getTime());
          }
          //详情页删除，刷新
          else {
            router.go(0);
          }
        });
      }
    };
    const goUnDelete = () => {
      //恢复
      const r = confirm($t("msg.undeleteConfirm"));
      if (r) {
        axios({
          method: "post",
          url: `/${modelName.value}/delete-switch/${props.formData.sid}`,
        }).then(() => {
          // 恢复需要
          updateCacheAfter();
          //列表页面: 本页刷新
          if (isList) {
            fetchListItems();
          }
          //详情页 恢复： 去到 list-deleted
          else {
            router.go(0);
          }
        });
      }
    };
    const goRealDelete = () => {
      const r = confirm("确定彻底删除？");
      if (r) {
        // 完全删除
        axios({
          method: "post",
          url: `/${modelName.value}/real-delete/${props.formData.sid}`,
        }).then(() => {
          //列表页面: 本页刷新
          if (isList) {
            fetchListItems();
          }
          //详情页 删除： 去到 list-deleted
          else {
            router.push(`/${modelName.value}/list-deleted`);
          }
        });
      }
    };
    const goDownload = () => {
      //判断可下载的范围
      if (!["project", "design", "order"].includes(modelName.value)) {
        return false;
      }
      const downloadData = {
        //下载传到后台的参数
        sid: props.formData.sid,
        //通过此处传入tpl_name
        tpl_name: props.formData.downloadOption
          ? props.formData.downloadOption.tpl_name
          : null,
        //可以传入
        download_option: props.formData.downloadOption,
      };
      const method = "post";
      const url = `/${modelName.value}/download-one/${props.formData.sid}`;
      let filename = "CCRM下载.docx";
      if (modelName.value === "design") {
        filename = `Polycera设计_${props.formData.name}.docx`;
      }
      if (modelName.value === "order") {
        filename = `销售合同-${props.formData.name}-${store.getters.objName(
          "oem_sid",
          props.formData.oem_sid
        )}.docx`;
      }
      if (modelName.value === "project") {
        filename = `项目_${props.formData.name}.docx`;
      }
      downloadReport(axios, method, url, downloadData, filename);
    };

    const goResetPassword = () => {
      axios({
        method: "post",
        url: `/user/reset-password/${props.formData.sid}`,
      }).then(() => {
        axios({
          method: "post",
          url: "/auth/default-user-password",
        }).then((res) => {
          // console.log(res.data);
          const pwd = res.data.msg;
          alert($t("actions.resetPwdSuccess", { pwd: pwd }));
        });
      });
    };
    const postAssign = () => {
      axios({
        method: "post",
        url: `/${modelName.value}/assign/${props.formData.sid}/${data.assignUserSid}`,
      }).then(() => {
        //本页刷新
        router.go(0);
      });
    };
    const goAssign = () => {
      // Assign action
      if (!canAssign.value) {
        return false;
      }
      if (!data.assignUserSid) {
        return false;
      }
      if (props.formData.owner_sid === data.assignUserSid) {
        alert($t("msg.alreadyCurrentOwner"));
        return false;
      }
      confirmDo($t("msg.confirm", { v: $t("actions.assign") }), postAssign);
    };
    const postMerge = () => {
      axios({
        method: "post",
        url: `/${modelName.value}/merge/${props.formData.sid}/${data.mergeSid}`,
      }).then((res) => {
        // 删除需要
        updateCacheAfter();
        //列表页面: 本页刷新
        if (isList) {
          fetchListItems();
          // router.push(route.path + "?tm=" + new Date().getTime());
        }
        //详情页合并，去往新合并的项
        else {
          if (res.data.sid) {
            router.push(`/${modelName.value}/read/${data.mergeSid}`);
          }
        }
      });
    };
    const goMerge = () => {
      if (props.formData.sid === data.mergeSid) {
        alert("合并目标为自身，无操作");
        return false;
      }
      if (!data.mergeSid) {
        return false;
      }
      confirmDo(
        $t("msg.confirm", { v: $t("actions.mergeConfirm") }),
        postMerge
      );
    };
    const goCreateDesignByStandardDesign = () => {
      //通过标准设计，新建Design
      const url = router.resolve(
        `/design/create?standard_design=${props.formData.sid}`
      );
      window.open(url.href, "_blank");
    };
    const canCreateDesignByStandardDesign = computed(() => {
      return (
        modelName.value === "standard_design" && !props.formData.is_deleted
      );
    });
    const btnPostionClass = computed(() => {
      if (!props.position) {
        return "col-12";
      } else {
        if (props.position === "right") {
          return "col-12 text-end";
        } else if (props.position === "left") {
          return "col-12 text-start";
        } else if (props.position === "center") {
          return "col-12 text-center";
        }
      }
      return "col-12";
    });
    return {
      goSubmit,
      goRead,
      goEdit,
      goDelete,
      goUnDelete,
      goRealDelete,
      goDownload,
      goResetPassword,
      goAssign,
      goMerge,
      goCreateDesignByStandardDesign,
      canCreateDesignByStandardDesign,
      confirmDo,
      canRead,
      canEdit,
      canDelete,
      canDownloadOne,
      store,
      btnPostionClass,
      showRead,
      showEdit,
      storeLocal,
      modelName,
      canAssign,
      route,
      canMerge,
      ...toRefs(data),
    };
  },
});
</script>
<style scoped>
.primary {
  background-color: #6200ee;
  color: #fff;
}
.secondary {
  background-color: #018786;
  color: #fff;
}
.surface {
  background-color: #fff;
  color: #000;
}
.error {
  background-color: #b00020;
  color: #fff;
}
</style>