export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
    // project_sid: "name",
    // oem_sid: "name",
    // contact_sid: "name",
    order_sid: "name",
    // pilot_sid: "name",
};



//以下为样板代码
import { reactive } from 'vue';

const createData = () => {
    return {
        "sid": "",
        "create_time_local": null,
        "update_time_local": null,
        "is_deleted": false,
        "owner_sid": "",
        "order_sid": "",
        "status": "未签订",
        "remark": "",
    }
}

// export const formData = reactive(createData())
const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["order.status", "required", state.fd.status],
                ["models.order", "required", state.fd.order_sid],
            ]
        },
        validateFormDataNonStandard() {
            return true
        }
    }
}

const createGetters = (state) => {
    return {
        name() { return state.fd.name }
    }
}

// Store中方法只放 操作 fd 或者与fd 有关的，无关的不放
export const createStore = () => {
    const state = reactive({
        fd: createData(),
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
