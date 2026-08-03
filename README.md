# AI Doc Assistant

个人 / 企业文档知识库 AI 助手。

用户上传 PDF、Word、Markdown、TXT 等文档后，可以通过聊天方式提问，系统基于文档内容检索相关片段，并调用大模型生成带引用的回答。后续扩展文档总结、待办提取、周报生成等工具能力。

---

## 项目目标

这个项目同时服务三个目标：

1. 秋招面试项目：展示 AI 应用开发、RAG、Agent 工具、部署和工程化能力。
2. 日常使用工具：处理课程资料、招聘 JD、简历、学习笔记、会议记录。
3. 学习主线项目：所有新技术围绕这个项目吸收，不再零散学习。

---

## 技术栈

第一阶段：

- 后端：Python、FastAPI、Pydantic、Uvicorn。
- 前端：Vue3、TypeScript、Vite。
- AI 接入：OpenAI 兼容接口。
- 数据库：SQLite。
- 向量检索：FAISS。
- 文档解析：PyMuPDF、python-docx。
- 部署：Docker、Docker Compose、Nginx、阿里云 ECS。

第二阶段可选升级：

- 数据库：MySQL。
- 向量库：Qdrant。
- 工具调用：Tool Calling / Function Calling。
- 评估：RAG 测试集、引用准确率、拒答准确率。

---

## 版本路线

| 版本 | 目标 | 核心验收 |
| --- | --- | --- |
| V0.1 | 聊天基础版 | FastAPI 成功调用模型，支持基础聊天 |
| V0.2 | 会话管理版 | 前端聊天页面、会话历史、Markdown 展示 |
| V0.3 | 文档知识库版 | 上传文档、解析、切片、Embedding、检索问答 |
| V0.4 | RAG 优化版 | 测试集、参数对比、拒答策略、引用优化 |
| V0.5 | Agent 工具版 | 总结文档、提取待办、生成报告 |
| V0.6 | 部署面试版 | Docker Compose、阿里云部署、面试文档 |

---

## 计划目录结构

```text
ai-doc-assistant/
  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
      rag/
      tools/
      main.py
    tests/
    Dockerfile
    requirements.txt

  frontend/
    src/
      components/
      pages/
      api/
      stores/
    Dockerfile
    package.json

  docs/
    产品需求文档.md
    行动路径.md
    系统架构.md
    开发指南.md
    API 设计.md
    第一阶段接口实现说明.md
    数据模型.md
    RAG 设计.md
    RAG 评估文档.md
    部署指南.md
    面试材料.md

  docker-compose.yml
  .env.example
  README.md
```

---

## 当前第一步

先不要写 Docker。

第一步先在 WSL Ubuntu 中跑通：

1. FastAPI 后端。
2. OpenAI 兼容接口调用。
3. `/api/chat` 基础接口。
4. `curl` 能收到模型回答。

完成这些后，再进入前端和 Docker。

---

## 文档索引

- [产品需求](docs/产品需求文档.md)
- [行动路径](docs/行动路径.md)
- [系统架构](docs/系统架构.md)
- [开发指南](docs/开发指南.md)
- [API 设计](docs/API 设计.md)
- [第一阶段接口实现说明](docs/第一阶段接口实现说明.md)
- [数据模型](docs/数据模型.md)
- [RAG 设计](docs/RAG 设计.md)
- [RAG 评估](docs/RAG 评估文档.md)
- [部署指南](docs/部署指南.md)
- [面试材料](docs/面试材料.md)
