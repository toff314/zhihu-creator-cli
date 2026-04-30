# AGENTS.md — Zhihu Creator CLI 开发指南

本文档为 AI Agent 和开发者提供项目结构、代码风格、工作流程的完整说明。

## 项目概述

zhihu-creator-cli 是一个 Agent-native 的知乎创作中心 CLI 工具，专注于内容创作者的日常操作：
- 创作中心文章管理（列表、详情、评论）
- 问题发现（推荐、搜索、详情、回答）
- 所有命令支持 `--json` 输出供程序消费

## 代码结构

```
zhihu_creator_cli/
├── cli.py          # Click CLI 命令定义（入口）
├── client.py       # Zhihu API 客户端（HTTP 调用封装）
├── display.py      # 终端显示逻辑（Rich 表格 + JSON 输出）
├── auth.py         # 认证管理（Cookie 存储/验证）
├── config.py       # 配置常量（API 端点、Headers）
├── adapters.py     # HTTP 适配器（强制 IPv4）
├── exceptions.py   # 自定义异常
└── __init__.py     # 版本信息
```

## 设计原则

### 1. CLI 命令组织（cli.py）

- 使用 Click 框架的 `@click.group` 组织命令层级
- 每个模块一个 group：`auth`, `articles`, `questions`
- 所有数据命令必须支持 `--json` 标志
- 使用装饰器模式：`@require_login`, `@json_option`, `@common_options`

```python
@cli.group(name="articles")
@require_login
def articles_group() -> None:
    """创作中心文章管理."""
    pass

@articles_group.command(name="list")
@common_options
@click.option("--status", default="all", type=click.Choice(["all", "published", "draft"]))
def list_articles(offset: int, limit: int, status: str, sort: str, json_mode: bool) -> None:
    ...
```

### 2. API 客户端（client.py）

- `ZhihuClient` 类封装所有 HTTP 调用
- 使用 `requests.Session` + `ForceIPv4Adapter` 强制 IPv4
- 低级方法 `_get()` 处理错误和 JSON 解析
- 每个业务方法返回原始 API dict（不做数据清洗）

```python
class ZhihuClient:
    def __init__(self, cookie_dict: dict[str, str]) -> None:
        self._session = requests.Session()
        self._session.mount("https://", ForceIPv4Adapter())
        ...
    
    def _get(self, url: str, **kwargs) -> dict:
        resp = self._session.get(url, **kwargs)
        return self._handle_response(resp, url)
```

### 3. 显示逻辑（display.py）

- 每个显示函数接受 `json_mode: bool` 参数
- `json_mode=True` 时输出紧凑 JSON
- `json_mode=False` 时使用 Rich 表格美化
- 时间戳格式化：`_fmt_ts()` 统一处理

```python
def show_creator_articles(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    # Rich 表格输出...
```

### 4. 异常处理（exceptions.py）

- `ZhihuCliError` — 基类
- `LoginError` — 认证失败
- `DataFetchError` — API 请求失败
- `PublishError` — 发布操作失败（暂未使用）

### 5. 配置管理（config.py）

- API 端点常量：`ZHIHU_API_V4`, `ZHIHU_ZHUANLAN_API`
- 浏览器 Headers：`get_browser_headers()` 返回一致的指纹
- Cookie 存储路径：`~/.zhihu-creator-cli/cookies.json`

## API 端点

| 功能 | 端点 | 状态 |
|------|------|------|
| 用户认证 | `/api/v4/me` | ✅ |
| 文章列表 | `/api/v4/members/{url_token}/articles` | ✅ |
| 文章详情 | `zhuanlan.zhihu.com/api/articles/{id}` | ✅ |
| 文章评论 | `/api/v4/articles/{id}/comments` | ⚠️ 待验证 |
| 问题推荐 | `/api/v3/feed/topstory/recommend` | ✅ |
| 问题搜索 | `/api/v4/search_v3` | ✅ |
| 问题详情 | `/api/v4/questions/{id}` | ⚠️ 可能 403 |
| 问题回答 | `/api/v4/questions/{id}/answers` | ✅ |
| 邀请回答 | `/api/v4/notifications/v2/recent` | ✅ |

