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

## 快速启动（V0.1 后端）

在 `backend/` 目录下配置 `.env`（可参考项目根目录的 `.env.example`），至少需要：

```text
OPENAI_BASE_URL
OPENAI_API_KEY
MODEL_NAME
```

安装依赖并启动（Conda）：

```bash
# 首次创建环境（只需一次，环境名可自定义）
conda create -n fastapi-demo python=3.11 -y

# 激活你用于本项目的 Conda 环境
conda activate fastapi-demo   # 或 ai-doc-assistant、llm312 等你已有的环境

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

日常开发时，激活环境后直接启动：

```bash
conda activate fastapi-demo   # 换成你的环境名
cd backend
uvicorn app.main:app --reload --port 8000
```

测试：

```bash
curl http://127.0.0.1:8000/api/health

curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"请用一句话解释 RAG\"}"
```

API 文档：http://127.0.0.1:8000/docs

---

## 当前第一步

先不要写 Docker。

第一步在 PyCharm 中跑通（Python Interpreter 选 `fastapi-demo`）：

1. FastAPI 后端。
2. OpenAI 兼容接口调用。
3. `/api/chat` 基础接口。
4. `curl` 能收到模型回答。

完成这些后，再进入前端和 Docker。

---

## 当前进度（截至 2026-08-03）

V0.1 后端代码已完成，PyCharm + conda `fastapi-demo` + GitHub 推送链路跑通。

已实现：

- `/`、`/api/health`、`/api/chat`（POST，body `{message}`，返回 `{answer}`）
- `backend/app/services/llm.py` 单例 OpenAI 兼容客户端（懒加载、自动补 `/v1`、配置校验）
- `.env` / `.env.example` / `.gitignore`（`.env` 和 IDE 配置已屏蔽）
- README + 11 个 docs 全部中文化；5 个文档已适配 conda `fastapi-demo`
- git 仓库根在 `ai-doc-assistant/`，3 个 commit，GitHub 远端通过 PyCharm + PAT 推送成功

下一步：`docs/行动路径.md` 第 3 天的流式输出 `/api/chat/stream`。

详细总结见 [`docs/2026-08-03-文档修订说明.md`](docs/2026-08-03-文档修订说明.md)。

---

## 开发日志

### 2026-08-03

- **环境定型**：PyCharm + conda `fastapi-demo`（Python 3.13） + Git for Windows，不用 WSL。
- **代码**：`backend/app/main.py` 实现 `/`、`/api/health`、`/api/chat`；`backend/app/services/llm.py` 封装 OpenAI 兼容客户端；`backend/requirements.txt` 锁定依赖。
- **配置**：`backend/.env` 已填 OPENAI_BASE_URL / OPENAI_API_KEY / MODEL_NAME，未提交。
- **文档**：11 个 `docs/*.md` 全部中文化；`README.md`、`开发指南.md`、`行动路径.md`、`第一阶段接口实现说明.md`、`部署指南.md` 适配 conda + PyCharm；新增 `docs/2026-08-03-文档修订说明.md`。
- **Git**：仓库根迁回 `ai-doc-assistant/`；清理 8 个错跟踪文件（`.workbuddy-ai/`、`.idea/`、`test_main.http`、私人 txt）；3 个 commit；通过 PyCharm + PAT 推送至 GitHub。
- **commit**：`96fa734 初始化 --v0.1` / `802247c 第一阶段第一次提交` / `7e5edaa 第一阶段第一次提交` / `16b2224 文档更新`。
- **V0.1 收尾**：本地实跑 `uvicorn app.main:app` 通过，`curl /api/health` 与 `curl /api/chat` 返回模型回答正确。`backend/app/main.py` 改动已 commit 并 push 至 GitHub。`docs/行动路径.md` "明天"段全部勾选 ✅，V0.1 后端聊天接口完成。
- **下一步**：进入"第 3 天"——实现 `/api/chat/stream` 流式输出。

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
- [2026-08-03 进度与文档修订说明](docs/2026-08-03-文档修订说明.md)
