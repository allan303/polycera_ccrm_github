<template>
  <StandardIndex :items="items" :useSearch="false"></StandardIndex>
</template>

<script scope>
import StandardIndex from "@/components/StandardIndex";

export default {
  components: { StandardIndex },
  setup() {
    const items = [
      { label: "auth.profile", route: "/auth/myprofile" },
      { label: "auth.changePwd", route: "/auth/change-password" },
    ];

    return { items };
  },
};
</script>