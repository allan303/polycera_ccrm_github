// Superadmin 所有路由
export default [
    {
        path: '/user',
        name: 'user',
        meta: { loginRequired: true, title: 'models.user', model: 'user', title_root: 'models.user', type: '', hasOwner: false, hasShared: false, forSu: true },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/user"),
        children: [
            {
                path: 'list-total',

                meta: { suRequired: true, title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/user/children/listTotal"),
            },
            {
                path: 'list-deleted',
                meta: { suRequired: true, title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/user/children/listDeleted"),
            },
            {
                path: 'create',
                meta: { suRequired: true, title: 'actions.create', type: 'create' },
                component: () => import("@/views/user/children/create"),
            },
            {
                path: 'read/:sid',
                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/user/children/read"),
            },
            {
                path: 'edit/:sid',
                meta: { suRequired: true, title: 'actions.edit', type: 'edit' },

                component: () => import("@/views/user/children/edit"),
            },
        ]
    },
]