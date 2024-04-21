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

# Bug?
- @vueform/multiselect: version 2.6.6 CSS style is right, but when use NPM RUN SERVE bugs happend
- use 1.5.0 could run but CSS style does not show correctly


## 标准化
1. 每个views 只需要修改 ： 
    - /components/js.js
    - /components/CreateComponent
    - /components/ListItemOne
    即可实现所有基础功能

2. 特殊附加信息，另外实现，如Project 下的 Post 展示等 （其实大部分也是通过已存在的ListComponent直接使用）




