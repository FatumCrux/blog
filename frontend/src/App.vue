<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="site">
    <header class="navbar">
      <RouterLink to="/" class="brand">
        <img alt="Darling Dance logo" class="logo" src="/img/DarlingDance.png" />
        <span>FatumCrux</span>
      </RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/login">登录</RouterLink>
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
