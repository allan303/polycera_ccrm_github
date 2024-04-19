// Superadmin 所有路由
export default [
    {
        path: '/project_update',
        name: 'project_update',
        // title: 'models.projectUpdate',
        meta: { loginRequired: true, model: 'project_update', title_root: 'models.projectUpdate', type: '', hasOwner: true, hasShared: false, forSu: true },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/project_update"),
        children: [
            {
                path: 'list-me',
                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/project_update/children/listMe"),
            },
            {
                path: 'list-total',
                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/project_update/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/project_update/children/listDeleted"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/project_update/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/project_update/children/read"),

            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/project_update/children/edit"),
            },
        ]
    },
]