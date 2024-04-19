
export const defaultCebHcl = () => {
    return {
        "chem_dosings": [
            {
                "chem_density": null,
                "chem_wt": 30.0,
                "dosing_wt": 0.1,
                "name": "hcl",
                "solid_price_per_kg": 0.0
            }
        ],
        "duration_add": {
            "unit": "minutes",
            "val": 5.0
        },
        "interval": {
            "unit": "day",
            "val": 2.0
        },
        "name": "酸",
        'temp': 25,
        "process_list": [
            {
                "duration": {
                    "unit": "seconds",
                    "val": 30.0
                },
                "name": "backwash"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 60.0
                },
                "name": "ceb"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 15.0
                },
                "name": "soak"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 120.0
                },
                "name": "wash"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 60.0
                },
                "name": "backwash"
            }
        ]
    }
}

export const defaultCebNaOH = () => {
    return {
        chem_dosings: [
            {
                "chem_density": null,
                "chem_wt": 20.0,
                "dosing_wt": 0.2,
                "name": "naoh",
                "solid_price_per_kg": 0.0
            },
            {
                "chem_density": null,
                "chem_wt": 10.0,
                "dosing_wt": 0.005,
                "name": "naclo",
                "solid_price_per_kg": 0.0
            }
        ],
        "duration_add": {
            "unit": "minutes",
            "val": 5.0
        },
        "interval": {
            "unit": "天",
            "val": 2.0
        },
        "name": "碱",
        'temp': 50,
        "process_list": [
            {
                "duration": {
                    "unit": "seconds",
                    "val": 30.0
                },
                "name": "backwash"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 60.0
                },
                "name": "ceb"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 30.0
                },
                "name": "soak"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 120.0
                },
                "name": "wash"
            },
            {
                "duration": {
                    "unit": "seconds",
                    "val": 60.0
                },
                "name": "backwash"
            }
        ]
    }
}
//以下CIP
export const defaultCipHCl = () => {
    return {
        chem_dosings: [
            {
                "chem_density": null,
                "chem_wt": 30,
                "dosing_wt": 0.2,
                "name": "hcl",
                "solid_price_per_kg": 0.0
            }
        ],
        "duration_add": {
            "unit": "minutes",
            "val": 20.0
        },
        "interval": {
            "unit": "day",
            "val": 30.0
        },
        "name": "盐酸",
        "temp": 25,
        "process_list": [
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 30.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "hours",
                    "val": 1.0
                },
                "name": "soak"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 90.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 10.0
                },
                "name": "wash"
            }
        ]
    }
}

export const defaultCipCitric = () => {
    return {
        chem_dosings: [
            {
                "chem_density": null,
                "chem_wt": 100,
                "dosing_wt": 1,
                "name": "citric",
                "solid_price_per_kg": 0.0
            }
        ],
        "duration_add": {
            "unit": "minutes",
            "val": 20.0
        },
        "interval": {
            "unit": "day",
            "val": 30.0
        },
        "name": "柠檬酸",
        "temp": 25,
        "process_list": [
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 30.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "hours",
                    "val": 1.0
                },
                "name": "soak"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 90.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 10.0
                },
                "name": "wash"
            }
        ]
    }
}

export const defaultChem = () => {
    return {
        "chem_density": null,
        "chem_wt": 30.0,
        "dosing_wt": 0.1,
        "name": "hcl",
        "solid_price_per_kg": 0.0
    }
}

export const defaultProcess = () => {
    return {
        "duration": {
            "unit": "minutes",
            "val": 0
        },
        "name": "drain"
    }
}
export const defaultCipNaOH = () => {
    return {
        "chem_dosings": [
            {
                "chem_density": null,
                "chem_wt": 20.0,
                "dosing_wt": 0.4,
                "name": "naoh",
                "solid_price_per_kg": 0.0
            },
            {
                "chem_density": null,
                "chem_wt": 5.0,
                "dosing_wt": 0.01,
                "name": "naclo",
                "solid_price_per_kg": 0.0
            }
        ],
        "duration_add": {
            "unit": "minutes",
            "val": 60.0
        },
        "interval": {
            "unit": "day",
            "val": 30.0
        },
        "name": "碱+氧化剂",
        "temp": 50,
        "process_list": [
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 30.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "hours",
                    "val": 2.0
                },
                "name": "soak"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 90.0
                },
                "name": "circulate"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 5.0
                },
                "name": "drain"
            },
            {
                "duration": {
                    "unit": "minutes",
                    "val": 10.0
                },
                "name": "wash"
            }
        ]
    }
}

