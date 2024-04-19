"use strict";
//此文件不能test，因为有export
import { isEmail } from "validator";
import fileDownload from "js-file-download";
import { useStore, useAxios } from './main';

//CRUD权限
export const can = (cu, model, action, scope, ownerSid, shareList) => {
    // const print = (i, str) => {
    //     if (['t', 'ft'].includes(str)) {
    //         console.log('can', str, i, model, action, scope, ownerSid, shareList)
    //     }
    // }
    const perm = cu.perm || {}
    const is_su = cu.is_su || false
    const userSid = cu.sid
    // su false情况1
    if (!userSid) {
        //print(1, 'f');
        return false
    }
    // su false情况2
    if (!model) {
        //print(2, 'f');
        return false
    }
    const model_actions_dt = perm[model]
    const my_scope = model_actions_dt ? model_actions_dt[action] : "me"
    if (action === 'edit') {
        // 此处必然结束判定
        if (ownerSid) {
            //print(3, 'ft');
            return ownerSid === userSid
        }
        else {//没有ownerSid的情况
            //su没有permDict因此靠这一条
            if (is_su) {
                //print(4, 't');
                return true
            }
            // 无所谓scope，只要有编辑权限，都可以编辑
            else {
                //print(5, 't');
                return (model_actions_dt && action in model_actions_dt)
            }
        }
    }
    if (is_su) {
        //print(7, 't');
        return true
    }
    if (!model_actions_dt) {
        //print(10, 'f');
        return false
    } //无 模块名称
    if (!scope && !action) {
        //print(19, 't');
        return true
    } // 没有设置scope没有action 意味着 can('post')
    if (action === 'read' && typeof (shareList) === 'object') {
        //在分享列表中
        if (shareList.includes(userSid)) {
            //print(8, 't');
            return true
        }
        if (shareList.includes('all')) {
            //print(9, 't');
            return true
        }
    }
    if (!(action in model_actions_dt)) {
        //print(12, 'f');
        return false
    }
    if (['create'].includes(action)) {
        //print(13, 'ft');
        return (action in model_actions_dt)
    }
    if (!my_scope) {
        //print(14, 'f');
        return false
    } // 没有获取操作范围 必须是me 或者 total
    // 没有提供ownerSid时候，针对list， 需要显性指定“total”才能控制 list-total 的访问权限
    if (!ownerSid) {
        if (my_scope === 'total') {
            //print(15, 't');
            return true
        } else {
            //print(16, 'ft');
            return scope === 'me'
        }
    }
    if (ownerSid === userSid) {
        //print(17, 't');
        return true
    }
    //print(18);
    return my_scope === 'total'

};

//确认消息
export const confirmDo = (msg, f) => {
    const r = confirm(msg);
    if (r) {
        f();
    } else {
        return false;
    }
};

//生成连续数组
// generateArray(2,15)
// [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
export const generateArray = (start, end) => {
    return Array.from(new Array(end + 1).keys()).slice(start);
};

export const getCacheInfo = (axios, names, total) => {
    return new Promise((resolve, reject) => {
        if (!names) {
            names = "";
        }
        axios({
            method: "post",
            url: `/auth/all_cache_info`,
            data: { names: names, total: total },
        })
            .then((res) => {
                //select 会因为 options 还没获取，导致显示只能是sid
                //需要确保先获得options 再获取 currentObj
                resolve(res);
            })
            .catch((err) => {
                reject(err);
            });
    });
};


export const setStateCache = () => {
    //设置 state中的 cacheInfo
    const store = useStore()
    const axios = useAxios()
    getCacheInfo(axios).then((res) => {
        store.actions.setCacheInfo(res.data)
    })

}

export const myRulesNoComment = {
    isEmail: () => (v) => isEmail(v),
    required: () => (v) => (v !== null && v !== undefined && v !== ''),
    // 大于
    len_gt: (m) => (v) => v.length > m,
    // 大于等于
    len_ge: (m) => (v) => v.length >= m,
    // 小于
    len_lt: (m) => (v) => v.length < m,
    // 小于等于
    len_le: (m) => (v) => v.length <= m,
    // 大于
    gt: (m) => (v) => v > m,
    // 大于等于
    ge: (m) => (v) => v >= m,
    // 小于
    lt: (m) => (v) => v < m,
    // 小于等于
    le: (m) => (v) => v <= m,
    between: (m, n) => (v) => v > Math.min(m, n) && v < Math.max(m, n),
    betweenEqual: (m, n) => (v) => v >= Math.min(m, n) && v <= Math.max(m, n),
    confirmPassword: (m) => (v) => m === v,
    in: (m) => (v) => m.includes(v),
};


