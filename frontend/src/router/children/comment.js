// Superadmin 所有路由
export default [
    {
        path: '/comment',
        name: 'comment',
        meta: { loginRequired: true, title: 'models.comment', model: 'comment', title_root: 'models.comment', type: '', hasOwner: true, hasShared: true, forSu: true },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/comment"),
        children: [
            {
                path: 'list-me',
                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/comment/children/listMe"),
            },
            {
                path: 'list-total',
                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/comment/children/listTotal"),
            },
            {
                path: 'list-deleted',
                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/comment/children/listDeleted"),
            },
            {
                path: 'create',
                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/comment/children/create"),
            },
            {
                path: 'read/:sid',
                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/comment/children/read"),
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/comment/children/edit"),
            },
        ]
    },
]