<template>
  <div class="row mt-3">
    <FormInput
      v-model="t"
      :placeholder="$t('config.text') + '...'"
      useDelete
    ></FormInput>
    <FormInput
      v-model="v"
      :placeholder="$t('config.v') + '...'"
      useDelete
      inputType="number"
    ></FormInput>
    <div class="col">
      <button class="btn btn-primary btn-sm mx-2" @click="addVal">
        {{ $t("actions.add") }}
      </button>
    </div>
  </div>
  <div class="row mt-3">
    <ul class="list-group list-group-numbered">
      <li
        class="list-group-item d-flex justify-content-between"
        v-for="(item, index) in formData"
        :key="index"
      >
        <div class="ms-2 me-auto">
          <div class="fw-bold">{{ item.name }} : {{ item.win_percentage }}</div>
        </div>
        <span>
          <button
            class="btn btn-primary btn-sm mx-2"
            @click="arrayMovePre(formData, index)"
          >
            {{ $t("config.up") }}
          </button>
          <button
            class="btn btn-primary btn-sm mx-2"
            @click="arrayMoveNext(formData, index)"
          >
            {{ $t("config.down") }}
          </button>
          <button class="btn btn-danger btn-sm mx-2" @click="deleteVal(index)">
            {{ $t("actions.delete") }}
          </button>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { computed, inject, reactive, toRefs } from "vue";
import { useStore } from "@/main";
import FormInput from "@/components/ui/FormInput";
import { arrayMoveNext, arrayMovePre } from "@/myjs";

export default {
  components: { FormInput },
  props: {
    keyName: { type: String, required: true },
  },
  setup(props) {
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const formData = computed(() => storeLocal.state.fd[props.keyName]);
    const data = reactive({
      t: "",
      v: "",
    });
    const addVal = () => {
      formData.value.push({ name: data.t, win_percentage: data.v });
    };
    const deleteVal = (index) => {
      formData.value.splice(index, 1);
    };
    return {
      formData,
      store,
      urlName,
      addVal,
      deleteVal,
      ...toRefs(data),
      arrayMoveNext,
      arrayMovePre,
    };
  },
};
</script>
