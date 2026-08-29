import { createRouter, createWebHistory } from 'vue-router'
import PostList from '@/views/PostList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'PostList',
      component: PostList,
    },
  ],
})

export default router
