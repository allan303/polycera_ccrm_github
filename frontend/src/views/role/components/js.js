import { reactive } from 'vue';


export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
};

export const defaulPerm = () => {
    //针对普通用户的基本权限
    return {
        "auth": {},
        "project": {
            "create": "me",
            "read": "me",
            "edit": "me",
            "delete": "me",
            "clone": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me",
            "download_many": "me",
            "merge": "me"
        },
        "oem": {
            "create": "me",
            "read": "me",
            "edit": "me",
            "delete": "me",
            "clone": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me",
            "download_many": "me",
            "merge": "me"
        },
        "contact": {
            "create": "me",
            "read": "me",
            "edit": "me",
            "delete": "me",
            "clone": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me",
            "download_many": "me",
            "merge": "me"
        },
        "pilot": {
            "read": "total",
            "edit": "me",
            "delete": "me",
            "clone": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me",
            "merge": "me"
        },
        "post": {
            "create": "me",
            "read": "me",
            "edit": "me",
            "delete": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me",
            "download_many": "me",
        },
        "design": {
            "read": "total",
            "edit": "me",
            "delete": "me",
            "clone": "me",
            "dashboard": "me",
            "assign": "me",
            "download_one": "me"
        },
        "standard_design": {
            "create": "me",
            "read": "total",
            "edit": "me",
            "delete": "me",
            "dashboard": "total",
            "download_one": "me"
        },
        'product': {
            "read": "total",
        },
        'design_module': {
            "read": "total",
        }
    }
}

export const defaultPermModel = () => {
    return {
        'create': 'me',
        'read': 'me',
        'edit': 'me',
        'delete': 'me',
    }
}

//以下为样板代码
const createData = () => {
    return {
        "sid": "",
        "create_time_local": "",
        "update_time_local": "",
        "is_deleted": false,
        "name": "",
        "remark": "",
        "perm": defaulPerm()
    }
}

// export const formData = reactive(createData())

const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["same.name", "required", state.fd.name],
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
        tabs: ["same.detail", "role.perm",],
        tabsNoCreate: ["models.user"],
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
