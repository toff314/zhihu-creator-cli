# AGENTS.md — Zhihu Creator CLI 开发指南

本文档为 AI Agent 和开发者提供项目结构、代码风格、工作流程的完整说明。

## 项目概述

zhihu-creator-cli 是一个 Agent-native 的知乎创作中心 CLI 工具，专注于内容创作者的日常操作：
- 创作中心文章管理（列表、详情）
- 问题发现（推荐、搜索、详情、回答）
- 用户信息查询（资料、内容、关注关系、收藏夹）
- 回答、想法、专栏、收藏夹、话题详情查看
- 热榜、搜索、通知等辅助功能
- 所有命令支持 `--json` 输出供程序消费

## 代码结构

```
zhihu_creator_cli/
├── cli.py              # Click CLI 入口（仅注册根命令和 group）
├── client/
│   ├── __init__.py     # ZhihuClient 导出
│   ├── base.py         # ZhihuClient 基类（session/headers/cookie/_get/_handle）
│   ├── creator.py      # 创作中心（暂无可用端点）
│   ├── search.py       # 搜索 Mixin
│   ├── users.py        # 用户 Mixin
│   ├── questions.py    # 问题 Mixin
│   ├── answers.py      # 回答 Mixin
│   ├── articles.py     # 文章 Mixin
│   ├── columns.py      # 专栏 Mixin
│   ├── collections.py  # 收藏夹 Mixin
│   ├── topics.py       # 话题 Mixin
│   ├── pins.py         # 想法 Mixin
│   └── notifications.py # 通知 Mixin
├── commands/
│   ├── __init__.py
│   ├── auth.py         # auth login/status/logout
│   ├── creator.py      # creator group（暂无子命令）
│   ├── search.py       # search general/question/column/topic/people + top/preset-words
│   ├── users.py        # users profile/articles/answers/questions/followers/followees/pins/...
│   ├── questions.py    # questions recommend/search/detail/answers/invites
│   ├── answers.py      # answers detail/comments
│   ├── articles.py     # articles list/detail/likers
│   ├── columns.py      # columns detail/articles/search/recommend
│   ├── collections.py  # collections detail/contents/answers
│   ├── topics.py       # topics detail/unanswered
│   ├── pins.py         # pins detail
│   ├── notifications.py # notifications invites/messages
│   └── hot.py          # hot list
├── display/
│   ├── __init__.py
│   ├── common.py       # _json_out, _fmt_ts, _clean_html, _paging_total, _show_empty
│   ├── creator.py
│   ├── search.py
│   ├── users.py
│   ├── questions.py
│   ├── answers.py
│   ├── articles.py
│   ├── columns.py
│   ├── collections.py
│   ├── topics.py
│   ├── pins.py
│   ├── notifications.py
│   └── hot.py
├── auth.py             # 认证管理（Cookie 存储/验证）
├── config.py           # 配置常量（API 端点、Headers）
├── adapters.py         # HTTP 适配器（强制 IPv4）
├── exceptions.py       # 自定义异常
└── __init__.py         # 版本信息
```

## 设计原则

### 1. 三层分离架构

- `commands/*`：参数定义、命令名、错误处理（Click 框架）
- `client/*`：各资源领域 API 调用，复用 `base.py` 的 session/headers/cookie
- `display/*`：各资源领域展示逻辑，`json_mode` 时直接输出 JSON

### 2. CLI 命令组织（commands/）

- 使用 Click 框架的 `@click.group` 组织命令层级
- 每个资源类型一个顶级 group：`auth`, `articles`, `questions`, `answers`, `users`, `search`, `hot`, `columns`, `collections`, `topics`, `pins`, `notifications`, `creator`
- 所有数据命令必须支持 `--json` 标志
- 使用装饰器模式：`@require_login`, `@json_option`, `@common_options`

### 3. API 客户端（client/）

- `ZhihuClient` 类封装所有 HTTP 调用，位于 `client/base.py`
- 使用 `requests.Session` + `ForceIPv4Adapter` 强制 IPv4
- 低级方法 `_get()` 处理错误和 JSON 解析
- `_get_no_xsrf()` 处理不需要 xsrf 的请求（search、feed 等）
- 每个业务方法返回原始 API dict（不做数据清洗）
- 各资源领域通过 Mixin 类组织，组合在 `ZhihuClient` 中

