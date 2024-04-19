export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值

};


//以下为样板代码
import { reactive } from 'vue';

const createData = () => {
    return {
        sid: "",
        create_time_local: "",
        update_time_local: "",
        is_deleted: false,
        owner_sid: "",
        name: "",
        location: "",
        oemtype: "",
        company_code: "",
        company_address: "",
        company_bank: "",
        company_bank_account: "",
        company_telephone: "",
        company_zipcode: "",
        remark: "",
        share_list: []
    }
}

// export const formData = reactive(createData())
const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["same.name", "required", state.fd.name],
                ["same.type", "required", state.fd.oemtype],
                // ["日志内容", "len_gt", formData.body, 5],
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
        tabs: ["same.detail",],
        tabsNoCreate: ["models.post", "models.contact", "models.project", "models.order", "models.design"],
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
