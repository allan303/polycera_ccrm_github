<template>
  <!-- 主内容 -->
  <StandardCreateComponent :readUrlDict="readUrlDict" :urlModel="urlModel">
    <template v-slot:tab0>
      <FormAutoSelect
        :disabled="urlName === 'read'"
        :options="cacheInfo.user"
        :label="$t('same.share_list')"
        v-model="formData.share_list"
        :col="{ md: 12 }"
        mode="multiple"
        :default_content="[{ sid: 'all', name: $t('same.allUser') }]"
      ></FormAutoSelect>
      <FormInput
        :modelValue="
          moment(formData.create_time_local).format('YYYY-MM-D HH:MM')
        "
        :label="$t('same.create_time')"
        v-if="urlName !== 'create'"
        disabled
      ></FormInput>
      <FormInput
        :modelValue="
          moment(formData.update_time_local).format('YYYY-MM-D HH:MM')
        "
        :label="$t('same.update_time')"
        v-if="urlName !== 'create'"
        disabled
      ></FormInput>
      <FormSelect
        :modelValue="formData.owner_sid"
        :label="$t('same.owner')"
        :options="cacheInfo.user"
        disabled
        v-if="urlName !== 'create'"
      ></FormSelect>
      <FormInput
        :modelValue="formData.name"
        :label="$t('order.name')"
        disabled
        v-if="urlName !== 'create'"
      ></FormInput>
      <div class="row mt-2">
        <FormCheckbox
          v-model="formData.free"
          :label="$t('order.free')"
          :disabled="urlName === 'read'"
        ></FormCheckbox>
      </div>
      <FormInput
        :modelValue="numeral(formData.price).format('0,0.00')"
        :label="$t('order.price')"
        disabled
        v-if="urlName === 'read'"
      ></FormInput>
      <FormInput
        :modelValue="formData.price_cn"
        :label="$t('order.price_cn')"
        disabled
        v-if="urlName === 'read'"
      ></FormInput>
      <FormSelect
        v-model="formData.status"
        :options="cacheInfo.config.order_status"
        :label="$t('order.status')"
        :disabled="urlName !== 'create'"
      ></FormSelect>
      <FormInput
        inputType="date"
        v-model="formData.order_date"
        :label="$t('order.order_date')"
        :disabled="urlName !== 'create'"
      ></FormInput>
      <FormAutoSelect
        v-model="formData.oem_sid"
        :options="cacheInfo.oem"
        :label="$t('same.related', { v: $t('models.oem') })"
        textKey="name"
        mode="single"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormAutoSelect
        v-model="formData.project_sid"
        :options="cacheInfo.project"
        :label="$t('same.related', { v: $t('models.project') })"
        :disabled="urlName === 'read'"
      ></FormAutoSelect>
      <FormAutoSelect
        v-model="formData.contact_sid"
        :options="cacheInfo.contact"
        :label="$t('same.related', { v: $t('models.contact') })"
        :disabled="urlName === 'read'"
        textKey="name"
      ></FormAutoSelect>
      <FormTextarea
        v-model="formData.payment_term"
        :label="$t('order.payment_term')"
        :disabled="urlName === 'read'"
        :rows="1"
        :col="{ md: 12 }"
      ></FormTextarea>
      <FormTextarea
        v-model="formData.shipment_term"
        :label="$t('order.shipment_term')"
        :disabled="urlName === 'read'"
        :rows="1"
        :col="{ md: 12 }"
      ></FormTextarea>
      <div class="col-12">
        <p class="text-primary mt-3">
          <strong>{{ $t("order.shipment_contact") }}:</strong>
        </p>
      </div>
      <FormInput
        v-model="formData.shipment_contact.name"
        :label="$t('order.receiver')"
        v-if="formData.shipment_contact"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-if="formData.shipment_contact"
        v-model="formData.shipment_contact.phone"
        :label="$t('user.phone')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-if="formData.shipment_contact"
        v-model="formData.shipment_contact.address"
        :label="$t('contact.address')"
        :col="{ md: 12 }"
        :disabled="urlName === 'read'"
      ></FormInput>
      <div class="col-12">
        <p class="text-primary mt-3">
          <strong>{{ $t("order.invoice_contact") }}:</strong>
        </p>
      </div>
      <FormInput
        v-if="formData.invoice_contact"
        v-model="formData.invoice_contact.name"
        :label="$t('order.receiver')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-if="formData.invoice_contact"
        v-model="formData.invoice_contact.phone"
        :label="$t('user.phone')"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormInput
        v-if="formData.invoice_contact"
        v-model="formData.invoice_contact.address"
        :label="$t('contact.address')"
        :col="{ md: 12 }"
        :disabled="urlName === 'read'"
      ></FormInput>
      <FormTextarea
        v-model="formData.remark"
        :label="$t('same.remark')"
        :col="{ md: 12 }"
        :rows="5"
        :disabled="urlName === 'read'"
      ></FormTextarea>
    </template>
    <template v-slot:tab1>
      <div class="row">
        <div class="clo-6">
          <MyButton
            :label="$t('order.addProduct')"
            @click="addProduct"
            icon="plus-lg"
            :disabled="urlName === 'read'"
          ></MyButton>
        </div>
      </div>
      <FormInput
        :modelValue="numeral(priceTotal).format('0,0.00')"
        :label="$t('order.price')"
        :col="{ md: 12, other: 'text-danger' }"
        disabled
      ></FormInput>
      <!-- 以下为产品清单 -->
      <!-- 如果用index作为key，发现删除products中的项，v-for不重新渲染，改成:key = "item"解决 -->
      <div
        class="col-12"
        v-for="(item, index) in formData.products"
        :key="item"
      >
        <oneProduct :index="index"></oneProduct>
      </div>
    </template>
    <template v-slot:tab2 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="order_update"
        :filter_dt_and="{ order_sid: formData.sid }"
      ></StandardToCreateBtn>
      <OrderUpdateComponent
        listScope="related"
        urlModel="order_update"
        :filter_dt_and="{ order_sid: formData.sid }"
      ></OrderUpdateComponent>
    </template>
    <template v-slot:tab3 v-if="urlName !== 'create'">
      <StandardToCreateBtn
        urlModel="post"
        :filter_dt_and="{ order_sid: formData.sid }"
      ></StandardToCreateBtn>
      <PostListComponent
        listScope="related"
        urlModel="post"
        :filter_dt_and="{ order_sid: formData.sid }"
      ></PostListComponent>
    </template>
  </StandardCreateComponent>
