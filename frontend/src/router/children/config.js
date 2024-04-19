// Superadmin 所有路由
export default [
    {
        path: '/config',
        name: 'config',
        meta: {
            loginRequired: true, title: 'models.config', model: 'config', title_root: 'models.config', type: '', hasOwner: false, hasShared: false, forSu: true,
            //用于sideBar显示的手动指定
            sideRoutes: [
                {
                    label: "models.config",
                    route: `/config/read`,
                },
            ],
        },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/config"),
        children: [
            {
                path: 'read',
                name: 'configRead',
                meta: { title: 'actions.read', type: 'read' },
                component: () => import("@/views/config/children/read")
            },
            {
                path: 'edit',
                name: 'configEdit',
                meta: { title: 'actions.edit', type: 'edit' },
                component: () => import("@/views/config/children/edit")
            }
        ]
    },
]