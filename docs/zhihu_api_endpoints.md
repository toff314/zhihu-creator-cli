# 知乎 Web API 端点汇总

> 数据来源：通过 `gh api search/code` 在 GitHub 上搜索 `api.zhihu.com`、`www.zhihu.com/api` 等引用，结合多个开源项目源码分析整理。所有端点已用 cookie 实测验证可用性。最后更新：2026-05-07（重构后）。

---

## 一、基础域名

| 域名 | 用途 |
|------|------|
| `https://www.zhihu.com/api/v4` | 主站 v4 API（最常用） |
| `https://www.zhihu.com/api/v3` | 主站 v3 API（feed、热榜等） |
| `https://api.zhihu.com` | 独立 API 域名（旧版接口，部分需签名） |
| `https://zhuanlan.zhihu.com/api` | 专栏 API |
| `https://www.zhihu.com/creator/api/v1` | 创作中心 v1 API（已废弃） |
| `https://lens.zhihu.com/api/v4` | 视频 API |

---

## 二、认证与登录

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/me` | GET | 当前登录用户信息 | ✅ | ✅ | 本项目 |
| `/api/v3/oauth/sign_in` | POST | OAuth 登录 | - | ❌ | lzjun567 |
| `/api/v3/oauth/captcha` | GET | 登录验证码 | - | ❌ | lzjun567 |
| `/api/v3/account/api/login/qrcode` | GET | QR 码登录 | - | ❌ | BAIGUANGMEI |

---

## 三、用户（People / Members）

### 3.1 用户资料

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/members/{url_token}` | GET | 用户资料（v4） | ✅ | ✅ | 本项目 |
| `/api.zhihu.com/people/{url_token}` | GET | 用户资料（api 域名） | ✅ | ❌ | ZhihuVAPI |

### 3.2 用户内容

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/members/{url_token}/articles` | GET | 用户文章列表 | ✅ | ✅ | 本项目 |
| `/api/v4/members/{url_token}/answers` | GET | 用户回答列表 | ✅ | ✅ | 本项目 |
| `/api/v4/members/{url_token}/questions` | GET | 用户提问列表 | ✅ | ✅ | 本项目 |
| `/api/v4/members/{url_token}/pins` | GET | 用户想法列表 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/zvideos` | GET | 用户视频列表 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/column-contributions` | GET | 用户专栏列表 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/marked-answers` | GET | 用户被收录回答 | ❌ (403) | ❌ | ZhihuVAPI |
| `/api.zhihu.com/people/{url_token}/activities` | GET | 用户动态 | ✅ | ✅ | ZhihuVAPI |

### 3.3 用户关注关系

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/members/{url_token}/followers` | GET | 粉丝列表 | ✅ | ✅ | 本项目 |
| `/api/v4/members/{url_token}/followees` | GET | 关注列表 | ✅ | ✅ | 本项目 |
| `/api/v4/members/{url_token}/following-topic-contributions` | GET | 关注的话题 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/following-questions` | GET | 关注的问题 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/following-columns` | GET | 关注的专栏 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/members/{url_token}/relations/mutuals` | GET | 互相关注列表 | ✅ | ✅ | Foxgeek36 |

### 3.4 用户收藏夹

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/people/{user_id}/collections` | GET | 用户收藏夹列表 | ✅ | ✅ | 本项目 |

### 3.5 用户屏蔽

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api.zhihu.com/settings/blocked_users` | GET | 屏蔽用户列表 | ✅ | ❌ | ZhihuVAPI |

---

## 四、问题（Question）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/questions/{id}` | GET | 问题详情 | ❌ (403) | ✅ (fallback) | 本项目 |
| `/api/v4/questions/{id}/answers` | GET | 问题回答列表 | ✅ | ✅ | 本项目 |
| `/api/v4/questions/{id}/followers` | GET | 问题关注者列表 | ✅ | ❌ | ZhihuVAPI |
| `/api.zhihu.com/questions/{id}/answers` | GET | 问题回答(api 域名) | ❌ (403) | ❌ | niuniuJQKKK |

---

## 五、回答（Answer）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/answers/{id}` | GET | 回答详情(v4) | ✅ | ✅ | 本项目 |
| `/api.zhihu.com/answers/{id}` | GET | 回答详情(api 域名) | ✅ | ❌ | ZhihuVAPI |
| `/api/v4/answers/{id}/voters` | GET | 回答投票人列表 | ✅ | ✅ | ZhihuVAPI |
| `/api/v4/answers/{id}/root_comments` | GET | 回答根评论 | ✅ | ✅ | Foxgeek36 |

---

