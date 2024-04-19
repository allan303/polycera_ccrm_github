<template>
  <StandardIndex :useSearch="false"></StandardIndex>
</template>

<script>
import StandardIndex from "@/components/StandardIndex";

export default {
  components: { StandardIndex },
  setup() {
    const items = [
      // { label: "我的档案", route: "/post/create" },
      // { label: "修改密码", route: "/post/change-password" },
    ];

    return { items };
  },
};
</script>