// 封装fetch请求
// 现在每个请求都要写fetch，每个接口都要带token，都要处理错误
// 所以封装一个request函数，统一处理这些问题

const BASE_URL = '/api' // 后端接口的基础路径

export async function request(url, options = {}) {
    // 获取token
    const token = localStorage.getItem('token')
    // 设置请求头
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}), // 如果有token就加上Authorization头
        ...options.headers // 如果options里有headers，就覆盖默认的headers，方便以后上传文件时自定义头
    }
    // 合并请求选项
    const config = {
        ...options,
        headers
    }
    // 发送请求
    const response = await fetch(`${BASE_URL}${url}`, config)
    // 处理响应
    if (!response.ok) {
        const data = await response.json().catch(() => ({})) // 如果响应不是json格式，就返回空对象
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
    }
    return response.json()
}