## 六、文章（Article）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/zhuanlan.zhihu.com/api/articles/{id}` | GET | 文章详情(zhuanlan) | ✅ | ✅ | 本项目 |
| `/api.zhihu.com/articles/{id}` | GET | 文章详情(api 域名) | ❌ (403) | ❌ | Foxgeek36 |
| `/api/v4/articles/{id}` | GET | 文章详情(v4) | ❌ (403) | ❌ | Foxgeek36 |
| `/api/v4/articles/{id}/likers` | GET | 文章点赞人列表 | ✅ | ❌ | ZhihuVAPI |

---

## 七、想法（Pin）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api.zhihu.com/pins/{id}` | GET | 想法详情 | ✅ (需真实ID) | ✅ | ZhihuVAPI |

---

## 八、专栏（Column）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/zhuanlan.zhihu.com/api/columns/{slug}` | GET | 专栏详情(zhuanlan) | ✅ | ✅ | 本项目 |
| `/api.zhihu.com/columns/{slug}` | GET | 专栏详情(api 域名) | ✅ | ✅ | 本项目 |
| `/zhuanlan.zhihu.com/api/columns/{slug}/articles` | GET | 专栏文章(zhuanlan) | ✅ | ❌ | lzjun567 |
| `/api.zhihu.com/columns/{slug}/articles` | GET | 专栏文章(api 域名) | ✅ | ✅ | 本项目 |
| `/api.zhihu.com/columns/{slug}/followers` | GET | 专栏关注者 | ✅ | ❌ | ZhihuVAPI |
| `/api.zhihu.com/columns` | GET | 专栏分类推荐 | ✅ | ✅ | 本项目 |

---

## 九、收藏夹（Collection）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api.zhihu.com/collections/{id}` | GET | 收藏夹详情 | ✅ (仅元数据) | ✅ | Foxgeek36 |
| `/api.zhihu.com/collections/{id}/contents` | GET | 收藏夹内容列表 | ✅ | ✅ | ZhihuVAPI |
| `/api.zhihu.com/collections/{id}/answers` | GET | 收藏夹回答列表 | ✅ | ✅ | Foxgeek36 |
| `/api.zhihu.com/collections/{id}/followees` | GET | 收藏夹关注者 | ❌ (404) | ❌ | ZhihuVAPI |

---

## 十、话题（Topic）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api.zhihu.com/topics/{id}/basic` | GET | 话题基础信息 | ✅ | ✅ | ZhihuVAPI |
| `/api/v4/topics/{id}` | GET | 话题详情(v4) | ❌ (403) | ❌ | Foxgeek36 |
| `/api/v4/topics/{id}/topic_index` | GET | 话题索引 | ❌ (403) | ❌ | ZhihuVAPI |
| `/api.zhihu.com/topics/{id}/feeds/essence` | GET | 话题精华 | ❌ (403) | ❌ | ZhihuVAPI |
| `/api.zhihu.com/topics/{id}/feeds/top_activity` | GET | 话题动态 | ❌ (403) | ❌ | ZhihuVAPI |
| `/api.zhihu.com/topics/{id}/unanswered_questions` | GET | 话题待答问题 | ✅ | ✅ | ZhihuVAPI |

---

## 十一、评论（Comment）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/answers/{id}/root_comments` | GET | 回答根评论 | ✅ | ✅ | Foxgeek36 |
| `/api.zhihu.com/comments/{id}/child_comments` | GET | 子评论 | ✅ | ❌ | ZhihuVAPI |

---

## 十二、搜索（Search）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/search_v3?t=general` | GET | 综合搜索 | ✅ | ✅ | niuniuJQKKK |
| `/api/v4/search_v3?t=question` | GET | 问题搜索 | ✅ | ✅ | 本项目 |
| `/api/v4/search_v3?t=answer` | GET | 回答搜索 | ✅ | ✅ | - |
| `/api/v4/search_v3?t=article` | GET | 文章搜索 | ✅ | ✅ | - |
| `/api/v4/search_v3?t=column` | GET | 专栏搜索 | ✅ | ✅ | 本项目 |
| `/api/v4/search_v3?t=topic` | GET | 话题搜索 | ✅ | ✅ | - |
| `/api/v4/search_v3?t=people` | GET | 用户搜索 | ✅ | ✅ | - |
| `/api/v4/search/top_search` | GET | 热搜关键词 | ✅ (有数据) | ✅ | niuniuJQKKK |
| `/api/v4/search/preset_words` | GET | 搜索预设词 | ✅ (有数据) | ✅ | Foxgeek36 |

---

## 十三、热榜与 Feed

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v3/feed/topstory/hot-lists/total` | GET | 热榜 | ✅ | ✅ | 本项目 |
| `/api/v3/feed/topstory/recommend` | GET | 推荐内容 | ✅ | ✅ | 本项目 |

---

## 十四、通知（Notification）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/api/v4/notifications/v2/recent?entry_name=all` | GET | 所有通知 | ✅ | ✅ | 本项目 |
| `/api/v4/notifications/v2/recent?entry_name=message` | GET | 消息通知 | ✅ | ✅ | - |
| `/api/v4/notifications/v2/recent?entry_name=invite` | GET | 邀请回答通知 | ✅ | ✅ | - |