// export const myRules = {
//     isEmail: () => (v) => isEmail(v) || $t('rule.isEmail'),
//     required: () => (v) => (v !== null && v !== undefined && v !== '') || $t('rule.required'),
//     // 大于
//     len_gt: (m) => (v) => v.length > m || $t('rule.len_gt', { m: m }),
//     // 大于等于
//     len_ge: (m) => (v) => v.length >= m || $t('rule.len_ge', { m: m }),
//     // 小于
//     len_lt: (m) => (v) => v.length < m || $t('rule.len_lt', { m: m }),
//     // 小于等于
//     len_le: (m) => (v) => v.length <= m || $t('rule.len_le', { m: m }),
//     // 大于
//     gt: (m) => (v) => v > m || $t('rule.gt', { m: m }),
//     // 大于等于
//     ge: (m) => (v) => v >= m || $t('rule.ge', { m: m }),
//     // 小于
//     lt: (m) => (v) => v < m || $t('rule.lt', { m: m }),
//     // 小于等于
//     le: (m) => (v) => v <= m || $t('rule.le', { m: m }),
//     between: (m, n) => (v) => v > Math.min(m, n) && v < Math.max(m, n) || $t('rule.between', { m: m, n: n }),
//     betweenEqual: (m, n) => (v) => v >= Math.min(m, n) && v <= Math.max(m, n) || $t('rule.betweenEqual', { m: m, n: n }),
//     confirmPassword: (m) => (v) => m === v || $t('rule.confirmPassword'),
//     in: (m) => (v) => m.includes(v) || $t('rule.in'),
// };
export const myRules = {
    isEmail: () => (v) => isEmail(v),
    required: () => (v) => (v !== null && v !== undefined && v !== ''),
    // 大于
    len_gt: (m) => (v) => v.length > m,
    // 大于等于
    len_ge: (m) => (v) => v.length >= m,
    // 小于
    len_lt: (m) => (v) => v.length < m,
    // 小于等于
    len_le: (m) => (v) => v.length <= m,
    // 大于
    gt: (m) => (v) => v > m,
    // 大于等于
    ge: (m) => (v) => v >= m,
    // 小于
    lt: (m) => (v) => v < m,
    // 小于等于
    le: (m) => (v) => v <= m,
    between: (m, n) => (v) => v > Math.min(m, n) && v < Math.max(m, n),
    betweenEqual: (m, n) => (v) => v >= Math.min(m, n) && v <= Math.max(m, n),
    confirmPassword: (m) => (v) => m === v,
    in: (m) => (v) => m.includes(v),
};
// export const validateField = (fieldName, ruleName, v, m, n) => {
//     //采用 myRules中的规则，对数据进行验证，并alert相关信息（单个）
//     if (!myRules[ruleName]) { alert(`没有 ${ruleName} 规则, ${fieldName}`); return false }
//     let res = myRules[ruleName](m, n)(v)
//     if (res === true) { return true } else {
//         alert(`[${fieldName}]: ${res}`)
//         return false
//     }
// }
export const validateField = ($t, fieldName, ruleName, v, m, n) => {
    //采用 myRules中的规则，对数据进行验证，并alert相关信息（单个）
    if (!myRules[ruleName]) { alert(`No Rule: ${ruleName}, ${fieldName}`); return false }
    let res = myRules[ruleName](m, n)(v)
    if (res === true) { return true } else {
        alert(`[${$t(fieldName)}]: ${$t(`rule.${ruleName}`)}`)
        return false
    }
}
//传入一个 field 和规则的 Array，验证Form
// const fields = [
//     ["用户名", "isEmail", data.username],
//     ["密码", "required", data.password],
//     ["数字", "ge", data.num, 3],
//     ["数字", "lt", data.num, 10],
// ];
export const validateForm = ($t, fields) => {
    for (const f of fields) {
        //其中一个是错误 则返回false
        if (validateField($t, ...f) !== true) {
            return false;
        }
    }
    return true;
};

export const downloadBlob = (res, filename) => {
    // Here is a hack, works well for me.
    // You can put it into `transformResponse`, etc as well.
    let resBlob = res.data; // <--- store the blob if it is
    let resData = null;
    try {
        let resText = new Promise((resolve, reject) => {
            let reader = new FileReader();
            reader.addEventListener("abort", reject);
            reader.addEventListener("error", reject);
            reader.addEventListener("loadend", () => {
                resolve(reader.result);
            });
            reader.readAsText(resBlob);
        });
        resData = JSON.parse(resText); // <--- try to parse as json evantually
    } catch (err) {
        // ignore
    }

    // Now you have `resData` and `resBlob` at the same time.
    // `resData` would be the normal data object,
    // or the error object if `resBlob` is expected.
    if (resData) {
        if (resData.error) {
            // handle error
            alert(resData.error);
        } else {
            // handle data
        }
    } else {
        // handle blob
        fileDownload(resBlob, filename);
    }
};

export const downloadReport = (axios, method, url, data, filename) => {
    //下载文件
    axios({
        method: method || "post",
        url: url,
        data: data,
        responseType: "blob",
    })
        .then((res) => {
            // this.download(res.data);
            downloadBlob(res, filename);
        });
};

export const validateVal = (val, validateFns) => {
    // 用于通过一系列Fns 验证 值
    if (typeof validateFns === "function") {
        // val值 validate 回调函数
        if (!validateFns(val)) {
            // console.log("验证", val);
            return false;
        }
    } else if (typeof validateFns === 'object') {
        for (let fn of validateFns) {
            if (typeof fn === "function") {
                // val值 validate 回调函数
                if (!fn(val)) {
                    // console.log("验证fn", val);
                    return false;
                }
            }
        }
    }
    return true
}

