# zhihu-creator-cli

知乎创作助手 CLI — 专为内容创作者和 AI Agent 设计的只读命令行工具。

支持 Cookie 登录，所有命令支持 `--json` 输出供程序消费。

## 安装

```bash
pip install -e .
```

## 认证

从浏览器开发者工具复制 Cookie（必须包含 `z_c0`, `_xsrf`, `d_c0`）：

```bash
zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"
zhihu-creator auth status
zhihu-creator auth whoami
zhihu-creator auth logout
```

## 命令总览

13 个顶级命令组，覆盖知乎主要只读 API：

| 组 | 说明 | 子命令 |
|---|---|---|
| `auth` | 认证 | `login`, `logout`, `status`, `whoami` |
| `articles` | 创作中心文章 | `list`, `detail` |
| `questions` | 问题发现 | `recommend`, `search`, `detail`, `answers`, `invites` |
| `answers` | 回答 | `detail`, `comments`, `voters` |
| `users` | 用户资料与内容 | `profile`, `articles`, `answers`, `questions`, `followers`, `followees`, `collections`, `pins`, `activities`, `mutuals`, `following-topics`, `following-questions`, `following-columns`, `zvideos`, `columns` |
| `columns` | 专栏 | `list`, `recommend`, `search`, `detail`, `articles` |
| `hot` | 热榜 | `list` |
| `search` | 统一搜索 | `general`, `questions`, `answers`, `articles`, `columns`, `topics`, `people`, `top`, `preset-words` |
| `creator` | 创作中心 | `home`, `stats` |
| `topics` | 话题 | `detail`, `unanswered` |
| `collections` | 收藏夹 | `detail`, `contents` |
| `pins` | 想法 | `detail` |
| `notifications` | 通知 | `invites`, `messages` |

## 常用示例

```bash
# 热榜
zhihu-creator hot list --limit 20

# 搜索（7 种类型）
zhihu-creator search general "Python"
zhihu-creator search topics "AI工具"
zhihu-creator search people "张三"

# 创作中心
zhihu-creator creator home
zhihu-creator creator stats

# 用户内容
zhihu-creator users profile toff314
zhihu-creator users pins toff314
zhihu-creator users following-topics toff314

# 话题/收藏夹/想法
zhihu-creator topics detail 19740929
zhihu-creator collections contents 158014176
zhihu-creator pins detail 2033873153219372749

# 回答评论
zhihu-creator answers comments 29960616

# JSON 输出（供 Agent 使用）
zhihu-creator search topics "AI" --json
zhihu-creator hot list --json --limit 5
```

## 通用选项

| 选项 | 说明 |
|---|---|
| `--json` | 输出原始 JSON（所有数据命令可用） |
| `--offset` | 分页偏移（默认 0） |
| `--limit` | 每页数量（默认 20） |
| `-v, --verbose` | 调试日志 |

## 代码结构

```
zhihu_creator_cli/
├── cli.py              # 入口，仅注册根命令
├── auth.py             # 认证管理
├── config.py           # API 端点与 Headers 常量
├── adapters.py         # ForceIPv4 HTTP 适配器
├── exceptions.py       # 自定义异常
├── commands/           # Click 命令定义（14 个模块）
├── client/             # API 客户端（Mixin 架构，14 个模块）
└── display/            # 终端展示（14 个模块）
```

三层职责：`commands/` 定义参数和错误处理 → `client/` 调用 API 返回原始 dict → `display/` Rich 表格或 JSON 输出。

## 开发

```bash
pip install -e ".[dev]"
ruff check zhihu_creator_cli/
ruff format zhihu_creator_cli/
```

添加新功能：在 `client/` 加 Mixin 方法 → `commands/` 加命令 → `display/` 加展示函数。

## 限制

- **只读**：不支持发布/编辑（需动态签名 `x-zst-81`）
- **Cookie 过期**：遇到 401 需重新登录
- **部分接口 403**：问题详情、文章详情(v4) 需签名（项目使用 fallback 策略）