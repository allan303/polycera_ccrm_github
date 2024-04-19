// Superadmin 所有路由

export default [
    {
        path: '/role',
        name: 'role',
        meta: {
            suRequired: true, title: 'models.role', model: 'role', title_root: 'models.role', type: '', hasOwner: false, hasShared: false, forSu: true,
        },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/role"),
        children: [
            {
                path: 'list-total',
                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/role/children/listTotal"),
            },
            {
                path: 'list-deleted',
                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/role/children/listDeleted"),
            },
            {
                path: 'create',
                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/role/children/create"),
            },
            {
                path: 'read/:sid',
                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/role/children/read"),
            },
            {
                path: 'edit/:sid',
                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/role/children/edit"),
            }
        ]
    },
]