// Superadmin 所有路由
export default [
    {
        path: '/auth',
        name: 'auth',
        meta: {
            title: 'models.personal', model: 'auth', title_root: 'models.personal', type: '', hasOwner: false, hasShared: false, forSu: false,
            //用于sideBar显示的手动指定
            sideRoutes: [
                {
                    label: "auth.profile",
                    route: `/auth/myprofile`,
                },
                {
                    label: "auth.changePwd",
                    route: `/auth/change-password`,
                },
            ],
        },
        //必须要有主 component，里面容纳router-view，用于显示children中的内容
        component: () => import("@/views/auth"),
        children: [
            {
                path: 'login',

                meta: { title: 'auth.login', type: 'login' },
                component: () => import("@/views/auth/children/login")
            },
            {
                path: 'myprofile',

                meta: { loginRequired: true, title: 'auth.profile', type: 'read' },
                component: () => import("@/views/auth/children/myprofile")
            },
            {
                path: 'myprofile/edit',

                meta: { loginRequired: true, title: 'auth.editProfile', type: 'edit' },
                component: () => import("@/views/auth/children/myprofileEdit")
            },
            {
                path: 'change-password',
                // name: 'changePassword',
                meta: { loginRequired: true, title: 'auth.changePwd', type: 'edit' },
                component: () => import("@/views/auth/children/changePassword")
            },
        ]
    },
]