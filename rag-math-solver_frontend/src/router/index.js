import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import LoginPageWithPw from '@/views/LoginPageWithPw.vue'
import LoginPageWithCode from '@/views/LoginPageWithCode.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import ChangePassword from '@/components/ChangePassword.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home  // 需要创建这个组件
    },
    {
        path: '/login1',
        name: 'LoginPageWithPw',
        component: LoginPageWithPw
    },
    {
        path: '/login2',
        name: 'LoginPageWithCode',
        component: LoginPageWithCode
    },
    {
        path: '/register',
        name: 'RegisterPage',
        component: RegisterPage
    },
    {
        path: '/change1',
        name: 'ChangePassword',
        component: ChangePassword
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router