# API 设计

接口前缀：

```text
/api
```

第一阶段优先实现聊天接口，RAG 和工具接口后续补齐。

---

## 1. 健康检查

### GET `/api/health`

用途：

检查服务是否启动。

响应：

```json
{
  "status": "ok"
}
```

---

## 2. 普通聊天

### POST `/api/chat`

用途：

发送用户问题，返回模型回答。

请求：

```json
{
  "message": "请介绍一下 RAG 是什么",
  "session_id": "optional-session-id",
  "system_prompt": "你是一个严谨的 AI 应用助手"
}
```

响应：

```json
{
  "session_id": "session-id",
  "message_id": "message-id",
  "answer": "RAG 是检索增强生成...",
  "model": "model-name"
}
```

---

## 3. 流式聊天

### POST `/api/chat/stream`

用途：

使用 SSE 返回流式回答。

请求：

```json
{
  "message": "用三句话解释 FastAPI",
  "session_id": "optional-session-id"
}
```

响应类型：

```text
text/event-stream
```

事件示例：

```text
data: {"delta":"FastAPI"}
data: {"delta":" 是一个"}
data: {"delta":" Python Web 框架"}
data: {"done":true}
```

---

## 4. 会话管理

### GET `/api/sessions`

返回会话列表。

### POST `/api/sessions`

创建新会话。

请求：

```json
{
  "title": "RAG 学习"
}
```

### GET `/api/sessions/{session_id}/messages`

返回指定会话的消息历史。

---

## 5. 文档管理

### POST `/api/documents/upload`

上传文档。

请求：

```text
multipart/form-data
file=<document>
```

响应：

```json
{
  "document_id": "doc-id",
  "filename": "example.pdf",
  "status": "uploaded"
}
```

### GET `/api/documents`

返回文档列表。

### GET `/api/documents/{document_id}`

返回文档详情。

### DELETE `/api/documents/{document_id}`

删除文档及其向量索引。

---

## 6. RAG 问答

### POST `/api/rag/chat`

用途：

基于知识库回答问题。

请求：

```json
{
  "question": "这个文档里提到的报销流程是什么？",
  "document_ids": ["doc-id-1", "doc-id-2"],
  "top_k": 5
}
```

响应：

```json
{
  "answer": "根据文档内容，报销流程包括...",
  "sources": [
    {
      "document_id": "doc-id-1",
      "filename": "员工手册.pdf",
      "chunk_id": "chunk-id",
      "score": 0.82,
      "text": "相关片段摘要"
    }
  ]
}
```

---

## 7. 文档工具

### POST `/api/tools/summarize`

文档总结。

请求：

```json
{
  "document_id": "doc-id",
  "style": "brief"
}
```

### POST `/api/tools/extract-todos`

提取待办。

请求：

```json
{
  "document_id": "doc-id"
}
```

### POST `/api/tools/generate-report`

生成报告。

请求：

```json
{
  "document_ids": ["doc-id-1", "doc-id-2"],
  "report_type": "weekly"
}
```

---

## 8. 错误响应格式

统一格式：

```json
{
  "error": {
    "code": "LLM_TIMEOUT",
    "message": "模型调用超时，请稍后重试",
    "details": {}
  }
}
```

常见错误码：

| 错误码 | 含义 |
| --- | --- |
| `BAD_REQUEST` | 请求参数错误 |
| `FILE_TYPE_UNSUPPORTED` | 文件类型不支持 |
| `DOCUMENT_PARSE_FAILED` | 文档解析失败 |
| `LLM_TIMEOUT` | 模型调用超时 |
| `LLM_API_ERROR` | 模型接口错误 |
| `RAG_NO_CONTEXT` | 未检索到有效上下文 |
| `INTERNAL_ERROR` | 服务内部错误 |