export const process_ceb_names = [
    { text: "加药反洗(ceb)", value: "ceb" },
    { text: "冲洗", value: "wash" },
    { text: "反洗", value: "backwash" },
    { text: "浸泡", value: "soak" },
    { text: "冲洗+反洗", value: "wash+backwash" },
];

export const process_cip_names = [
    { text: "循环", value: "circulate" },
    { text: "冲洗", value: "wash" },
    { text: "反洗", value: "backwash" },
    { text: "浸泡", value: "soak" },
    { text: "排空", value: "drain" },
];


const validateChemDosing = (cd) => {
    if (!cd.name) { alert('化学品名称:不能为空'); return false }
    if (!cd.chem_wt) { alert('化学品原液浓度:不能为空或0'); return false }
    if (cd.chem_wt <= 0) { alert('化学品原液浓度:>0'); return false }
    if (cd.chem_wt > 100) { alert('化学品原液浓度:<=100'); return false }
    if (!cd.dosing_wt) { alert('加药浓度:不能为空或0'); return false }
    if (cd.dosing_wt <= 0) { alert('加药浓度:>0'); return false }
    if (cd.dosing_wt > 100) { alert('加药浓度:<=100'); return false }
    if (cd.dosing_wt >= cd.chem_wt) { alert('加药浓度必须小于原液浓度'); return false }
    if ([null, undefined, ''].includes(cd.solid_price_per_kg)) { alert('化学品单价不能为空,留空请填写0'); return false }
    return true
}
const validateDosing = (ds) => {
    for (let cd of ds.chem_dosings) {
        if (!validateChemDosing(cd)) { return false }
    }
    return true
}

const validateProcess = (pc) => {
    if (!pc.name) { alert('清洗操作名称:不能为空'); return false }
    if (!pc.duration.val) { alert('清洗操作时间:不能为空'); return false }
    if (pc.duration.val < 0) { alert('清洗操作时间:>0'); return false }
    if (!pc.duration.unit) { alert('清洗操作时间单位:不能为空'); return false }
    return true
}
const validateOneClean = (cc) => {
    if (!cc.temp) { alert('温度:不能为空'); return false }
    if (cc.temp <= 0) { alert('温度:>0'); return false }
    if (!cc.interval.val) { alert('清洗间隔:不能为空'); return false }
    if (cc.interval.val <= 0) { alert('清洗间隔:>0'); return false }
    const cds = cc.chem_dosings
    for (let cd of cds) {
        if (!validateChemDosing(cd)) { return false }
    }
    const pcs = cc.process_list
    for (let pc of pcs) {
        if (!validateProcess(pc)) { return false }
    }
    return true
}

