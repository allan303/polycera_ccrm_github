//Author : Jack Li
//Email  : allanth3@163.com
//Date   : 2021-07-20
import { reactive, readonly } from 'vue';
import { createState, } from './state'
import { createActions } from './actions'
import { createGetters } from './getters';
// 创建 Symbol：全局唯一key值
// export const symbolStore = Symbol('store');
// Store工厂函数，用于创建Store {state, actions}
export const createStore = () => {
  //定义需要统一保存的 state
  let state = reactive(createState())
  const actions = createActions(state)
  //专门存储 {value:label}
  const getters = createGetters(state)
  // 最终为 function合集 actions + 状态state, State 为 Readonly
  return { actions, getters, state: readonly(state) };
}
// fn : 使用state(inject 通过 Symbol key找到唯一的state)
// export const useStore = () => inject(symbolStore);
// const storeInstance = createStore()

