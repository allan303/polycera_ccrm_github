// Superadmin 所有路由
export default [
    {
        path: '/project_oem',
        name: 'project_oem',
        // title: 'models.projectOem',
        meta: { loginRequired: true, model: 'project_oem', title_root: 'models.projectOem', type: '', hasOwner: true, hasShared: false, forSu: true },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/project_oem"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/project_oem/children/listMe"),
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/project_oem/children/listTotal"),
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/project_oem/children/listDeleted"),
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/project_oem/children/create"),
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/project_oem/children/read"),

            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/project_oem/children/edit"),
            },
        ]
    },
]