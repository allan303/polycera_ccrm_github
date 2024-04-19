
export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
    'role_sid': 'name'
};



//以下为样板代码
import { reactive } from 'vue';
export const createData = () => {
    return {
        "company": "polycera",
        "phone": "",
        "name": "",
        "name_en": "",
        "title": "",
        "country": "China",
        "province": "shanghai",
        "gender": "",
        "sid": "",
        "create_time_local": "",
        "update_time_local": "",
        "is_deleted": false,
        "username": "",
        "email": "",
        "role_sid": "",
        "is_su": false,
        "last_seen_local": "",
        "remark": "",
        "perm": {},
        "user_config": { use_half: false, locale: 'zh' }
    }
}

// export const formData = reactive(createData())
const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["user.name", "required", state.fd.name],
                ["user.username", "required", state.fd.username],
                ["models.role", "required", state.fd.role_sid],
                ["models.workgroup", "required", state.fd.workgroup_sid],
            ]
        },
        validateFormDataNonStandard() {
            const fd = state.fd
            if (!fd.email && !fd.phone) {
                return "user.no_email_phone"
            }
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
        tabsNoCreate: ["models.project", "models.oem", "models.contact", "models.post"],
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
