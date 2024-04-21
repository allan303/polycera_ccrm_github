<template>
  <MyprofileComponent :isEdit="true"></MyprofileComponent>
</template>

<script scope>
import MyprofileComponent from "../components/MyprofileComponent";
export default {
  components: {
    MyprofileComponent,
  },
};
</script>