export const validateDesignOption = (options) => {
    const md = options.module
    if (!md.model) { alert('膜型号:不能为空'); return false }
    const mb = options.main_balance
    if (!mb.lmh_design) { alert('膜型号:不能为空'); return false }
    if (!mb.rec_operate) { alert('设计运行回收率:不能为空'); return false }
    if (mb.rec_operate <= 0) { alert('设计运行回收率:>0'); return false }
    if (mb.rec_operate > 1) { alert('设计运行回收率:<1'); return false }
    if (mb.module_nums_per_train < 1) { alert('串联长度:>=1'); return false }
    if (mb.serie_nums < 1) { alert('系列数量:>=1'); return false }
    if (mb.group_nums_per_serie < 1) { alert('组/系列:>=1'); return false }
    if (mb.serie_nums_backup < 0) { alert('系列备用数量:>=0'); return false }

    const bw = options.backwash
    if (bw.is_use) {
        if (!bw.lmh) { alert('反洗通量:不能为空'); return false }
        if (bw.lmh < 0) { alert('反洗通量:>0'); return false }
        if (!bw.duration.val) { alert('反洗时间:不能为空'); return false }
        if (bw.duration.val <= 0) { alert('反洗时间:>0'); return false }
        if (!bw.interval.val) { alert('反洗间隔:不能为空'); return false }
        if (bw.interval.val <= 0) { alert('反洗间隔:>0'); return false }
        if (!bw.duration_add.val) { alert('反洗切换时间:不能为空'); return false }
        if (bw.duration_add.val <= 0) { alert('反洗切换时间:>0'); return false }
    }
    const bf = options.backflow
    if (bf.is_use) {
        if (bf.m3ph_per_train < 0) { alert('反洗通量:>=0'); return false }
    }
    const cir = options.cir
    if (cir.is_use) {
        if (cir.m3ph_per_train < 0) { alert('循环流量:>=0'); return false }
    }
    const ceb = options.ceb
    if (ceb.is_use) {
        if (!ceb.lmh) { alert('CEB通量:不能为空'); return false }
        if (ceb.lmh <= 0) { alert('CEB通量:>0'); return false }
        for (let oneClean of ceb.oneclean_list) {
            if (!validateOneClean(oneClean)) {
                return false
            }
        }
    }
    const cip = options.cip
    if (cip.is_use) {
        if (!cip.cip_nums) { alert('CIP系统数量:不能为空'); return false }
        if (cip.cip_nums < 1) { alert('CIP系统数量:>1'); return false }
        if (cip.m3ph_per_train < 0) { alert('CIP单膜壳流量:>=0'); return false }
        for (let oneClean of cip.oneclean_list) {
            if (!validateOneClean(oneClean)) {
                return false
            }
        }
    }

    const tanks = options.tanks
    if (!tanks.perm.hrt_minutes || tanks.perm.hrt_minutes <= 0) { alert('产水箱停留时间：必须大于0'); return false }
    if (!tanks.cip.hrt_minutes || tanks.cip.hrt_minutes <= 0) { alert('化学清洗箱停留时间：必须大于0'); return false }
    if (!tanks.feed.hrt_minutes || tanks.feed.hrt_minutes <= 0) { alert('原水箱停留时间：必须大于0'); return false }

    const ds = options.dosing
    if (ds.is_use) {
        return validateDosing(ds)
    }

    const rf = options.raw_flow
    if (!rf.q) { alert('水量:不能为空'); return false }
    if (rf.q <= 0) { alert('水量:>0'); return false }
    if (!rf.temp) { alert('设计温度:不能为空'); return false }
    if (rf.temp <= 0) { alert('设计温度:>0'); return false }
    if (!rf.hpd) { alert('工作时间:不能为空'); return false }
    if (rf.hpd <= 0) { alert('工作时间:>0'); return false }
    if (rf.hpd > 24) { alert('工作时间:<=24'); return false }
    if (!rf.wwtyp > 24) { alert('工作时间:不能为空'); return false }
    return true

}