```python
class ZhihuClient(SearchMixin, UsersMixin, QuestionsMixin, ...):
    def __init__(self, cookie_dict: dict[str, str]) -> None:
        self._session = requests.Session()
        self._session.mount("https://", ForceIPv4Adapter())
        ...
```

### 4. 显示逻辑（display/）

- 每个显示函数接受 `json_mode: bool` 参数
- `json_mode=True` 时输出紧凑 JSON（`_json_out()`）
- `json_mode=False` 时使用 Rich 表格美化
- 公共工具在 `display/common.py`：`_json_out`, `_fmt_ts`, `_clean_html`, `_paging_total`, `_show_empty`

### 5. 异常处理（exceptions.py）

- `ZhihuCliError` — 基类
- `LoginError` — 认证失败
- `DataFetchError` — API 请求失败

### 6. 配置管理（config.py）

- API 端点常量：`ZHIHU_API_V4`, `ZHIHU_ZHUANLAN_API`, `ZHIHU_API`
- 浏览器 Headers：`get_browser_headers()` 返回一致的指纹
- Cookie 存储路径：`~/.zhihu-creator-cli/cookies.json`

## 命令一览

| 命令 | 说明 | 状态 |
|------|------|------|
| `auth login --cookie` | Cookie 登录 | ✅ |
| `auth status` | 登录状态 | ✅ |
| `auth logout` | 退出登录 | ✅ |
| `articles list` | 创作中心文章列表 | ✅ |
| `articles detail <id>` | 文章详情 | ✅ |
| `articles likers <id>` | 文章点赞人列表 | ✅ |
| `questions recommend` | 推荐问题 | ✅ |
| `questions search <kw>` | 问题搜索 | ✅ |
| `questions detail <id>` | 问题详情（fallback） | ✅ |
| `questions answers <id>` | 问题回答列表 | ✅ |
| `questions invites` | 邀请回答通知 | ✅ |
| `answers detail <id>` | 回答详情 | ✅ |
| `answers comments <id>` | 回答评论 | ✅ |
| `users profile <url_token>` | 用户信息 | ✅ |
| `users articles <url_token>` | 用户文章列表 | ✅ |
| `users answers <url_token>` | 用户回答列表 | ✅ |
| `users questions <url_token>` | 用户提问列表 | ✅ |
| `users followers <url_token>` | 粉丝列表 | ✅ |
| `users followees <url_token>` | 关注列表 | ✅ |
| `users collections <user_id>` | 收藏夹列表 | ✅ |
| `users pins <url_token>` | 用户想法列表 | ✅ |
| `users following-topics <url_token>` | 关注的话题 | ✅ |
| `users following-questions <url_token>` | 关注的问题 | ✅ |
| `users following-columns <url_token>` | 关注的专栏 | ✅ |
| `users mutuals <url_token>` | 互相关注 | ✅ |
| `hot list` | 知乎热榜 | ✅ |
| `search general <kw>` | 综合搜索（约20条混合） | ✅ |
| `search questions <kw>` | 问题搜索 | ✅ |
| `search columns <kw>` | 专栏搜索 | ✅ |
| `search topics <kw>` | 话题搜索 | ✅ |
| `search people <kw>` | 用户搜索 | ✅ |
| `search top` | 热搜关键词 | ✅ |
| `search preset-words` | 搜索预设词 | ✅ |
| `columns detail <slug>` | 专栏详情 | ✅ |
| `columns articles <slug>` | 专栏文章列表 | ✅ |
| `columns search <kw>` | 专栏搜索 | ✅ |
| `columns recommend` | 专栏推荐 | ✅ |
| `columns followers <slug>` | 专栏关注者 | ✅ |
| `collections detail <id>` | 收藏夹详情 | ✅ |
| `collections contents <id>` | 收藏夹内容 | ✅ |
| `collections answers <id>` | 收藏夹回答 | ✅ |
| `topics detail <id>` | 话题详情 | ✅ |
| `topics unanswered <id>` | 话题待答问题 | ✅ |
| `topics essence <id>` | 话题精华内容（回答+文章） | ✅ |
| `pins detail <id>` | 想法详情 | ✅ |
| `notifications invites` | 邀请回答通知 | ✅ |
| `notifications messages` | 消息通知 | ✅ |
| `creator` | 创作中心（暂无可用 API） | ❌ |

