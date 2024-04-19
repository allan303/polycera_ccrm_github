import { reactive } from 'vue';
export const readUrlDict = {
    // project_sid: "name",
    // oem_sid: "name",
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
};
import { createData, createActions, createGetters } from '@/components/designOption/js';


export const createStore = () => {
    const state = reactive({
        fd: createData(),
        tabs: ["design.base", 'design.raw_flow', "design.other_info", "design.main_balance",
            "design.backwash", "design.cir", "design.backflow", "design.ceb", "design.cip", "design.pumps",
            "design.dosing", "design.tanks",],
        tabsNoCreate: [],
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
