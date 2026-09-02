<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { request } from '@/utils/request.js'

  const route = useRoute()
  const router = useRouter()
  const title = ref('')
  const content = ref('')
  const tagsInput = ref('')
  const message = ref('')
  const error = ref('')
  const postId = route.params.id  // 获取路由参数中的文章ID
  const isEditMode = !!postId  // 如果有文章ID，则为编辑模式，否则为创建模式，!!表示将postId转换为布尔值
  const loadFailed = ref(false)  // 用于标记加载文章失败的状态

  onMounted(async () => {
    if (isEditMode) {
      try {
        const post = await request(`/posts/${postId}`)  // 获取文章详情
        title.value = post.title
        content.value = post.content
        tagsInput.value = post.tags.map(t => t.name).join(',')  // 将标签数组转换为逗号分隔的字符串
      } catch (err) {
        loadFailed.value = true
        error.value = err.message
      }
    }
  })

  async function submitPost() {
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
      // await request('/posts/', {
      //     method: 'POST',
      //     body: JSON.stringify({ title: title.value, content: content.value, tags })
      // })
      // message.value = '上传成功'
      const body = JSON.stringify({
        title: title.value,
        content: content.value,
        tags,
      })
      if (isEditMode) {
        await request(`/posts/${postId}`, {
          method: 'PUT',
          body,
        })
        message.value = '编辑成功'
      } else {
        await request('/posts/', {
          method: 'POST',
          body,
        })
        message.value = '上传成功'
        // 清空输入框
        title.value = ''
        content.value = ''
        tagsInput.value = ''
      }
    } catch (err) {
      error.value = err.message
    }
  }
</script>

<template>  <!--Vue单文件组件必须包含在template里面-->
  <div class="write">
    <!-- 如果加载文章失败，显示错误信息 -->
    <p v-if="loadFailed">{{ error }}</p>
    <!-- 如果加载文章成功，显示表单 -->
    <template v-else>
      <h1>{{ isEditMode ? '是要修改什么吗？' : '今天想要分享什么呢？' }}</h1>
      <form @submit.prevent="submitPost">
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
        <button type="submit">提交</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p v-if="error">{{ error }}</p>
    </template>
  </div>
</template>