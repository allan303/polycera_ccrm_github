<template>
  <StandardIndex>
    <div class="btn-group">
      <MyButton
        small
        :label="$t('role.saveToJson')"
        @click="saveToJson"
        btnClass="btn-secondary"
      ></MyButton>
    </div>
  </StandardIndex>
</template>

<script scope>
import StandardIndex from "@/components/StandardIndex";
import MyButton from "@/components/ui/MyButton";
import { useAxios } from "@/main";
export default {
  components: { StandardIndex, MyButton },
  setup() {
    const items = [
      // { label: "我的档案", route: "/post/create" },
      // { label: "修改密码", route: "/post/change-password" },
    ];
    const axios = useAxios();
    const saveToJson = () => {
      axios({
        method: "post",
        url: "/role/save-to-json",
      }).then((res) => {
        alert(res.data.msg);
      });
    };
    return { items, saveToJson };
  },
};
</script>