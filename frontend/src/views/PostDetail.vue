<script setup>
import { useRoute} from 'vue-router'
import { ref, onMounted } from 'vue'
import { formatDate } from '@/utils/format.js'

// 获取当前路由对象并拿到id参数，使用空对象存储单篇文章
const route = useRoute()
const postId = route.params.id
const post = ref({})

onMounted(async () => {
    // 发送请求获取文章详情
    const response = await fetch(`/api/posts/${postId}`)
    post.value = await response.json()
})
</script>

<template>
    <div class="post-detail">
        <!-- 使用 v-if 判断 post.id 是否存在，避免在数据未加载完成时渲染页面 -->
        <article class="post-detail" v-if="post.id">
            <h1>{{ post.title }}</h1>
            <p>By {{ post.author.username }}</p>
            <p>{{ formatDate(post.created_at) }}</p>
            <p>{{ post.content }}</p>
            <span v-for="tag in post.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
        </article>

    <!-- 如果 post.id 不存在，显示加载中提示 -->
        <p v-else>加载中...</p>
    </div>
</template>

<style scoped>
.post-detail {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
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