<template>
  <!-- 用于 编辑 一个action及删除 -->
  <div class="card mt-3">
    <div class="card-header">
      <div class="row">
        <div class="col-md-7">
          <button disabled class="btn text-start text-primary">
            {{ selected.text }}{{ permModel }}
          </button>
        </div>
        <div
          class="col-md-5 d-flex justify-content-end"
          v-if="urlName !== 'read'"
        >
          <div class="dropdown">
            <button
              class="btn dropdown-toggle"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi-plus"></i>{{ $t("actions.add") }}
            </button>
            <ul
              class="dropdown-menu"
              aria-labelledby="dropdownMenuButton1"
              v-if="urlName !== 'read'"
            >
              <li v-for="(action, index) in actionList" :key="index">
                <a
                  class="dropdown-item"
                  @click.prevent="addAction(action.value)"
                >
                  {{ action.text }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div
        class="card-text"
        v-for="(actionScope, actionName) in actions"
        :key="actionName"
      >
        <PermScope :action="actionName" :permModel="permModel"></PermScope>
      </div>
    </div>
    <div class="card-action d-grid" v-if="urlName !== 'read'">
      <button class="btn btn-danger mx-3 mb-2" @click="deletePermModel()">
        {{ $t("actions.delete") }}
      </button>
    </div>
  </div>
</template>
<script>
import { defineComponent, inject, computed } from "vue";
import PermScope from "./PermScope";
import { useStore } from "@/main";

export default defineComponent({
  components: { PermScope },
  props: { permModel: { type: String } },
  setup(props) {
    const urlName = inject("urlName");

    const store = useStore();

    const permOption = store.state.perm_option;

    const storeLocal = inject("storeLocal");
    const perm = storeLocal.state.fd.perm;
    const actions = perm[props.permModel];
    // 已经选择的 筛选
    const selected = computed(() => {
      for (let item of permOption.models) {
        if (item.value === props.permModel) {
          return item;
        }
      }
      return {};
    });
    //method
    const deleteKey = (key) => {
      delete actions[key];
    };
    const deleteAction = (action) => {
      delete actions[action];
    };
    const deletePermModel = () => {
      delete perm[props.permModel];
    };

    // 默认清单
    const actionList = computed(() => {
      //新增权限 去掉已存在
      const ls = permOption.actions;
      const ls1 = [];
      for (let x of ls) {
        if (!actions[x.value]) {
          ls1.push(x);
        }
      }
      return ls1;
    });
    const addAction = (action) => {
      //新增一个操作 如 create
      const ac = {};
      ac[action] = "me";
      Object.assign(actions, ac);
    };

    return {
      deleteKey,
      actions,
      deleteAction,
      actionList,
      addAction,
      urlName,
      deletePermModel,
      selected,
      perm,
      permOption,
    };
  },
});
</script>