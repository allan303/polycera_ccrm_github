// Superadmin 所有路由
export default [
    {
        path: '/workgroup',
        name: 'workgroup',
        meta: { suRequired: true, title: 'models.workgroup', model: 'workgroup', title_root: 'models.workgroup', type: '', hasOwner: false, hasShared: false, forSu: true },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/workgroup"),
        children: [
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/workgroup/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/workgroup/children/listDeleted"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/workgroup/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/workgroup/children/read"),
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/workgroup/children/edit"),
            },
        ]
    },
]