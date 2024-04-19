export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
    project_sid: "name",
    oem_sid: "name",
    contact_sid: "name",
};


export const createOneProductData = () => {
    return {
        "brand": "Polycera",
        "description": "",
        "unit_price": 0,
        "unit": "",
        "nums": 1,
        "name": "",
        "model": ""
    }
}


//以下为样板代码
import { reactive } from 'vue';

const createData = () => {
    return {
        "sid": "",
        "create_time_local": "",
        "update_time_local": "",
        "is_deleted": false,
        "owner_sid": "",
        "order_date": null,
        "name": "",
        "oem_sid": "",
        "project_sid": "",
        "contact_sid": "",
        "remark": "",
        "products": [],
        "payment_term": "100%全款",
        "shipment_term": "1周内",
        "shipment_contact": {
            "name": "",
            "phone": "",
            "address": ""
        },
        "invoice_contact": {
            "name": "",
            "phone": "",
            "address": ""
        },
        "price": "",
        "price_cn": "",
        status: "",
        share_list: []
    }
}

// export const formData = reactive(createData())
const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["models.oem", "required", state.fd.oem_sid],
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
        tabs: ["same.detail", "order.products",],
        tabsNoCreate: ['models.orderUpdate', "models.post"],
    })
    const actions = createActions(state)
    //专门存储 {value:label}
    const getters = createGetters(state)
    // 最终为 function合集 actions + 状态state, State 为 Readonly
    return { actions, getters, state };
}
