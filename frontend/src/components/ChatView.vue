<script setup lang="ts">
import { ref, nextTick } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}

const messages = ref<Message[]>([])
const input = ref('')
const isSending = ref(false)

const chatContainer = ref<HTMLElement | null>(null)

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

async function sendMessage() {
  const text = input.value.trim()
  if (!text || isSending.value) return

  // Add user message
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  scrollToBottom()

  // Add placeholder for assistant reply
  const assistantMsg: Message = {
    role: 'assistant',
    content: '',
    isStreaming: true,
  }
  messages.value.push(assistantMsg)
  isSending.value = true
  scrollToBottom()

  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    })

    if (!response.ok) {
      assistantMsg.content = `请求失败 (HTTP ${response.status})`
      assistantMsg.isStreaming = false
      return
    }

    const reader = response.body?.getReader()
    if (!reader) {
      assistantMsg.content = '无法读取响应流'
      assistantMsg.isStreaming = false
      return
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // Parse SSE events
      const lines = buffer.split('\n')
      buffer = '' // reset and re-accumulate incomplete lines

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        if (!line.startsWith('data: ')) continue

        // Rejoin the rest as buffer (incomplete lines)
        buffer = lines.slice(i + 1).join('\n')

        const jsonStr = line.slice(6) // remove "data: "
        try {
          const data = JSON.parse(jsonStr)
          if (data.delta) {
            assistantMsg.content += data.delta
            scrollToBottom()
          } else if (data.done) {
            assistantMsg.isStreaming = false
          } else if (data.error) {
            assistantMsg.content = `错误: ${data.error}`
            assistantMsg.isStreaming = false
          }
        } catch {
          // skip malformed JSON
        }

        // Only process one data line per loop iteration
        break
      }
    }

    // Final safety: if stream ended without "done", mark complete
    assistantMsg.isStreaming = false
  } catch (err: any) {
    assistantMsg.content = `网络错误: ${err.message || '连接失败'}`
    assistantMsg.isStreaming = false
  } finally {
    isSending.value = false
  }
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="chat-view">
    <div class="chat-messages" ref="chatContainer">
      <div v-if="messages.length === 0" class="chat-empty">
        <div class="empty-icon">💬</div>
        <p>开始和 AI 文档助手对话吧</p>
      </div>

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['chat-bubble', msg.role]"
      >
        <div class="bubble-label">{{ msg.role === 'user' ? '你' : 'AI' }}</div>
        <div class="bubble-content">
          {{ msg.content }}
          <span v-if="msg.isStreaming" class="cursor-blink">|</span>
        </div>
      </div>
    </div>

    <div class="chat-input-area">
      <textarea
        v-model="input"
        :disabled="isSending"
        class="chat-input"
        placeholder="输入消息，Enter 发送，Shift+Enter 换行"
        rows="2"
        @keydown="onKeydown"
      ></textarea>
      <button
        class="chat-send-btn"
        :disabled="isSending || !input.trim()"
        @click="sendMessage"
      >
        {{ isSending ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  gap: 12px;
}

.empty-icon {
  font-size: 48px;
}

.chat-bubble {
  max-width: 80%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-bubble.user {
  align-self: flex-end;
}

.chat-bubble.assistant {
  align-self: flex-start;
}

.bubble-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  padding: 0 4px;
}

.chat-bubble.user .bubble-label {
  text-align: right;
}

.bubble-content {
  padding: 10px 16px;
  border-radius: 16px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-bubble.user .bubble-content {
  background: #4f46e5;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-bubble.assistant .bubble-content {
  background: #fff;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 4px;
}

.cursor-blink {
  animation: blink 0.8s infinite;
  color: #4f46e5;
  font-weight: 300;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.chat-input-area {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #fff;
  flex-shrink: 0;
}

.chat-input {
  flex: 1;
  resize: none;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 10px 14px;
  outline: none;
  transition: border-color 0.15s;
}

.chat-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.chat-send-btn {
  align-self: flex-end;
  padding: 10px 24px;
  border: none;
  border-radius: 12px;
  background: #4f46e5;
  color: #fff;
  font-weight: 500;
  font-size: 14px;
  transition: background 0.15s;
  white-space: nowrap;
}

.chat-send-btn:hover:not(:disabled) {
  background: #4338ca;
}

.chat-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
