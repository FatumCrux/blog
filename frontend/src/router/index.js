import { createRouter, createWebHistory } from 'vue-router'
import PostList from '@/views/PostList.vue'
import PostDetail from '@/views/PostDetail.vue'
import Login from '@/views/Login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'PostList',
      component: PostList,
    },
    {
      path: '/post/:id',
      name: 'PostDetail',
      component: PostDetail,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    }
  ],
})

export default router
