"use strict";
// 此文件为函数合集，可以test
const genColClass = (options) => {
    // 为数字且>0
    const valNumber = (n) => typeof (n) === 'number' && n > 0 ? n : null
    let { sm, md, lg, xl, xxl, other } = options
    const col = {
        sm: valNumber(sm),
        md: valNumber(md),
        lg: valNumber(lg),
        xl: valNumber(xl),
        xxl: valNumber(xxl),
    }
    const keys = ['sm', 'md', 'lg', 'xl', 'xxl']
    const cls_arr = []
    if (other) {
        cls_arr.push(other)
    }
    for (let k of keys) {
        if (col[k]) {
            cls_arr.push(`col-${k}-${col[k]}`)
        }
    }
    return cls_arr.join(' ')
}

const sm = genColClass({ md: 6, other: 'mt-10' })
// console.log(sm)

const genUid = () => {
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}

const can = (cu, model, action, scope, ownerSid) => {
    const perm = cu.perm || {}
    const is_su = cu.is_su || false
    const userSid = cu.sid
    if (!userSid) { return false }
    const model_actions_dt = perm[model]
    const action_scope = model_actions_dt ? model_actions_dt[action] : ""
    if (['create', 'dashboard'].includes(action)) { ownerSid = '' }
    if (action === 'edit') {
        // 此处必然结束判定
        if (ownerSid) { return ownerSid == userSid } else {
            if (is_su) { return true }
            else if (action_scope === 'total') { return true }
        }
        return false
    }
    if (is_su) { return true }
    if (!model_actions_dt) { return false }
    if (!action) { return true } //无 操作名称
    if (!action_scope) { return false } // 没有获取操作范围 必须是me 或者 total
    // 没有提供ownerSid时候，针对list， 需要显性指定“total”才能控制 list-total 的访问权限
    if (!ownerSid) { if (scope !== 'total') { return true } else { return action_scope === 'total' } }
    if (ownerSid === userSid) { return true }
    return action_scope === 'total'

};

const genBtnClass = (position, btnClass, other) => {
    let cls = "btn"
    if (btnClass) { cls = cls + " " + btnClass } else { cls = "btn btn-primary" }
    if (['right', 'left', 'center'].includes(position)) {
        //在中间的话 就加两侧的Margin
        if (position === 'center') { cls = cls + " " + "my-2 mx-2" }
        //右侧 则加左边
        else if (position === 'right') { cls = cls + " " + "my-2 ms-2" }
        //左侧 则加右边
        else if (position === 'left') { cls = cls + " " + "my-2 me-2" }
    } else { cls = cls + " " + "my-2 me-2" }
    if (other) { cls = cls + " " + other }
    return cls
}
// const state = { cu: { sid: "123", perm: { post: { edit: 'me', create: 'me', delete: 'me', dashboard: 'total' } } } }
// const model = 'post'
// const scope = 'me'
// const action = 'dashboard'
// const ownerSid = '1213'
// console.log(can(state.cu, model, action, scope, ownerSid))

// const c = genBtnClass('right', '', 'mt-3')
// console.log(c)


const getOptionValue = (item, valueKey) => {
    // 根据一个option的item，获取Value
    if (typeof item !== "object") {
        return item;
    } else if (typeof item === "object") {
        return item[valueKey];
    }
};
const getOptionText = (item, textKey, sep) => {
    // 根据一个option的item，获取显示的text
    if (typeof item !== "object") {
        return item;
    } else if (typeof item === "object") {
        if (typeof (textKey) === 'string') { return item[textKey] }
        else if (typeof item === 'object') {
            let ls = []
            for (let k of textKey) {
                if (item[k]) { ls.push(item[k]) }
            }
            const sep1 = sep ? sep : ', '
            return ls.join(sep1)
        }
    }
};
// const item = { a: 'a1', b: 'b2', c: 'c1' }
// console.log(getOptionText(item, ['c', 'b']))

const genReadUrl = (sidKey, sid, name) => {
    if (!sid || !name) { return null }
    const sidKeys = {
        post_sid: "post",
        project_sid: "project",
        oem_sid: 'oem',
        contact_sid: 'contact',
        pilot_sid: "pilot",
        order_sid: "order",
        quote_sid: "quote",
        owner_sid: 'user',
        role_sid: 'role',
        product_sid: 'product',
        design_module_sid: 'design_module',
        design_sid: 'design',
        standard_design_sid: 'standard_design'
    }
    const model = sidKeys[sidKey]
    if (model) { return { url: `/${model}/read/${sid}`, name: name } }
    else { return null }
}

// console.log(genReadUrl('project_sid', 'adasdadasd', '大项目'))

// const genPaginationList = (totalPage, currentPage, maxShowNums) => {
//     // 输出 pagenation list
//     const ls = []
//     if (totalPage <= maxShowNums) {
//         for (let i = 1; i <= totalPage; i++) { ls.push(i) }
//     } else {
//         const half = Math.floor(maxShowNums / 2) //一半,目标为7， 中间5，两边各1
//         if (currentPage === 1 || currentPage===totalPage){

//         }
//     }
// }

const getDataType = (data) => {
    // 判断数据类型
    const temp = Object.prototype.toString.call(data);
    const type = temp.match(/\b\w+\b/g);
    return (type.length < 2) ? 'Undefined' : type[1];
}


