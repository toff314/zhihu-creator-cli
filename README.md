# 知乎创作助手 CLI

<p align="center">
  <strong>专为内容创作者打造的知乎 CLI 工具</strong><br>
  创作中心文章管理 · 问题推荐
</p>

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10+-blue.svg">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-green.svg">
</p>

---

## 功能特性

| 模块 | 功能 | 状态 |
|------|------|------|
| **认证** | Cookie 登录、登出、状态检查 | ✅ |
| **创作中心** | 文章列表（已发布/草稿）、文章详情 | ✅ |
| **问题发现** | 问题推荐（个性化）、问题搜索、问题详情、回答列表 | ✅ |
| **Agent 友好** | 所有数据命令支持 `--json` 输出 | ✅ |
| **网络优化** | 强制 IPv4 连接，避免 IPv6 超时 | ✅ |

## 安装

使用 `python -m venv` 创建虚拟环境并安装：

```bash
# 1. 克隆仓库
git clone https://github.com/toff314/zhihu-creator-cli.git
cd zhihu-creator-cli

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
# Linux / macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# 4. 安装依赖
pip install -e .
```

> **注意**：如果使用国内镜像源遇到 `hatchling` 包找不到的问题，请使用官方 PyPI 源：
>
> ```bash
> pip install -e . -i https://pypi.org/simple
> ```

## 快速开始

### 1. 登录

```bash
# Cookie 登录（唯一方式）
zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"

# 检查登录状态
zhihu-creator auth status
```

### 2. 创作中心

```bash
# 查看文章列表
zhihu-creator articles list --limit 10

# 查看文章详情（包含完整 HTML 内容）
zhihu-creator articles detail 2032112310991499955
```

### 3. 问题推荐

```bash
# 获取推荐问题
zhihu-creator questions recommend --limit 10

# 搜索问题
zhihu-creator questions search "Python 学习" --limit 20

# 查看问题详情
zhihu-creator questions detail 302196756

# 查看问题回答
zhihu-creator questions answers 656013053 --limit 5
```

### 4. Agent / 脚本使用（JSON 输出）

所有数据命令支持 `--json` 标志：

```bash
# JSON 输出文章列表
zhihu-creator articles list --limit 5 --json

# JSON 输出问题推荐
zhihu-creator questions recommend --limit 5 --json

# 将结果保存到文件
zhihu-creator questions recommend --limit 10 --json > questions.json
```

## 命令结构

```
zhihu-creator
├── auth
│   ├── login --cookie
│   ├── logout
│   ├── status [--json]
│   └── whoami [--json]
├── articles
│   ├── list [--offset] [--limit] [--status] [--sort] [--json]
│   └── detail <article_id> [--json]
└── questions
    ├── recommend [--offset] [--limit] [--topic] [--json]
    ├── search <keyword> [--offset] [--limit] [--json]
    ├── detail <question_id> [--json]
    └── answers <question_id> [--offset] [--limit] [--sort] [--json]
```

## 验证过的 API

| API 端点 | 状态 |
|----------|------|
| `api/v4/me` (用户认证) | ✅ |
| `api/v4/members/{token}/articles` (文章列表) | ✅ |
| `zhuanlan.zhihu.com/api/articles/{id}` (文章详情) | ✅ |
| `api/v3/feed/topstory/recommend` (问题推荐) | ✅ |
| `api/v4/search_v3` (问题搜索) | ✅ |
| `api/v4/questions/{id}/answers` (回答列表) | ✅ |
| `api/v4/questions/{id}` (问题详情) | ⚠️ 可能返回 403，有 fallback |

## 技术说明

### 强制 IPv4

本项目所有 HTTP 请求强制使用 IPv4（通过 `source_address=("0.0.0.0", 0)`），避免在 IPv6 网络环境下出现连接超时问题。

### 只读限制

由于知乎写操作 API（发布回答/文章）需要动态签名验证（`x-zst-81` 等字段），本项目目前**仅支持读取操作**。写操作需要通过浏览器自动化工具（如 Playwright）实现。

## 依赖

- Python 3.10+
- `click` — CLI 框架
- `requests` — HTTP 客户端
- `rich` — 终端表格输出

## License

MIT License
- Python 3.10+
- `click` — CLI 框架
- `requests` — HTTP 客户端
- `rich` — 终端表格输出

## License

MIT License
