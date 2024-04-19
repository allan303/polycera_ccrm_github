//Author : Jack Li
//Email  : allanth3@163.com
//Date   : 2020-10-30
export const createCu = () => {
    return {
        sid: '',
        create_time_local: '',
        'update_time_local': '',
        'last_seen_local': '',
        'is_deleted': false,
        'username': '',
        'email': '',
        'role_sid': '',
        'company': '',
        'phone': '',
        'name': '',
        'title': '',
        'is_su': false,
        perm: {},
        user_config: {}
    }
}

// 这样导出 每次都会生成新的对象
export const createState = () => {
    // 注意 为了提高性能，采用的是ShallowReactive
    return {
        cu: createCu(),
        token_recieve_time: null, // 获得token的时间
        access_token: '',
        token_type: '',
        expire_minutes: 0,
        cacheInfo: {
            project: [],
            oem: [],
            role: [],
            post: [],
            order: [],
            pilot: [],
            contact: [],
            config: {},
            quote: [],
            user: [],
            product_units: [],
            workgroup: []
        }, // 直接通过 getCache更新
        order_keywords: {},
        local: {
            use_half: false,
            workgroup_sid: '',
            locale: 'zh'
        },
    }
}



