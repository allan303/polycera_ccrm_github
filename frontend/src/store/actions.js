//Author : Jack Li
//Email  : allanth3@163.com
//Date   : 2020-10-30
// 传入 state 用于 操作，CreateFns工厂函数返回一个 可以操作 state 的函数集合
import { createState } from './state'
import { getCacheInfo } from '@/myjs';
export const createActions = (state) => {
    return {
        // 设置 State，并且 保存到 LocalStorage
        setState(obj) {
            // 采用 键位 更新
            // Example: Object.assign(state, {cu:{...}}) 这样只更新 cu 部分
            Object.assign(state, obj);
            console.log('setState')
            //local
            this.setStateToLocalStorage()
        },
        //全部重置
        resetState() {
            // 采用 assign
            console.log('resetState')
            const newState = createState()
            newState.local = state.local
            state = Object.assign(state, newState);
            //local
            localStorage.removeItem('state')
        },
        setCacheInfo(cacheInfo) {
            //仅仅更新cacheinfo
            Object.assign(state.cacheInfo, cacheInfo)
        },
        //将当前的状态保存到 localstorage
        setStateToLocalStorage() {
            console.log('setStateToLocalStorage')
            const vs = JSON.stringify(state)
            localStorage.setItem('state', vs)
            return false
        },
        //从localStorage中获得保存的state，仅在重新启动时候
        getStateFromLocalStorage() {
            let v0 = localStorage.getItem('state')
            if (v0) {
                try {
                    let obj = JSON.parse(v0)
                    state = Object.assign(state, obj)
                    return false
                } catch {
                    // 全部设置为默认值
                    console.log('getStateFromLocalStorage出错')
                    this.resetState()
                    return false
                }
            }
        },
        updateCacheInfo(axios, names) {
            //更新State中的cache
            getCacheInfo(axios, names, true).then(res => {
                console.log(`updateCacheInfo:${names || 'names=空'}`)
                Object.assign(state.cacheInfo, res.data)
            })
        },
        updateLocalByKey(key, value) {
            //更新一个键值对
            state.local[key] = value
            this.setStateToLocalStorage()
        },
        updateLocal(data) {
            //全部更新
            state.local = Object.assign(state.local, data)
            this.setStateToLocalStorage()
        },
        switchLocale() {
            //切换 local.locale
            if (state.local.locale === 'zh') {
                state.local.locale = 'en'
            } else {
                state.local.locale = 'zh'
            }
        },
        setTokenRecieveTime() {
            state.token_recieve_time = Date.now()
        }
    }
}