## 开发工作流

### 环境准备

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 代码检查

```bash
ruff check zhihu_creator_cli/
ruff format zhihu_creator_cli/
mypy zhihu_creator_cli/
```

### 测试验证

**重要**：所有功能必须进行自测验证，确保 API 调用可用：

```bash
zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"
zhihu-creator auth status

zhihu-creator articles list --limit 5
zhihu-creator articles detail <article_id>
zhihu-creator articles likers <article_id> --limit 5

zhihu-creator questions recommend --limit 5
zhihu-creator questions search "Python" --limit 5
zhihu-creator questions detail <question_id>
zhihu-creator questions answers <question_id> --limit 5

zhihu-creator answers detail <answer_id>
zhihu-creator answers comments <answer_id> --limit 5

zhihu-creator users profile <url_token>
zhihu-creator users articles <url_token> --limit 5
zhihu-creator users followers <url_token> --limit 5
zhihu-creator users pins <url_token> --limit 5
zhihu-creator users following-topics <url_token>

zhihu-creator hot list --limit 10
zhihu-creator search general "Python" --limit 5
zhihu-creator search top

zhihu-creator columns detail pythoneer
zhihu-creator columns articles pythoneer --limit 5
zhihu-creator collections detail <collection_id>
zhihu-creator topics detail <topic_id>
zhihu-creator pins detail <pin_id>
zhihu-creator notifications invites --limit 5

# JSON 输出验证
zhihu-creator articles list --json --limit 1
zhihu-creator hot list --json --limit 5
```

### 添加新功能

1. 在 `client/` 对应文件添加 Mixin 方法
2. 在 `commands/` 对应文件添加命令定义
3. 在 `display/` 对应文件添加显示函数
4. 自测验证：运行命令确认 API 可用
5. 运行 lint + typecheck

### 代码风格

- 行长度：100 字符
- 类型注解：使用 Python 3.10+ 语法 (`dict[str, str]`, `str | None`)
- 文档字符串：中文，简洁描述功能
- 无额外注释：代码自解释，避免冗余注释
- 日志：使用 `logging` 模块，非 print

## 已知问题

### 1. 问题详情 API 需要多重策略

直接访问 `/api/v4/questions/{id}` 返回 403（错误码 10003）。

当前 fallback 策略：
1. 尝试直接 API（可能失败）
2. 从 answers API 获取基本字段
3. 通过 search API 搜索标题获取 description

### 2. 评论 API 部分可用

回答评论通过 `/api/v4/answers/{id}/root_comments` 可用，但文章评论需要动态签名已移除。

### 3. 创作中心 API 不可用

`/creator/api/v1/home` 和 `/creator/api/v1/stats/overview` 实测 404，端点不存在。`creator` 命令组暂时保留但无子命令。

### 4. 只读限制

知乎写操作（发布文章/回答）需要动态签名（`x-zst-81`），暂不支持。

## 命令使用示例

```bash
zhihu-creator users profile toff314
zhihu-creator users articles toff314 --limit 10
zhihu-creator users followers toff314 --limit 20
zhihu-creator users pins toff314 --limit 5
zhihu-creator answers detail 29960616
zhihu-creator answers comments 29960616 --limit 5
zhihu-creator hot list --limit 20
zhihu-creator search general "深度学习" --limit 5
zhihu-creator search top
zhihu-creator columns detail pythoneer
zhihu-creator collections detail 158014176
zhihu-creator topics detail 19740929
zhihu-creator notifications invites --limit 5
```

## 参考资源

- 项目内知乎仓库：
  - `zhihu-python/` — 老版本知乎爬虫，HTML 解析方式
  - `zhihu-api/` — 知乎 API 封装库，有签名加密实现
- 知乎 Web API：观察浏览器 DevTools Network 请求
- API 端点汇总：`docs/zhihu_api_endpoints.md`

## 可用 API 端点汇总

详见 `docs/zhihu_api_endpoints.md`，当前项目已用端点约 30 个，尚有约 10 个实测可用的端点可新增功能（如 `questions followers`、`articles likers`、`comments child_comments` 等）。