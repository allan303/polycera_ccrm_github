<template>
  <td>
    <MySelect
      :options="store.state.cacheInfo.config.chem"
      textKey="text"
      valueKey="value"
      v-model="formData.name"
    ></MySelect>
  </td>
  <td>
    <MyInput v-model="formData.chem_wt" inputType="number"></MyInput>
  </td>
  <td>
    <MyInput v-model="formData.dosing_wt" inputType="number"></MyInput>({{
      numeral(formData.dosing_wt * 10000).format("0,0")
    }}
    mg/L)
  </td>
  <td>
    <MyInput v-model="formData.solid_price_per_kg" inputType="number"></MyInput>
    (为100%纯度单价，留空采用市场价)
  </td>
  <td>
    <button class="btn btn-danger" @click="deleteSelf">删除</button>
    <!-- <MyButton @click="deleteSelf" label="删除" btnClass="btn-danger"></MyButton> -->
  </td>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
import MyInput from "@/components/ui/MyInput";
import MySelect from "@/components/ui/MySelect";
// "chem_wt": 20.0,
// "dosing_wt": 0.4,
// "name": "naoh",
export default defineComponent({
  props: {
    oneclean_index: { required: true, type: Number },
    chem_dosing_index: { required: true, type: Number },
  },
  components: { MyInput, MySelect },
  setup(props) {
    const store = useStore();
    const numeral = inject("numeral");
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const cleanName = inject("cleanName");
    // 获取 formData
    const Clean = storeLocal.state.fd.options[cleanName]; //CEB or CIP
    const oneClean = Clean.oneclean_list[props.oneclean_index]; // oneclean_list[0]

    const chem_doings = oneClean.chem_dosings;
    const formData = chem_doings[props.chem_dosing_index];
    const deleteSelf = () => {
      chem_doings.splice(props.chem_dosing_index, 1);
    };
    return { storeLocal, formData, store, urlName, deleteSelf, numeral };
  },
});
</script>