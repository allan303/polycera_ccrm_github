// Superadmin 所有路由
export default [
    {
        path: '/design',
        name: 'design',
        meta: { loginRequired: true, title: 'models.design', model: 'design', title_root: 'models.design', type: '', hasOwner: true, hasShared: true, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/design"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/design/children/listMe"),
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/design/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/design/children/listDeleted"),
            },
            {
                path: 'list-shared',

                meta: { title: 'actions.listShared', type: 'list' },
                component: () => import("@/views/design/children/listShared"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/design/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/design/children/read")
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/design/children/edit"),
            },
        ]
    },
]