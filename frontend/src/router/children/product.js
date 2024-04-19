// Superadmin 所有路由
export default [
    {
        path: '/product',
        name: 'product',
        meta: { suRequired: false, title: 'models.orderProduct', model: 'product', title_root: 'models.orderProduct', type: '', hasOwner: false, hasShared: false, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/product"),
        children: [
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/product/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/product/children/listDeleted"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/product/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/product/children/read"),
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/product/children/edit"),
            },
        ]
    },
]