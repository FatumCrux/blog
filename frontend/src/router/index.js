import { createRouter, createWebHistory } from 'vue-router'
import PostList from '@/views/PostList.vue'
import PostDetail from '@/views/PostDetail.vue'

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
    }
  ],
})

export default router
