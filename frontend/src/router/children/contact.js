// Superadmin 所有路由
export default [
    {
        path: '/contact',
        name: 'contact',
        meta: { loginRequired: true, title: 'models.contact', model: 'contact', title_root: 'models.contact', type: '', hasOwner: true, hasShared: true, forSu: false },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/contact"),
        children: [
            {
                path: 'list-me',

                meta: { title: 'actions.listMe', type: 'list' },
                component: () => import("@/views/contact/children/listMe")
            },
            {
                path: 'list-total',

                meta: { title: 'actions.listTotal', type: 'list' },
                component: () => import("@/views/contact/children/listTotal")
            },
            {
                path: 'list-deleted',

                meta: { title: 'actions.listDeleted', type: 'list' },
                component: () => import("@/views/contact/children/listDeleted")
            },
            {
                path: 'list-shared',

                meta: { title: 'actions.listShared', type: 'list' },
                component: () => import("@/views/contact/children/listShared")
            },
            {
                path: 'create',

                meta: { title: 'actions.create', type: 'create' },
                component: () => import("@/views/contact/children/create")
            },
            {
                path: 'read/:sid',

                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/contact/children/read")
            },
            {
                path: 'edit/:sid',

                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/contact/children/edit")
            },
            {
                path: 'insert-by-excel',
                meta: { title: 'actions.upload', type: 'upload' },
                component: () => import("@/views/contact/children/insertByExcel")
            },
        ]
    },
]