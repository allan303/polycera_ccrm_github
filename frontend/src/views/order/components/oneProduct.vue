<template>
  <div class="card mt-2">
    <div class="card-body">
      <div class="row">
        <h5 class="card-title text-primary">
          {{ $t("same.product") }}-{{ index + 1 }}
        </h5>
        <FormAutoSelect
          v-model="product_sid"
          :options="store.state.cacheInfo.product"
          v-if="urlName !== 'read'"
          :label="$t('same.product')"
          :col="{ md: 12 }"
          valueKey="sid"
          :textKey="['name', 'model']"
        ></FormAutoSelect>
        <FormAutoSelect
          v-model="formData.model"
          :options="store.state.cacheInfo.product"
          disabled
          v-if="urlName === 'read'"
          :label="$t('same.product')"
          :col="{ md: 12 }"
          valueKey="model"
          :textKey="['name', 'model']"
        ></FormAutoSelect>
        <FormInput
          v-model="formData.unit_price"
          :disabled="urlName === 'read'"
          inputType="number"
          :label="$t('same.unit_price')"
        ></FormInput>

        <FormInput
          v-model="formData.nums"
          :disabled="urlName === 'read'"
          inputType="number"
          :label="`${$t('same.nums')}(${formData.unit || 'pcs'})`"
        ></FormInput>
        <FormInput
          :modelValue="numeral(price).format('0,0.00')"
          :label="$t('same.price')"
          disabled
          v-if="canReadPrice"
        ></FormInput>
        <FormTextarea
          v-model="formData.description"
          :disabled="urlName === 'read'"
          :rows="2"
          :col="{ md: 12 }"
          :label="$t('same.description')"
        ></FormTextarea>
      </div>
      <div class="text-end">
        <FormButton
          btnClass="card-link btn-danger"
          @click="
            confirmDo($t('msg.confirm', { v: $t('actions.delete') }), onDelete)
          "
          :disabled="urlName === 'read'"
          label="删除"
          position="right"
        ></FormButton>
      </div>
    </div>
  </div>
</template>
<script>
import { watch, computed, defineComponent, inject, ref } from "vue";
import { useStore } from "@/main";
import { confirmDo } from "@/myjs";
import FormAutoSelect from "@/components/ui/FormAutoSelect";
import FormInput from "@/components/ui/FormInput";
import FormTextarea from "@/components/ui/FormTextarea";
import FormButton from "@/components/ui/FormButton";
export default defineComponent({
  components: { FormAutoSelect, FormInput, FormTextarea, FormButton },
  //父 传入 一个 product
  props: {
    index: { type: Number },
  },
  setup(props) {
    const storeLocal = inject("storeLocal");
    const products = storeLocal.state.fd.products;
    const product_sid = ref("");
    const formData = products[props.index];
    const urlName = inject("urlName");
    const numeral = inject("numeral");
    const store = useStore();
    const price = computed(
      () => Number(formData.unit_price) * Number(formData.nums)
    );
    //当前选择的产品
    const selectedProduct = computed(() => {
      for (let item of store.state.cacheInfo.product) {
        if (product_sid.value === item.sid) {
          return item;
        }
      }
      return {};
    });

    const onDelete = () => {
      //删除 本项
      products.splice(props.index, 1);
    };
    const canReadPrice = computed(() => {
      if (store.state.cu.is_su) {
        return true;
      } else if (store.state.cu.sid === formData.owner_sid) {
        return true;
      }
      return false;
    });
    //总价
    watch(
      () => product_sid.value,
      () => {
        formData.description = selectedProduct.value.description;
        formData.unit = selectedProduct.value.unit;
        formData.name = selectedProduct.value.name;
        formData.model = selectedProduct.value.model;
      }
    );

    return {
      store,
      selectedProduct,
      onDelete,
      confirmDo,
      numeral,
      urlName,
      formData,
      price,
      products,
      product_sid,
      canReadPrice,
    };
  },
});
</script>