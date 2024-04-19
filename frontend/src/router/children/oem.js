// Superadmin 所有路由
export default [
    {
        path: '/oem',
        name: 'oem',
        meta: { loginRequired: true, title: 'models.oem', model: 'oem', title_root: 'models.oem', type: '', hasOwner: true, hasShared: true, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/oem"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/oem/children/listMe"),
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/oem/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/oem/children/listDeleted"),
            },
            {
                path: 'list-shared',

                meta: { title: 'actions.listShared', type: 'list' },
                component: () => import("@/views/oem/children/listShared"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/oem/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/oem/children/read"),
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/oem/children/edit"),
            },
        ]
    },
]