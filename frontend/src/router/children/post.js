// Superadmin 所有路由
export default [
    {
        path: '/post',
        name: 'post',
        meta: { loginRequired: true, title: 'models.post', model: 'post', title_root: 'models.post', type: '', hasOwner: true, hasShared: true, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/post"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/post/children/listMe")
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/post/children/listTotal")
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/post/children/listDeleted")
            },
            {
                path: 'list-shared',

                meta: { title: 'actions.listShared', type: 'list' },
                component: () => import("@/views/post/children/listShared"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/post/children/create")
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/post/children/read")
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/post/children/edit")
            },
            {
                path: 'dashboard',

                meta: { title: 'actions.dashboard', type: 'dashboard' },
                component: () => import("@/views/post/children/dashboard")
            },
        ]
    },
]