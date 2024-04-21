<template>
  <div class="card border-primary">
    <div :class="'card-header ' + cardHeaderClass">
      <a
        href="#"
        :class="'link-primary fw-bold ' + cardHeaderTextClass"
        @click.prevent="router.push(`/user/read/${formData.owner_sid}`)"
      >
        {{ store.getters.objName("owner_sid", formData.owner_sid) }}
      </a>
      {{ $t("common.createIn") }}
      {{ moment(formData.create_time_local).format("YYYY-MM-D H:mm") }}
      <small class="fst-italic fw-light text-mute text-end"
        >{{ $t("common.editIn") }}
        {{ moment(formData.update_time_local).format("YYYY-MM-D H:mm") }}</small
      >
    </div>
    <!-- 显示关联信息及连接 -->
    <div class="card-body">
      <StandardReadUrls
        :formData="formData"
        :readUrlDict="readUrlDict"
      ></StandardReadUrls>
      <p class="card-text">
        <!-- 以下为 slot -->
        <slot></slot>
      </p>
    </div>
    <!-- 操作按钮 -->
    <div class="text-end">
      <StandardActionBtns
        urlName="read"
        :formData="formData"
        small
        useReadBtn
        :urlModel="urlModel"
      ></StandardActionBtns>
    </div>
  </div>
</template>
<script scope>
import { defineComponent, inject } from "vue";

import { useRouter } from "vue-router";
import StandardActionBtns from "@/components/StandardActionBtns";
import StandardReadUrls from "./StandardReadUrls";
import { useStore } from "@/main";
export default defineComponent({
  props: {
    formData: { type: Object, requried: true },
    readUrlDict: { type: Object },
    urlModel: { type: String, default: null },
    cardHeaderClass: { type: String, default: "" },
    cardHeaderTextClass: { type: String, default: "" },
  },
  components: { StandardActionBtns, StandardReadUrls },
  setup() {
    const moment = inject("moment");
    const router = useRouter();
    const store = useStore();
    return { moment, router, store };
  },
});
</script>
