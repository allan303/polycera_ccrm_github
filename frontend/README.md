# polycera_ccrm_frontend_bootstrap

## Author
- Author: Jack Li 李津晶
- Email: allanth3@163.com
- 未经作者同意不允许使用。

# Node
- Nodejs version: 14.21.3

## Note
1. Use bootstrap CSS UI, not a Vue3 UI component
2. Use self-made base components, like Input,Select,Button
## Project setup
```
npm install 
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```


## 标准化
1. 每个views 只需要修改 ： 
    - /components/js.js
    - /components/CreateComponent
    - /components/ListItemOne
    即可实现所有基础功能

2. 特殊附加信息，另外实现，如Project 下的 Post 展示等 （其实大部分也是通过已存在的ListComponent直接使用）

## 坑
1. 将Array通过v-for传递给子组件，是通过 :key="index" , 子组件中通过 index 和 inject Array 操作数据，v-for是不能重新自动渲染的。
    - 解决： v-for= "item,index of Array"  :key="item"


# ChangeLog
### 2022-2-4
- 前台登录过期的问题
- CEB选项更新
- Design 结果处，显示回收率等


