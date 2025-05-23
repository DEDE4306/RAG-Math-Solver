import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import LoginPageWithPw from '@/views/LoginPageWithPw.vue'
import LoginPageWithCode from '@/views/LoginPageWithCode.vue'
import RegisterPage from '@/views/RegisterPage.vue'
// import ChatComponent from '@/components/ChatComponent.vue'
// import HistoryChatList from '@/components/HistoryChatList.vue'
import UserProfile from '@/components/UserProfile.vue'
import ChatPage from '@/views/ChatPage.vue'

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
        path: '/chat',
        name: 'ChatPage',
        component: ChatPage
    }, 
    {
        path: '/user',
        name: 'UserProfile',
        component: UserProfile
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router