// 通过函数的方式，修改 object 中 深层 key 的值
export const updateObject = (obj, keylist, val, validateFns) => {
    if (validateFns) {
        if (!validateVal(val, validateFns)) { return false }
    }
    // obj 为目标修改的值
    // keylist 是 多级key， 如 obj.a.b  => keylist = ['a','b']
    // val 是设定的值
    let target = obj;
    const keylen = keylist.length;
    for (let i = 0; i < keylen - 1; i++) {
        // 注意循环到最后第二个key
        // 不然会指向一个固定值，如果 obj.a.b = 1 , 此时target = 1，无法修改
        // 需要将target指向 obj.a
        // 之后通过 target[b] = val 进行修改
        let key = keylist[i];
        // console.log('key', key)
        target = target[key];
    }
    // console.log('keylist[keylen-1]', keylist[keylen - 1])
    target[keylist[keylen - 1]] = val;
};

// 直接生成对应的 Breakpoint组合 仅适用于 Materialize-CSS
export const genColClass = (options) => {
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
export const genBtnClass = (position, btnClass, other) => {
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

export const genUid = () => {
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}



export const getOptionValue = (item, valueKey) => {
    // 根据一个option的item，获取Value
    if (typeof item !== "object") {
        return item;
    } else if (typeof item === "object") {
        return item[valueKey];
    }
};
export const getOptionText = (item, textKey, sep) => {
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



export const getDataType = (data) => {
    // 判断数据类型
    const temp = Object.prototype.toString.call(data);
    const type = temp.match(/\b\w+\b/g);
    return (type.length < 2) ? 'Undefined' : type[1];
}


export const isObjectChanged = (source, comparison) => {
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

export const genReadUrl = (sidKey, sid, name) => {
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
        brand: 'Polycera',
        design_sid: 'design',
        standard_design_sid: 'standard_design'
    }
    const model = sidKeys[sidKey]
    if (model) { return { url: `/${model}/read/${sid}`, name: name } }
    else { return null }
}

export const getRelatedUrls = (readUrlDict, formData, store) => {
    // 获取、生成全部的可用连接和名称
    const urls = [];
    if (!readUrlDict || !Object.keys(readUrlDict).length) {
        return urls;
    }
    for (let k in readUrlDict) {
        let sid = formData[k];
        // let name = formData[readUrlDict[k]];
        let name = store.getters.objName(k, sid)
        const url = genReadUrl(k, sid, name);
        if (url) {
            urls.push(url);
        }
    }
    return urls;
};


export const getRelatedUrls1 = (readUrlDict, formData, store) => {
    // 获取、生成全部的可用连接和名称
    const urls = [];
    if (!readUrlDict || !Object.keys(readUrlDict).length) {
        return [];
    }
    for (let k in readUrlDict) {
        let sid = formData[k]; //formData['project_sid']
        // let name = formData[readUrlDict[k]];
        let name = store.getters.objName(k, sid, readUrlDict[k])
        // let name = store.getters.objName(k, sid)
        const url = genReadUrl(k, sid, name);
        if (url) {
            urls.push(url);
        }
    }
    return urls;
};

const changeHandle = (arr, index, value, key) => {
    // Array[Object] 形式，修改其中參數
    if (key === null || key === undefined) {
        arr[index] = value;
    } else {
        arr[index][key] = value;
    }
};
const deleteHandle = (arr, index) => {
    //arr 刪除 key
    arr.splice(index, 1);
};
export const updateArr = (action, arr, index, value, key) => {
    // 深度 操作 Arr[Object]
    if (action === "change") {
        changeHandle(arr, index, value, key);
    } else if (action === "delete") {
        deleteHandle(arr, index);
    }
};



export const arrayMove = (farther, index, targetIndex) => {
    // 将元素在Array内部 进行移动到目标Index
    const len = farther.length
    if (index < 0 || index >= len) { return false }
    if (targetIndex < 0 || targetIndex >= len) { return false }
    farther.splice(targetIndex, 0, farther.splice(index, 1)[0])
}

export const arrayMoveNext = (farther, index) => {
    const targetIndex = index + 1
    arrayMove(farther, index, targetIndex)
}
export const arrayMovePre = (farther, index) => {
    const targetIndex = index - 1
    arrayMove(farther, index, targetIndex)
}


export const getTodayStr = () => {
    // 获取当前日期
    var date = new Date();

    // 获取当前月份
    var nowMonth = date.getMonth() + 1;

    // 获取当前是几号
    var strDate = date.getDate();

    // 添加分隔符“-”
    var seperator = "-";

    // 对月份进行处理，1-9月在前面添加一个“0”
    if (nowMonth >= 1 && nowMonth <= 9) {
        nowMonth = "0" + nowMonth;
    }

    // 对月份进行处理，1-9号在前面添加一个“0”
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }

    // 最后拼接字符串，得到一个格式为(yyyy-MM-dd)的日期
    var nowDate = date.getFullYear() + seperator + nowMonth + seperator + strDate;
    return nowDate
}
