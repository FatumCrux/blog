<script setup>
import { ref } from 'vue'
import { request } from '@/utils/request.js'

const title = ref('')
const content = ref('')
const tagsInput = ref('')
const message = ref('')
const error = ref('')

async function createPost() {
    error.value = ''
    message.value = ''
    if (!title.value || !content.value) {
            error.value = '标题和内容不能为空'
            return
    }
    try {
        const tags = tagsInput.value
        .split(/[,，]/)
        .map(tag => tag.trim())
        .filter(tag => tag)
        await request('/posts/', {
            method: 'POST',
            body: JSON.stringify({ title: title.value, content: content.value, tags })
        })
        message.value = '上传成功'
        // 清空输入框
        title.value = ''
        content.value = ''
        tagsInput.value = ''
    } catch (err) {
        error.value = err.message
    }
}
</script>

<template>
  <div class="admin">
    <h1>今天想要分享什么呢？</h1>
    <form @submit.prevent="createPost">
      <div>
        <label for="title">标题：</label>
        <input type="text" id="title" v-model="title" />
      </div>
      <div>
        <label for="content">内容：</label>
        <textarea id="content" v-model="content"></textarea>
      </div>
      <div>
        <label for="tags">标签</label>
        <input type="text" id="tags" v-model="tagsInput" placeholder="多个标签请用逗号分隔" />
      </div>
      <button type="submit">分享</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>