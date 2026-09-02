import { defineStore } from 'pinia'

// 定义一个名为 auth 的 Pinia store，用于管理用户的登录状态和 token
// 这个 store 的 state 包含一个 token 属性，用于存储用户的登录 token
export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,  // 初始化 token，从 localStorage 中获取，如果没有则为 null
    }),
    actions: {
        login(token) {  // 登录方法，持久化 token 到 localStorage 中
            this.token = token
            localStorage.setItem('token', token)
        },
        logout() {  // 登出方法，从 localStorage 中移除 token
            this.token = null
            localStorage.removeItem('token')
        }
    }
})