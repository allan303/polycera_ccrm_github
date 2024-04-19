// Superadmin 所有路由
export default [
    {
        path: '/order',
        name: 'order',
        meta: { loginRequired: true, title: 'models.order', model: 'order', title_root: 'models.order', type: '', hasOwner: true, hasShared: true, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/order"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/order/children/listMe"),
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/order/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/order/children/listDeleted"),
            },
            {
                path: 'list-shared',

                meta: { title: 'actions.listShared', type: 'list' },
                component: () => import("@/views/order/children/listShared"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/order/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/order/children/read")
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/order/children/edit"),
            },
            {
                path: 'chart-me',

                meta: { title: '订单 | 统计', type: 'chart' },
                component: () => import("@/views/order/children/chartMe"),
            },
        ]
    },
]