## 开发工作流

### 环境准备

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"
```

### 代码检查

```bash
# Ruff lint + format
ruff check zhihu_creator_cli/
ruff format zhihu_creator_cli/

# Type check (mypy)
mypy zhihu_creator_cli/
```

### 测试验证

**重要**：所有功能必须进行自测验证，确保 API 调用可用：

```bash
# 1. 登录验证
zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"
zhihu-creator auth status

# 2. 文章功能测试
zhihu-creator articles list --limit 5
zhihu-creator articles detail <article_id>
zhihu-creator articles comments <article_id> --limit 5

# 3. 问题功能测试
zhihu-creator questions recommend --limit 5
zhihu-creator questions search "Python" --limit 5
zhihu-creator questions detail <question_id>
zhihu-creator questions answers <question_id> --limit 5
zhihu-creator questions invites --limit 5

# 4. JSON 输出验证
zhihu-creator articles list --json --limit 1
zhihu-creator questions detail <id> --json
```

### 添加新功能

1. 在 `client.py` 添加 API 方法
2. 在 `cli.py` 添加命令定义
3. 在 `display.py` 添加显示函数（如有新格式）
4. 自测验证：运行命令确认 API 可用
5. 运行 lint + typecheck

### 代码风格

- 行长度：100 字符
- 类型注解：使用 Python 3.10+ 语法 (`dict[str, str]`, `str | None`)
- 文档字符串：中文，简洁描述功能
- 无额外注释：代码自解释，避免冗余注释
- 日志：使用 `logging` 模块，非 print

## 已知问题

### 1. 文章评论 API 已移除

评论 API 需要动态签名（`x-zse-81` 或 `x-zse-96`），签名有效期短且生成算法复杂。
功能已移除，如需查看评论请使用浏览器访问文章页面。

### 2. 问题详情 API 需要多重策略

**状态**: ⚠️ 部分可用

直接访问 `/api/v4/questions/{id}` 返回 403（错误码 10003）。

当前实现的 fallback 策略：
1. 尝试直接 API（可能失败）
2. 从 answers API 获取基本字段（id, title, answer_count 等）
3. 通过 search API 搜索标题获取 description/detail 字段

注意：
- 无回答的问题无法通过 answers API 获取信息
- 问题详情（detail/description）需要通过搜索 API 获取
- 搜索 API 返回的 description 包含 HTML 标签，display.py 已做清理

### 3. 只读限制

知乎写操作（发布文章/回答）需要动态签名（`x-zst-81`），暂不支持。
需浏览器自动化工具实现。

## 已添加功能

以下功能已全部实现：

### 用户模块 (`users`)

| 命令 | 说明 |
|------|------|
| `users profile <url_token>` | 用户信息 |
| `users articles <url_token>` | 用户文章列表 |
| `users answers <url_token>` | 用户回答列表 |
| `users questions <url_token>` | 用户提问列表 |
| `users followers <url_token>` | 粉丝列表 |
| `users followees <url_token>` | 关注列表 |
| `users collections <user_id>` | 收藏夹列表（注意：使用 user_id，非 url_token） |

### 回答模块 (`answers`)

| 命令 | 说明 |
|------|------|
| `answers detail <answer_id>` | 回答详情 |

### 热榜模块 (`hot`)

| 命令 | 说明 |
|------|------|
| `hot list [--limit]` | 知乎热榜 |

## 命令使用示例

```bash
# 用户信息
zhihu-creator users profile toff314

# 用户文章
zhihu-creator users articles toff314 --limit 10

# 用户回答
zhihu-creator users answers toff314 --limit 10 --sort voteups

# 用户粉丝
zhihu-creator users followers toff314 --limit 20

# 回答详情
zhihu-creator answers detail 29960616

# 热榜
zhihu-creator hot list --limit 20
```

## 参考资源

- 项目内知乎仓库：
  - `zhihu-python/` — 老版本知乎爬虫，HTML 解析方式
  - `zhihu-api/` — 知乎 API 封装库，有签名加密实现
- 知乎 Web API：观察浏览器 DevTools Network 请求