<script setup lang="ts">
import ChatView from './components/ChatView.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>AI 文档助手</h1>
      <span class="app-badge">V0.1</span>
    </header>
    <main class="app-main">
      <ChatView />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
}

.app-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.app-header h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.app-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 9999px;
  background: #eef2ff;
  color: #4f46e5;
  font-weight: 500;
}

.app-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
