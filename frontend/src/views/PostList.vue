<script setup>
import { ref, onMounted } from 'vue'

// 响应式数据：数据变化，页面自动刷新
// 存放文章列表，初始为空数组
const posts = ref([])

// 挂载组件，向后端请求文章列表
// onMounted 是 Vue 3 的生命周期钩子函数，表示组件挂载完成后执行的逻辑
// 网络请求是异步的，可能需要等待一段时间才能返回结果，期间页面无法进行操作
// async 用于处理异步操作。请求发出去后不进行等待，页面正常运行，数据返回后再处理
// async/await 是 ES7 的语法糖，简化 Promise 的写法，让代码读起来像是同步
// fetch 是浏览器提供的 API，用于向服务器发送请求，返回一个 Promise 对象
onMounted(async () => {
    const response = await fetch('/api/posts/')  // vite代理把请求转发到localhost:8000端口，返回一个 Response 对象
    posts.value = await response.json()  // 将响应体解析为 JSON 格式的数据并存入posts.value中，触发页面刷新
})
</script>

<template>
  <div class="post-list">
    <h1>文章列表</h1>
    <!-- 使用 v-for 循环渲染每篇文章，给每篇文章一个article元素 -->
    <article v-for="post in posts" :key="post.id" class="post-item">
      <h2>{{ post.title }}</h2>
      <p>By {{ post.author.username }}</p>
      <p>{{ post.content }}</p>
      <!-- 使用 v-for 渲染标签数组 -->
      <span v-for="tag in post.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
    </article>
  </div>
</template>

<style scoped>
.post-list {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
}
.post-item {
  border-bottom: 1px solid #ccccff;
  padding: 10px 0;
}
.tag {
  display: inline-block;
  background-color: #e0e0e0ce;
  color: #333;
  padding: 2px 6px;
  margin-right: 5px;
  border-radius: 4px;
  font-size: 12px;
}
</style>