---

## 十五、创作中心（Creator）

| 端点 | 方法 | 说明 | 可用 | 项目已用 | 来源 |
|------|------|------|------|----------|------|
| `/creator/api/v1/home` | GET | 创作中心首页 | ❌ (404) | ❌ | BAIGUANGMEI |
| `/creator/api/v1/stats/overview` | GET | 创作数据统计 | ❌ (404) | ❌ | BAIGUANGMEI |
| `/api/v4/creator/content_stats` | GET | 创作数据统计(v4) | ❌ (404) | ❌ | BAIGUANGMEI |

---

## 十六、不可用端点汇总（需签名或已废弃）

| 端点 | HTTP | 原因 |
|------|------|------|
| `/creator/api/v1/home` | 404 | 端点不存在 |
| `/creator/api/v1/stats/overview` | 404 | 端点不存在 |
| `/api/v4/questions/{id}` | 403 | 需 x-zse-96 签名 |
| `/api/v4/articles/{id}` | 403 | 需 x-zse-96 签名 |
| `/api.zhihu.com/articles/{id}` | 403 | 需签名 |
| `/api/v4/members/{url_token}/marked-answers` | 403 | 需签名 |
| `/api/v4/topics/{id}` | 403 | 需签名 |
| `/api/v4/topics/{id}/topic_index` | 403 | 需签名 |
| `/api.zhihu.com/topics/{id}/feeds/essence` | 403 | 需签名 |
| `/api.zhihu.com/topics/{id}/feeds/top_activity` | 403 | 需签名 |
| `/api.zhihu.com/questions/{id}/answers` | 403 | 需签名 |
| `/lens.zhihu.com/api/v4/videos/{id}` | 403 | 需签名 |
| `/api/v4/creator/content_stats` | 404 | 已废弃 |
| `/api/v4/creator/statistics/content` | 404 | 不存在 |
| `/api/v4/creator/statistics/fans` | 404 | 不存在 |

---

## 十七、实测可用但项目未用的 API 端点

以下端点实测可用但项目尚未使用，可作为后续扩展候选：

| # | 端点 | 说明 | 对应命令建议 | 优先级 |
|---|------|------|-------------|--------|
| 1 | `/api.zhihu.com/people/{url_token}` | 用户资料(api域名) | `users profile` 已有v4替代 | 低 |
| 2 | `/api/v4/questions/{id}/followers` | 问题关注者 | `questions followers` | 中 |
| 3 | `/api.zhihu.com/answers/{id}` | 回答详情(api域名) | `answers detail` 已有v4替代 | 低 |
| 4 | `/api/v4/articles/{id}/likers` | 文章点赞人 | `articles likers` | 中 |
| 5 | `/zhuanlan.zhihu.com/api/columns/{slug}/articles` | 专栏文章(zhuanlan) | `columns articles` 已有api域名替代 | 低 |
| 6 | `/api.zhihu.com/columns/{slug}/followers` | 专栏关注者 | `columns followers` | 低 |
| 7 | `/api.zhihu.com/collections/{id}/followees` | 收藏夹关注者 | ❌ (404) | - |
| 8 | `/api.zhihu.com/comments/{id}/child_comments` | 子评论 | `comments children` 或 `answers comments --children` | 中 |
| 9 | `/api.zhihu.com/settings/blocked_users` | 屏蔽用户列表 | `settings blocked-users` | 低 |
| 10 | `/zhuanlan.zhihu.com/api/columns/{slug}/articles` | 专栏文章(zhuanlan) | 已有替代 | 低 |

---

## 十八、备注

1. **写操作**（POST/DELETE）需要动态签名 `x-zse-81` / `x-zst-81` / `x-zse-96`，当前项目不支持
2. **403 端点**：问题详情、文章详情(v4)、话题详情(v4)、话题精华/动态均需 `x-zse-96` 签名才能访问
3. **评论 API** `/api/v4/answers/{id}/root_comments` 实测可用，项目已重新实现
4. **创作中心 API** `/creator/api/v1/home` 和 `/creator/api/v1/stats/overview` 实测 404，端点已不存在
5. `api.zhihu.com` 域名部分接口需要签名，但 `/answers/{id}`、`/pins/{id}`、`/collections/{id}/contents` 等实测可用
6. **搜索统一化**：所有搜索类型（general/question/answer/article/column/topic/people）通过统一 `search(kind, keyword)` 方法实现
7. **用户标识统一解析**：`resolve_user_id(url_token)` 自动将 url_token 转换为 user_id，`users collections` 同时兼容两种输入