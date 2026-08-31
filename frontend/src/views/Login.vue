<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { request } from '@/utils/request.js'


const username = ref('')
const password = ref('')   
const error = ref('')  // 用于存储错误信息，初始为空字符串
const router = useRouter()  // 响应式数据：数据变化，页面自动刷新

async function login() {
    error.value = ''  // 清空错误信息
    try {
        if (!username.value || !password.value) {
            throw new Error('用户名和密码不能为空')  // 如果用户名或密码为空，抛出错误
        }
        const response = await request('/auth/login/',{
            method: 'POST',
            body: JSON.stringify({ username: username.value, password: password.value })
        })
        localStorage.setItem('token', response.access_token)  // 将access_token存入localStorage
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