<script setup>
import { useRouter, RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const auth = useAuthStore()  // 引入authStore，用于管理登录状态

function logout() {
    auth.logout()  // 调用auth store的logout方法，清除token并更新登录状态
    router.push('/')  // 登出后跳转到首页
}

function goToWrite() {
  if (!auth.token) {
    router.push({ path: '/login', query: { msg: '请先登录再上传文章' } })  // 如果未登录，跳转到登录页面
    return
  }
  router.push('/write')  // 如果已登录，跳转到写作页面
}
</script>

<template>
  <div class="site">
    <header class="navbar">
      <RouterLink to="/" class="brand">
        <img alt="Darling Dance logo" class="logo" src="/img/DarlingDance.png" />
        <span>FatumCrux的小站</span>
      </RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink v-if="!auth.token" to="/login">登录</RouterLink>
        <a v-if="auth.token" href="#" @click.prevent="logout">登出</a>
        <!-- <RouterLink v-if="!auth.token" to="/register">注册</RouterLink>
        <RouterLink v-if="auth.token" to="/profile">个人中心</RouterLink>
        <RouterLink v-if="auth.token" to="/settings">设置</RouterLink> -->
        <a href="#" @click.prevent="goToWrite">写作</a>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;  /* flex左右布局 */
  justify-content: space-between;  /* logo靠左，链接靠右 */
  align-items: center;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #ccdeff;  /* 下边框，分隔导航栏和内容区 */
  background: #ccccff;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;  /* logo和文字之间的间距 */
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.nav-links a {
  margin-left: 1rem;
  text-decoration: none;
  color: #333;
}

/* 高亮当前路由链接 */
.nav-links a.router-link-exact-active {
  font-weight: bold;
  color: #4b0a76;
}

.content {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}
</style>
