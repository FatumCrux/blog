import { createRouter, createWebHistory } from 'vue-router'
import PostList from '@/views/PostList.vue'
import PostDetail from '@/views/PostDetail.vue'
import Login from '@/views/Login.vue'
import Write from '@/views/Write.vue'
import Admin from '@/views/Admin.vue'

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
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,
      meta: { requiresAuth: true }, // 需要登录才能访问
    },
    {
      path: '/write',
      name: 'Write',
      component: Write,
    },
    {
      path: '/write/:id',
      name: 'WriteEdit',
      component: Write,
    }
  ],
})

// 路由守卫，检查路由是否需要登录
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