const isObjectChanged = (source, comparison) => {
    // 判断两个对象是否相等
    const iterable = (data) => ['Object', 'Array'].includes(getDataType(data));
    if (!iterable(source)) {
        throw new Error(`source should be a Object or Array , but got ${getDataType(source)}`);
    }
    if (getDataType(source) !== getDataType(comparison)) {
        return true;
    }
    const sourceKeys = Object.keys(source);
    const comparisonKeys = Object.keys({ ...source, ...comparison });
    if (sourceKeys.length !== comparisonKeys.length) {
        return true;
    }
    return comparisonKeys.some(key => {
        if (iterable(source[key])) {
            return isObjectChanged(source[key], comparison[key]);
        } else {
            return source[key] !== comparison[key];
        }
    });
}
// 通过函数的方式，修改 object 中 深层 key 的值
const updateObject = (obj, keylist, value) => {
    // obj 为目标修改的值
    // keylist 是 多级key， 如 obj.a.b  => keylist = ['a','b']
    // val 是设定的值
    if (typeof (keylist) === 'object') {
        const keylen = keylist.length;
        for (let i = 0; i < keylen - 1; i++) {
            // 注意循环到最后第二个key
            // 不然会指向一个固定值，如果 obj.a.b = 1 , 此时target = 1，无法修改
            // 需要将target指向 obj.a
            // 之后通过 target[b] = val 进行修改
            let key = keylist[i];
            // console.log('key', key)
            obj = obj[key];
        }
        // console.log('keylist[keylen-1]', keylist[keylen - 1])
        obj[keylist[keylen - 1]] = value;
    } else if (typeof keylist === 'string') {
        obj[keylist] = value
    }
};


// arr为 array形式的数据，对其进行操作
const changeHandle = (arr, index, value, key) => {
    if (key === null || key === undefined) {
        arr[index] = value;
    } else {
        arr[index][key] = value;
    }
};
const deleteHandle = (arr, index) => {
    arr.splice(index, 1);
};
const updateArr = (action, arr, index, value, key) => {
    // 深度 操作 Arr[Object]
    if (action === "change") {
        changeHandle(arr, index, value, key);
    } else if (action === "delete") {
        deleteHandle(arr, index);
    }
};

// var _ = require('lodash');

// const arr = [{ a: 1, b: 11 }, { a: 2, b: 22 },]
// const r = _.sumBy(arr, 'b');
// console.log(r)

// const a = { a: 1, b: 11 }
// const b = { b: [1, 2, 3], c: 8 }
// Object.assign(a, b)
// console.log(a, b)


const arrayMove = (farther, index, targetIndex) => {
    // 将元素在Array内部 进行移动到目标Index
    const len = farther.length
    if (index < 0 || index >= len) { return false }
    if (targetIndex < 0 || targetIndex >= len) { return false }
    farther.splice(targetIndex, 0, farther.splice(index, 1)[0])
}

const arrayMoveNext = (farther, index) => {
    const targetIndex = index + 1
    arrayMove(farther, index, targetIndex)
}
const arrayMovePre = (farther, index) => {
    const targetIndex = index - 1
    arrayMove(farther, index, targetIndex)

}

const a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
// arrayMove(a, 1, 8)
// console.log(a)
arrayMoveNext(a, 9)
console.log(a)

arrayMovePre(a, 9)
console.log(a)


const myRules = {
    isEmail: (v) => isEmail(v) || '不是合法email格式',
    required: (v) => (v !== null && v !== undefined && v !== '') || '不能为空',
    // 大于
    len_gt: (m) => (v) => v.length > m || `长度必须 > ${m}`,
    // 大于等于
    len_ge: (m) => (v) => v.length >= m || `长度必须 >= ${m}`,
    // 小于
    len_lt: (m) => (v) => v.length < m || `长度必须 < ${m}`,
    // 小于等于
    len_le: (m) => (v) => v.length <= m || `长度必须 <= ${m}`,
    // 大于
    gt: (m) => (v) => v > m || `必须 > ${m}`,
    // 大于等于
    ge: (m) => (v) => v >= m || `必须 >= ${m}`,
    // 小于
    lt: (m) => (v) => v < m || `必须 < ${m}`,
    // 小于等于
    le: (m) => (v) => v <= m || `必须 <= ${m}`,
    between: (m, n) => (v) => v > Math.min(m, n) && v < Math.max(m, n) || `必须 > ${Math.min(m, n)} 且 < ${Math.max(m, n)}`,
    betweenEqual: (m, n) => (v) => v >= Math.min(m, n) && v <= Math.max(m, n) || `必须 > ${Math.min(m, n)} 且 < ${Math.max(m, n)}`,
    confirmPassword: (m) => (v) => m === v || "两次密码输入不一致",
    in: (arr) => (v) => arr.includes(v) || `不在给定范围内`,
};

const v = myRules['ge'](5)(4)
console.log(v)

var _ = require('lodash')

const t1 = Date.now()

console.log(t1)
const t2 = t1 + 5 * 60 * 1000
console.log(t2)

const d = new Date(t1) // 时间戳 转换为 Date
console.log(d)
console.log('d转换为时间戳', d.getTime())
const d2 = new Date(t2)
console.log(d2)

console.log(d2 > d)

