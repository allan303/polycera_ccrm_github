//Author : Jack Li
//Email  : allanth3@163.com
//Date   : 2020-11-01
//用于生产一些计算属性
export const createGetters = (state) => {
    return {
        isSu() { return state.cu ? state.cu.is_su : false },
        isLogin() {
            return state.access_token ? true : false
        },
        stateFromLocalStorage() {
            let v0 = localStorage.getItem('state')
            if (v0) {
                try {
                    return JSON.parse(v0)
                } catch {
                    return {}
                }
            }
        },
        cacheInfo() {
            return state.cacheInfo
        },
        getObjFromCache(sidName, sid) {
            // 通过sidName（project_sid）,和具体sid，获取 OBJECT
            const defaultDict = {
                owner_sid: "user"
            }
            if (!sidName || !sid) { return null }
            let cacheName = null//缓存key，减去“_sid”
            if (defaultDict[sidName]) { cacheName = defaultDict[sidName] } else {
                // 减去后4位 "_sid"
                cacheName = sidName.substring(0, sidName.length - 4)
            }
            const cacheList = state.cacheInfo[cacheName]
            if (!cacheList) { return null }
            // console.log(cacheList)
            // console.log(sid)
            for (let obj of cacheList) {
                if (obj.sid === sid) {
                    return obj
                }
            }
        },
        objName(sidName, sid, key) {
            //获取具体的key，默认=“sid”
            const obj = this.getObjFromCache(sidName, sid)
            if (!obj) { return null }
            if (!key) { return obj.name }
            else { return obj[key] }
        },
        expireRemainMinutes() {
            //过期剩余时间
            if (!state.expire_minutes || !state.token_recieve_time) { return 0 }
            const now = Date.now()//现在的时间戳 int
            const expireTimestamp = state.token_recieve_time + state.expire_minutes * 60 * 1000
            const delt_s = (expireTimestamp - now) / 1000//和拿到token的时间 过了多久
            return delt_s / 60
        },
        isTokenExpired() {
            const remain = this.expireRemainMinutes()
            if (!remain) { return true }
            if (remain <= 15) { return true }//5分钟有效期
            return false //返回剩余秒数
        }
    }
}

