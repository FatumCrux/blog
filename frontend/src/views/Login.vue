<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { request } from '@/utils/request.js'
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()  // 引入authStore，用于管理登录状态
const username = ref('')
const password = ref('')   
const error = ref('')  // 用于存储错误信息，初始为空字符串
const router = useRouter()  // 响应式数据：数据变化，页面自动刷新
const route = useRoute()  // 响应式数据：获取路由信息

// 监听路由的query参数中的msg
watch(() => route.query.msg, (msg) => {
    error.value = msg || ''  // 如果路由中有msg参数，将其赋值给error.value，触发页面刷新
}, { immediate: true })  // immediate: true表示立即执行一次回调函数，确保页面加载时就能显示msg信息

async function login() {
    error.value = ''  // 清空错误信息
    try {
        if (!username.value || !password.value) {
            throw new Error('用户名和密码不能为空')
        }
        const response = await request('/auth/login',{
            method: 'POST',
            body: JSON.stringify({ username: username.value, password: password.value })
        })
        //localStorage.setItem('token', response.access_token)  // 将access_token存入localStorage
        auth.login(response.access_token)  // 使用 auth store 的 login 方法，将 access_token 持久化到 localStorage，并更新登录状态
        router.push('/')  // 登录成功后跳转到首页
    } catch (err) {
        error.value = err.message  // 将错误信息存入error.value中，触发页面刷新
    }
}
</script>

<template>
  <div class="login">
    <h1>登录</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">用户名：</label>
        <!-- v-model 双向绑定, 输入框的值会自动更新username.value -->
        <input type="text" id="username" v-model="username" />
      </div>
      <div>
        <label for="password">密码：</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <button type="submit">登录</button>
    </form>
    <!-- 如果error.value不为空，显示错误信息 -->
    <p v-if="error">{{ error }}</p>
  </div>
</template>