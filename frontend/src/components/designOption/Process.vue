<template>
  <td>
    <MySelect
      v-model="formData.name"
      :options="process_names"
      valueKey="value"
      textKey="text"
    ></MySelect>
  </td>
  <td>
    <MyInput v-model="formData.duration.val" inputType="number"></MyInput>
  </td>
  <td>
    <MySelect v-model="formData.duration.unit" :options="timeUnits"></MySelect>
  </td>
  <td>
    <button class="btn btn-danger" @click="deleteSelf">删除</button>
  </td>
</template>
<script scope>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import { process_ceb_names, process_cip_names } from "./js";
import MySelect from "@/components/ui/MySelect";
import MyInput from "@/components/ui/MyInput";

export default defineComponent({
  components: { MySelect, MyInput },
  props: {
    process_index: { required: true, type: Number },
    oneclean_index: { required: true, type: Number },
  },
  setup(props) {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const cleanName = inject("cleanName");
    // 获取 formData
    const Clean = storeLocal.state.fd.options[cleanName];
    const oneClean = Clean.oneclean_list[props.oneclean_index];
    const process_list = oneClean.process_list;
    const formData = process_list[props.process_index];
    let process_names = [];
    if (cleanName === "ceb") {
      process_names = process_ceb_names;
    } else if (cleanName === "cip") {
      process_names = process_cip_names;
    }
    const timeUnits = ["秒", "分钟", "小时", "seconds", "minutes", "hours"];
    const deleteSelf = () => {
      process_list.splice(props.process_index, 1);
    };
    return {
      storeLocal,
      formData,
      store,
      urlName,
      process_ceb_names,
      process_names,
      timeUnits,
      deleteSelf,
    };
  },
});
</script>