//以下为样板代码
export const createData = () => {
    return {
        "sid": "",
        "create_time_local": "",
        "update_time_local": "",
        "is_deleted": false,
        "owner_sid": "",
        "name": "",
        "remark": "",
        options: {
            'backflow': { 'is_use': false, 'm3ph_per_train': 0 },
            'backwash': {
                'backwash_wash_m3ph_per_train': null,
                'duration': { 'unit': 'seconds', 'val': 30.0 },
                'duration_add': { 'unit': 'seconds', 'val': 30.0 },
                'group_nums_per_backwash': 4,
                'interval': { 'unit': 'minutes', 'val': 30.0 },
                'is_drain_out': true,
                'is_use': true,
                'lmh': 150,
                'pressure': { 'unit': 'bar', 'val': 1.7 },
                'use_wash': false
            },
            'ceb': { 'is_use': false, 'use_ceb_pump': false, 'lmh': 10, 'oneclean_list': [] },
            'cip': {
                'cip_nums': 1,
                'is_use': false,
                'm3ph_per_train': 5,
                'oneclean_list': []
            },
            'cir': { 'is_use': false, 'm3ph_per_train': 0 },
            'dosing': { 'chem_dosings': [], 'is_use': false },
            'is_target_perm': true,
            'main_balance': {
                'design_pn': 10,
                'group_nums_per_serie': 1,
                'install': '立式',
                'is_use': true,
                'k_list': [],
                'lmh_design': 80,
                'module_nums_per_train': 1,
                'rec_operate': 0.95,
                'serie_nums': 1,
                'serie_nums_backup': 0
            },
            'matter_balance': { 'is_use': false, 'matter_name': 'cod' },
            'module': {
                'fa': 23.6,
                'flux_per_bar_25': 80,
                'is_contained_pv': false,
                'liter_inside': 20,
                'model': '',
                'module_size': '8040',
                'spacer_mil': 40
            },
            'other_info': {
                'create_time_local_str': '',
                'module_model': '',
                'project_remark': '',
                'show_bom': false,
                'show_kw_consumer': true,
                'show_tree': false,
                'special_note': '',
                'treatment_process': '',
                'treatment_process_note': '',
                'version': '1.0',
                'sdi': '≤3',
                'ntu': '≤0.5NTU',
                'rec': '≥0.5NTU',
                'lifetime': '≥5年',
                'tss': "≤1mg/L",
            },
            'pumps_pressure': {
                'backwash_pump': 2,
                'backwash_vfd': true,
                'cip_pump': 2.5,
                'cip_vfd': false,
                'cir_pump': 2,
                'cir_vfd': true,
                'feed_pump': 4,
                'feed_vfd': true
            },
            'raw_flow': {
                'concs_dt': { 'cod': 0, 'ntu': 0, 'oil': 0, 'ss': 0, 'tds': 0 },
                'hpd': 24,
                'name': '原水',
                'ph': 7,
                'q': 0,
                'q_unit': 'm3/h',
                'remark': '',
                'temp': 25,
                'water_solution': 'nacl',
                'wwtype': '地表水'
            },
            'real_feed_pressure': {
                'dp_per_train': 0.1,
                'fouling_k': 0.9,
                'perm_bar': 0.1,
                'years': 3
            },
            'tanks': {
                'cip': {
                    'drain_minutes': 15.0,
                    'hrt_minutes': 1.5,
                    'material': '碳钢防腐/PP',
                    'name': '清洗水箱',
                    'nums': 1,
                    'v': 0
                },
                'feed': {
                    'drain_minutes': 60,
                    'hrt_minutes': 60.0,
                    'material': '碳钢防腐/PP',
                    'name': '原水箱',
                    'nums': 1,
                    'v': 0
                },
                'perm': {
                    'drain_minutes': 60,
                    'hrt_minutes': 60.0,
                    'material': '碳钢防腐/PP',
                    'name': '产水箱',
                    'nums': 1,
                    'v': 0
                }
            },
            'wash': {
                'duration': { 'unit': 'seconds', 'val': 30.0 },
                'duration_add': { 'unit': 'seconds', 'val': 15.0 },
                'interval': { 'unit': 'minutes', 'val': 120.0 },
                'is_use': false,
                'm3ph_per_train': 10,
                'wash_water': 'other'
            }
        },
        share_list: [],
        downloadOption: {
            show_bom: true,
            show_kw_consumer: true,
            show_tree: false,
            show_cip: false,
            show_ceb: true,
            show_time: true,
            show_chem_consumer: true,
            tpl_name: 'design_uf_sheet_polycera_jack_tpl.docx'
        }
    }
}

export const tpl_names = [
    {
        name: "Polycera超滤计算书(Jack)",
        value: 'design_uf_sheet_polycera_jack_tpl.docx',
    },
    {
        name: "Polycera超滤方案(Jack)",
        value: 'design_uf_scheme_polycera_jack_tpl.docx',
    },
    // {
    //     name: "Polycera纳滤计算书(Jack)",
    //     value: 'design_nf_sheet_polycera_jack_tpl.docx',
    // },
    {
        name: "Polycera超滤方案(Simon)",
        value: 'design_uf_scheme_polycera_simon_tpl.docx',
    },
    {
        name: "中空纤维超滤计算书(Jack)",
        value: 'design_uf_sheet_fiber_jack_tpl.docx',
    }
]


export const createGetters = (state) => {
    return {
        name() { return state.fd.name }
    }
}
// export const validateFormDataNonStandard = (fd) => {
//     if (!fd.name) { alert("名称：不能为空"); return false }
//     const options = fd.options
//     if (!validateDesignOption(options)) { return false }
//     return true
// }
// export const formData = reactive(createData())

export const createActions = (state) => {
    //创建对 formData的操作合集 ,fd = formData
    return {
        getValidateFields() {
            return [
                ["same.name", "required", state.fd.name],
            ]
        },
        validateFormDataNonStandard() {
            const fd = state.fd
            if (!fd.name) { alert("名称：不能为空"); return false }
            const options = fd.options
            if (!validateDesignOption(options)) { return false }
            return true
        }
    }
}