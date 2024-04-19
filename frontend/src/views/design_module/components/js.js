export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值

};

export const membrane_types = [
    { text: '超滤', value: 'uf' },
    { text: '纳滤', value: 'nf' },
    { text: '反渗透', value: 'ro' },
    { text: '微滤', value: 'mf' },
]

export const module_types = [
    '卷式膜', '中空纤维', '平板膜', '管式膜', '碟片式', '蜂窝'
]

export const sizes = [
    8080, 8040, 4040, 2540, 1812
]
//以下为样板代码
import { reactive } from 'vue';

const createData = () => {
    return {
        "sid": "",
        "create_time_local": null,
        "update_time_local": null,
        "is_deleted": false,
        "name": "",
        "material": "",
        "membrane_type": "",
        "module_type": "",
        "brand": "",
        "model": "",
        "fa": 0,
        "is_contained_pv": false,
        "flux_per_bar_25": 80,
        "liter_inside": 20,
        "spacer_mil": 0,
        "module_size": "",
        "rej_dt": {},
        "description": ""
    }

}

// export const formData = reactive(createData())
const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["same.name", "required", state.fd.name],
                ["product.flux_per_bar_25", "required", state.fd.flux_per_bar_25],
                ["product.flux_per_bar_25", "gt", state.fd.flux_per_bar_25, 0],
                ["product.fa", "gt", state.fd.fa, 0],
                ["product.fa", "required", state.fd.fa],
                ["product.membrane_type", "required", state.fd.membrane_type],
                ["product.module_type", "required", state.fd.module_type],
                ["product.model", "required", state.fd.model],
                ["product.brand", "required", state.fd.brand],
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
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