</template>

<script scope>
import { provide, computed, inject } from "vue";
import { useStore } from "@/main";
import StandardCreateComponent from "@/components/StandardCreateComponent";
import FormTextarea from "@/components/ui/FormTextarea";
import FormSelect from "@/components/ui/FormSelect";
import FormInput from "@/components/ui/FormInput";
import MyButton from "@/components/ui/MyButton";
import { readUrlDict, createStore, createOneProductData } from "./js";
import oneProduct from "./oneProduct";
import _ from "lodash";
import FormAutoSelect from "@/components/ui/FormAutoSelect";
import FormCheckbox from "@/components/ui/FormCheckbox";

// 非标
import PostListComponent from "@/views/post/components/ListComponent";
import OrderUpdateComponent from "@/views/order_update/components/ListComponent";
import StandardToCreateBtn from "@/components/StandardToCreateBtn";

export default {
  props: {
    urlName: { required: true },
    urlModel: { type: String, default: null },
  },
  components: {
    StandardCreateComponent,
    FormSelect,
    FormTextarea,
    FormInput,
    MyButton,
    oneProduct,
    PostListComponent,
    StandardToCreateBtn,
    OrderUpdateComponent,
    FormAutoSelect,
    FormCheckbox,
  },
  setup(props) {
    const storeLocal = createStore();
    //注入 createComponent 所有子组件
    provide("storeLocal", storeLocal);
    const formData = storeLocal.state.fd;
    //此item限定条件
    provide("urlName", props.urlName);
    const moment = inject("moment");
    const numeral = inject("numeral");
    const store = useStore();
    const cacheInfo = computed(() => store.state.cacheInfo);

    // 以下为非标
    const priceTotal = computed(() => {
      return _.sumBy(formData.products, function (o) {
        return o.unit_price * o.nums;
      });
    });
    const addProduct = () => {
      formData.products.push(createOneProductData());
    };

    return {
      formData,
      store,
      moment,
      cacheInfo,
      readUrlDict,
      priceTotal,
      numeral,
      addProduct,
    };
  },
};
</script>
