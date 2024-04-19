export const readUrlDict = {
    // key 为 url 目标sid，value 为连接显示的名称 在formdata中的key值
    project_sid: "name",
    oem_sid: "name",
    contact_sid: "name",
    order_sid: "name",
    pilot_sid: "name",
};



//以下为样板代码
import { reactive } from 'vue';

const createData = () => {
    return {
        "location": [
            "安徽",
            "北京",
            "福建",
            "甘肃",
            "广东",
            "广西",
            "贵州",
            "海南",
            "河北",
            "河南",
            "黑龙江",
            "湖北",
            "湖南",
            "吉林",
            "江苏",
            "江西",
            "辽宁",
            "内蒙古",
            "宁夏",
            "青海",
            "山东",
            "山西",
            "陕西",
            "上海",
            "四川",
            "天津",
            "西藏",
            "新疆",
            "云南",
            "浙江",
            "重庆",
            "香港",
            "澳门",
            "台湾",
            "其他国内",
            "亚洲区域",
            "欧洲区域",
            "其他国外",
            "韩国",
            "日本",
            "印度",
            "俄罗斯"
        ],
        "source": [
            "展会",
            "交流会",
            "客户拜访",
            "网络或电话咨询",
            "老客户",
            "其他"
        ],
        "industry": [
            "油气田",
            "电力",
            "重金属",
            "半导体",
            "光伏面板",
            "化工",
            "垃圾",
            "印染",
            "医药",
            "特种分离",
            "市政",
            "其他"
        ],
        "pjtype": [
            "新建或扩建",
            "技改",
            "换膜"
        ],
        "wwtype": [
            {
                "name": "地下水",
                "flux_min": 100,
                "flux_max": 230
            },
            {
                "name": "自来水",
                "flux_min": 100,
                "flux_max": 230
            },
            {
                "name": "地表水",
                "flux_min": 80,
                "flux_max": 200
            },
            {
                "name": "中水回用",
                "flux_min": 80,
                "flux_max": 200
            },
            {
                "name": "海水",
                "flux_min": 80,
                "flux_max": 200
            },
            {
                "name": "循环排污水",
                "flux_min": 70,
                "flux_max": 130
            },
            {
                "name": "冷凝液",
                "flux_min": 70,
                "flux_max": 130
            },
            {
                "name": "矿井水",
                "flux_min": 70,
                "flux_max": 130
            },
            {
                "name": "反渗透浓水",
                "flux_min": 70,
                "flux_max": 120
            },
            {
                "name": "工业废水",
                "flux_min": 70,
                "flux_max": 130
            },
            {
                "name": "油田采出水",
                "flux_min": 20,
                "flux_max": 50
            },
            {
                "name": "压裂返排液",
                "flux_min": 20,
                "flux_max": 40
            },
            {
                "name": "其他含油废水",
                "flux_min": 10,
                "flux_max": 80
            },
            {
                "name": "其他",
                "flux_min": 20,
                "flux_max": 150
            }
        ],
        "pjstage": [
            {
                "name": "线索",
                "win_percentage": 10
            },
            {
                "name": "方案及报价",
                "win_percentage": 25
            },
            {
                "name": "已投标",
                "win_percentage": 50
            },
            {
                "name": "指定我司",
                "win_percentage": 75
            },
            {
                "name": "拟签合同",
                "win_percentage": 90
            },
            {
                "name": "获得订单",
                "win_percentage": 100
            },
            {
                "name": "丢失-竞争对手中标",
                "win_percentage": 0
            },
            {
                "name": "丢失-项目取消",
                "win_percentage": 0
            }
        ],
        "oemtype": [
            "代理商",
            "工程公司",
            "总包",
            "设计院",
            "经销商",
            "其他"
        ],
        "department": [
            "设计及技术",
            "销售及商务",
            "采购",
            "运营",
            "管理层",
            "其他"
        ],
        "title": [
            "总经理",
            "副总级别",
            "主管级别",
            "专工级别",
            "普通级别",
            "其他"
        ],
        "product_units": [
            "支",
            "个",
            "套",
            "pcs",
            "set",
            "片",
            "组",
            "-"
        ],
        "order_status": [
            "未签订",
            "已签订",
            "已收预付款",
            "已收全款",
            "已发货"
        ],
        "chem": [
            {
                "text": "盐酸HCl",
                "value": "hcl"
            },
            {
                "text": "氢氧化钠NaOH",
                "value": "naoh"
            },
            {
                "text": "硫酸H2SO4",
                "value": "h2so4"
            },
            {
                "text": "柠檬酸",
                "value": "citric"
            },
            {
                "text": "次氯酸钠NaClO",
                "value": "naclo"
            }
        ]
    }
}

// export const formData = reactive(createData())
const createActions = () => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                //     ["same.content", "required", state.fd.body],
                //     ["same.content", "len_gt", state.fd.body, 5],
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
